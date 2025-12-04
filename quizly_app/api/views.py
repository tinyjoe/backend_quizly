from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import QuizSerializer, QuizCreateSerializer
from .quiz_logic import create_quiz_pipeline


class CreateQuizFromYoutubeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = QuizCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        youtube_url = serializer.validated_data["url"]
        try:
            quiz = create_quiz_pipeline(youtube_url)
            return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)