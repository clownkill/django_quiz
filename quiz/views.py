from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.models import User

from .models import Category, Question, Quiz
from accounts.models import UserQuizResult
from .forms import QuestionForm


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category

    context_object_name = 'categories'
    paginate_by =  20


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    paginate_by = 20


class QuizView(LoginRequiredMixin, FormView):
    form_class = QuestionForm
    template_name = 'quiz/question.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, slug=self.kwargs['slug'])
        self.sitting = self.load_sitting()
        return super(QuizView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=QuestionForm):
        self.question = self.get_next_question()
        self.progress = self.get_sitting_progress()

        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizView, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        self.user_form_valid(form)
        if not self.request.session[f'{self.request.user.id}_question_list']:
            return self.final_result()
        self.request.POST = {}
        return super(QuizView, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizView, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['quiz'] = self.quiz
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
        if hasattr(self, 'progress'):
            context['progress'] = self.progress
        return context

    def load_sitting(self):
        if f'{self.request.user.id}_question_list' in self.request.session:
            return self.request.session[f'{self.request.user.id}_question_list']
        else:
            return self.new_quiz_session()

    def new_quiz_session(self):
        self.request.session.set_expiry(259200)
        questions = self.quiz.questions.all()
        question_list = [question.id for question in questions]

        self.request.session[f'{self.request.user.id}_question_list'] = question_list
        self.request.session[f'{self.request.user.id}_question_data'] = dict(
            incorrect_questions=[],
            order=question_list,
        )
        return self.request.session[f'{self.request.user.id}_question_list']
    #
    def get_next_question(self):
        next_question_id = self.request.session[f'{self.request.user.id}_question_list'][0]
        return Question.objects.get(id=next_question_id)
    #
    def get_sitting_progress(self):
        total = len(self.request.session[f'{self.request.user.id}_question_data']['order'])
        answered = total - len(self.request.session[f'{self.request.user.id}_question_list'])
        return (answered, total)

    def user_form_valid(self, form):
        guess = [
            int(user_answer) for user_answer in form.cleaned_data['answers']
        ]
        correct_answers = [
            answer.id for answer in self.question.answers.filter(is_correct=True)
        ]


        if guess == correct_answers:
            self.session_score(self.request.session, 1, 1)
        else:
            self.request.session[
                f'{self.request.user.id}_question_data'
            ]['incorrect_questions'].append(self.question.id)
            self.session_score(self.request.session, 0, 1)


        self.previous = {}

        self.request.session[
            f'{self.request.user.id}_question_list'
        ] = self.request.session[f'{self.request.user.id}_question_list'][1:]

    def final_result(self):
        incorrect_question_ids = self.request.session[
            f'{self.request.user.id}_question_data'
        ]['incorrect_questions']
        incorrect_questions = []
        if incorrect_question_ids:
            for id in incorrect_question_ids:
                incorrect_questions.append(Question.objects.get(id=id))

        session_score, session_possible = self.session_score(
            self.request.session)

        percent_correct = session_score / session_possible * 100

        results = {
            'incorrect_questions': incorrect_questions,
            'session_score': session_score,
            'possible': session_possible,
            'percent_correct': percent_correct,

        }

        UserQuizResult.objects.create(
            user=get_object_or_404(User, id=self.request.user.id),
            quiz=self.quiz,
            question_counts=session_possible,
            correct_answers=session_score
        )

        del self.request.session[f'{self.request.user.id}_question_list']

        results['previous'] = self.previous

        del self.request.session[f'{self.request.user.id}_question_data']
        self.request.session["session_score"], self.request.session["session_score_possible"] = 0, 0
        return render(self.request, 'quiz/result.html', results)

    def session_score(self, session, to_add=0, possible=0):
        if "session_score" not in session:
            session["session_score"], session["session_score_possible"] = 0, 0
        if possible > 0:
            session["session_score"] += to_add
            session["session_score_possible"] += possible

        return session["session_score"], session["session_score_possible"]
