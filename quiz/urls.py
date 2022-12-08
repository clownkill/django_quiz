from django.urls import path

from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='home'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
    path('quiz/<slug:slug>/', views.QuizView.as_view(), name='quiz'),
    # path('api/get-quiz/', views.get_quiz, name='get_quiz'),
    # path('quizes/', views.quiz, name='quiz'),
]
