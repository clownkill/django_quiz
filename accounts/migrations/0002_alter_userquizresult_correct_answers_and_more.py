# Generated by Django 4.1.3 on 2022-12-09 07:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_alter_question_options_alter_quiz_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquizresult',
            name='correct_answers',
            field=models.PositiveSmallIntegerField(verbose_name='Количество верных ответов'),
        ),
        migrations.AlterField(
            model_name='userquizresult',
            name='question_counts',
            field=models.PositiveSmallIntegerField(verbose_name='Количество вопросов в тесте'),
        ),
        migrations.AlterField(
            model_name='userquizresult',
            name='quiz',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_results', to='quiz.quiz', verbose_name='Тест'),
        ),
        migrations.AlterField(
            model_name='userquizresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_results', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]