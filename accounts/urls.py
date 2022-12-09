from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('account/', views.QuizResultListView.as_view(), name='account'),
    path('account/<int:pk>/', views.QuizResultDetailView.as_view(), name='results'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]