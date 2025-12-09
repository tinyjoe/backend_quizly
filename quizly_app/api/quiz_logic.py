import tempfile
import json
import yt_dlp
import mimetypes
from google import genai

from django.conf import settings
from quizly_app.models import Quiz, Question


def download_audio_from_youtube(youtube_url):
    """
    Downloads audio from YouTube and returns the path to the temp file.
    """
    temp = tempfile.NamedTemporaryFile(suffix=".m4a", delete=False)
    temp_path = temp.name
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': temp_path,
        'postprocessors': [],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return temp_path


def transcribe_audio(file_path: str, api_key: str = settings.GEMINI_API_KEY):
    """
    Transcribes an audio file using Gemini API and returns the transcription text.
    """
    """ import whisper
    model = whisper.load_model("turbo")
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)
    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)
    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    # print the recognized text
    print(result.text)
    return result.text """
    """
    client = genai.Client(api_key=api_key)
    mime_type = define_mime_type(file_path)
    with open(file_path, 'rb') as f:
        uploaded = client.files.upload(file=f, filename=file_path.split('/')[-1], mime_type=mime_type)
    response = client.models.generate_content(model='gemini-2.0-flash', contents=[{'file_data': {'file_uri':   uploaded.uri, 'mime_type': mime_type}}
    ], config={"response_mime_type": "text/plain",})
    return response.text
    """
    


def define_mime_type(file_path):
    mime_type = mimetypes.guess_type(file_path)[0]
    if mime_type is None:
        if file_path.endswith('mp3'):
            mime_type = 'audio/mp3'
        elif file_path.endswith('.m4a'):
            mime_type = 'audio/mp4'
        else:
            mime_type = 'audio/mpeg'
    return mime_type


def generate_quiz_from_text(text: str, api_key: str = settings.GEMINI_API_KEY):
    """
    Sends transcription text to Gemini and returns a quiz JSON structure.
    """
    client = genai.Client(api_key=api_key)
    prompt = f"""
    Erstelle ein Quiz mit 10 Fragen basierend auf folgendem Video-Transkript:
    Format (STRICT JSON):
    {{
      'title': '...',
      'description': '...',
      'questions': [
        {{
          'question_title': '...',
          'question_options': ['A','B','C','D'],
          'answer': 'A'
        }}
      ]
    }}
    Transkript: 
    {text}
    """
    response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt, config={'response_mime_type': 'application/json'})
    return response.text


def save_quiz_to_db(user, youtube_url: str, quiz_data: dict):
    """
    Saves quiz and questions into database.
    Returns the created Quiz instance.
    """
    quiz = Quiz.objects.create(owner=user, title=quiz_data.get('title'), description=quiz_data.get('description'), video_url=youtube_url)
    for q in quiz_data.get('questions', []):
        Question.objects.create(quiz=quiz, question_title=q['question_title'], question_options=q['question_options'], answer=q['answer'])
    return quiz


def create_quiz_pipeline(user, youtube_url: str, api_key: str = settings.GEMINI_API_KEY):
    """
    Full pipeline: download → transcribe → Gemini → save.
    Raises exceptions normally so View can catch them.
    """
    audio_path = download_audio_from_youtube(youtube_url)
    text = transcribe_audio(audio_path, api_key)
    quiz_json = generate_quiz_from_text(text, api_key)
    quiz = save_quiz_to_db(user, youtube_url, quiz_json)
    return quiz
