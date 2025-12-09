from django.urls import path
from .views import CreateQuizFromYoutubeView, QuizListView, QuizDetailView

urlpatterns = [
    path('createQuiz/', CreateQuizFromYoutubeView.as_view(), name='create-quiz'),
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail')
]