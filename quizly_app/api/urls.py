from django.urls import path
from .views import CreateQuizFromYoutubeView

urlpatterns = [
    path('createQuiz/', CreateQuizFromYoutubeView.as_view(), name='create-quiz'),
]