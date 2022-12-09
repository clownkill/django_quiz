from django.db import models
from django.contrib.auth.models import User

from quiz.models import Quiz


class UserQuizResult(models.Model):
    user = models.ForeignKey(
        User,
        related_name='quiz_results',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    quiz = models.ForeignKey(
        Quiz,
        related_name='quiz_results',
        on_delete=models.CASCADE,
        verbose_name='Тест',
    )
    question_counts = models.PositiveSmallIntegerField(
        'Количество вопросов в тесте',
    )
    correct_answers = models.PositiveSmallIntegerField(
        'Количество верных ответов',
    )
    created_at = models.DateTimeField(
        'Дата прохождения теста',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at',]
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'

    def __str__(self):
        return f'{self.user.username} - {self.quiz.name} - {self.created_at.strftime("%d.%m.%Y %H:%m")}'
