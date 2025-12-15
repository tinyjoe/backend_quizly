from rest_framework import serializers
from quizly_app.models import Quiz, Question

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for a Question model.
    """
    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at']


class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for Quiz model including nested questions.
    """
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']
        write_only_fields = ['owner']


class QuizCreateSerializer(serializers.Serializer):
    """
    Serializer for generating a quiz from a YouTube URL.
    """
    url = serializers.URLField()
