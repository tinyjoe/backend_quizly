import tempfile
import json
import yt_dlp
import google.generativeai as genai

from django.conf import settings
from quizly_app.models import Quiz, Question

ffmpeg_path = '/usr/local/bin/ffmpeg'   
ffprobe_path = '/usr/local/bin/ffprobe'


def download_audio_from_youtube(youtube_url: str):
    """
    Downloads audio from YouTube and returns the path to the temp file.
    """
    temp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    temp_path = temp.name
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_path,
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return temp_path


def transcribe_audio(file_path: str):
    """
    Takes an audio file, runs Whisper and returns the transcription text.
    """
    import whisper
    model = whisper.load_model('turbo')
    result = model.transcribe(file_path)
    return result['text']


def generate_quiz_from_text(text: str):
    """
    Sends transcription text to Gemini and returns a quiz JSON structure.
    """
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Erstelle ein Quiz basierend auf folgendem Text:
    {text}
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
    """
    response = model.generate_content(prompt)
    quiz_data = json.loads(response.text)
    return quiz_data


def save_quiz_to_db(youtube_url: str, quiz_data: dict):
    """
    Saves quiz and questions into database.
    Returns the created Quiz instance.
    """
    quiz = Quiz.objects.create(title=quiz_data.get('title'), description=quiz_data.get('description'), video_url=youtube_url)
    for q in quiz_data.get('questions', []):
        Question.objects.create(quiz=quiz, question_title=q['question_title'], question_options=q['question_options'], answer=q['answer'])
    return quiz


def create_quiz_pipeline(youtube_url: str):
    """
    Full pipeline: download → transcribe → Gemini → save.
    Raises exceptions normally so View can catch them.
    """
    audio_path = download_audio_from_youtube(youtube_url)
    text = transcribe_audio(audio_path)
    quiz_json = generate_quiz_from_text(text)
    quiz = save_quiz_to_db(youtube_url, quiz_json)
    return quiz
