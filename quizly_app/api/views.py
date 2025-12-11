from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.permissions import IsAuthenticated

from quizly_app.models import Quiz
from .serializers import QuizSerializer, QuizCreateSerializer
from .quiz_logic import create_quiz_pipeline
from .permissions import IsOwnerAndAuthenticated


class CreateQuizFromYoutubeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = QuizCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        youtube_url = serializer.validated_data["url"]
        try:
            quiz = create_quiz_pipeline(user=request.user, youtube_url=youtube_url)
            return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsOwnerAndAuthenticated]