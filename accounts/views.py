from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from .models import UserQuizResult


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class QuizResultListView(LoginRequiredMixin, ListView):
    model = UserQuizResult

    context_object_name = 'quizzes'
    paginate_by = 20


class QuizResultDetailView(LoginRequiredMixin, DetailView):
    model = UserQuizResult

    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz_id = self.kwargs['pk']
        quiz = self.model.objects.get(id=quiz_id)
        percent_correct = quiz.correct_answers / quiz.question_counts * 100
        context['percent_correct'] = percent_correct

        return context

