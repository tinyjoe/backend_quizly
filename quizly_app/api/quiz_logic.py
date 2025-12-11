import tempfile
import json
import yt_dlp
from google import genai
from google.genai import types

from django.conf import settings

from quizly_app.models import Quiz, Question


def download_audio_from_youtube(youtube_url):
    """
    Downloads audio from YouTube and returns the path to the temp file.
    """
    temp = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
    temp_path = temp.name
    ydl_opts = {
        'format': 'bestaudio[ext=mp3]/bestaudio/best',
        'outtmpl': temp_path,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return temp_path


def transcribe_audio(file_path):
    """
    Transcribes an audio file using Whisper and returns the transcription text.
    """
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    with open(file_path, 'rb') as audio_file:
        audio_data = audio_file.read()
    response = client.models.generate_content(model='gemini-2.5-flash', contents= ['Transcribiere die folgende Audiodatei ins Deutsche: ', types.Part.from_bytes(data=audio_data, mime_type='audio/mp3')])
    text = response.text
    if not text:
        raise ValueError("Transcription failed or returned empty text.")
    return text


def generate_quiz_from_text(text):
    """
    Sends transcription text to Gemini and returns a quiz JSON structure.
    """
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    prompt = f"""
    Erstelle ein Multiple-Choice-Quiz mit 10 Fragen basierend auf folgendem Video-Transkript:
    Das Format muss STRICT JSON sein:
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
    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt, config={'response_mime_type': 'application/json'})
    return json.loads(response.text)


def save_quiz_to_db(user, youtube_url, quiz_data):
    """
    Saves quiz and questions into database.
    Returns the created Quiz instance.
    """
    quiz = Quiz.objects.create(owner=user, title=quiz_data.get('title'), description=quiz_data.get('description'), video_url=youtube_url)
    for q in quiz_data.get('questions', []):
        Question.objects.create(quiz=quiz, question_title=q['question_title'], question_options=q['question_options'], answer=q['answer'])
    return quiz


def create_quiz_pipeline(user, youtube_url):
    """
    Full pipeline: download → transcribe → Gemini → save.
    Raises exceptions normally so View can catch them.
    """
    audio_path = download_audio_from_youtube(youtube_url)
    transcript = transcribe_audio(audio_path)
    quiz_json = generate_quiz_from_text(transcript)
    quiz = save_quiz_to_db(user, youtube_url, quiz_json)
    return quiz