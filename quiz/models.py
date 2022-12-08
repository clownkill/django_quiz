import uuid

from django.db import models
from django.core.exceptions import ValidationError

from .validators import answers_validator

class BaseModel(models.Model):
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(
        'Название категории',
        max_length=100
    )
    slug = models.SlugField(
        max_length=250
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Quiz(BaseModel):
    name = models.CharField(
        'Название теста',
        max_length=250,
        unique=True
    )
    slug = models.SlugField(
        max_length=250
    )
    category = models.ForeignKey(
        Category,
        related_name='quizzes',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )

    class Meta:
        ordering = ['-created_at',]
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.name


class Question(BaseModel):
    quiz = models.ForeignKey(
        Quiz,
        related_name='questions',
        on_delete=models.CASCADE,
        verbose_name='Тест',
    )
    question = models.TextField(
        'Вопрос',
        max_length=1000
    )

    class Meta:
        ordering = ['-created_at',]
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.question

    def get_answers(self):
        return [
            (answer.id, answer.answer) for answer in self.answers.all()
        ]


class Answer(BaseModel):
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE,
        verbose_name='Ответ'
    )
    answer = models.CharField(
        'Ответ',
        max_length=250
    )
    is_correct = models.BooleanField(
        'Правильный ответ',
        default=False
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Oтветы'

    def __str__(self):
        return self.answer
