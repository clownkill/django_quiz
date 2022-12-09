# Generated by Django 4.1.3 on 2022-12-09 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz', '0002_alter_question_options_alter_quiz_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserQuizResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_counts', models.PositiveSmallIntegerField(editable=False, verbose_name='Количество вопросов в тесте')),
                ('correct_answers', models.PositiveSmallIntegerField(editable=False, verbose_name='Количество верных ответов')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата прохождения теста')),
                ('quiz', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_results', to='quiz.quiz', verbose_name='Тест')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_results', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Результат теста',
                'verbose_name_plural': 'Результаты тестов',
                'ordering': ['-created_at'],
            },
        ),
    ]
