import uuid

from django.db import models


class BaseModel(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
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

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Question(BaseModel):
    category = models.ForeignKey(
        Category,
        related_name='questions',
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    question = models.TextField(
        'Вопрос',
        max_length=1000
    )
    marks = models.IntegerField(
        'Оценка',
        default=1
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.question


class Answer(BaseModel):
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE,
        verbose_name='Ответ'
    )
    answer = models.TextField(
        'Ответ',
        max_length=1000
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
