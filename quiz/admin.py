from django.contrib import admin
from django.core.exceptions import ValidationError
from nested_admin import NestedTabularInline, NestedModelAdmin

from .models import Category, Quiz, Question, Answer
from .validators import answers_validator


class AnswerInline(NestedTabularInline):
    model = Answer
    extra = 0


class QuestionInline(NestedTabularInline):
    model = Question
    inlines = [AnswerInline]
    extra = 0



@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Question)
class QuestionAdmin(NestedModelAdmin):
    list_display = ['question', ]
    fields = ['question', 'quiz',]
    readonly_fields = ['created_at', 'updated_at',]
    inlines = [AnswerInline, ]


@admin.register(Quiz)
class QuizAdmin(NestedModelAdmin):
    list_display = ['name', 'category', ]
    inlines = [QuestionInline]
    list_filter = ['category', ]
    prepopulated_fields = {'slug': ('name',)}

    # def save_model(self, request, obj, form, change):
    #     for question in obj.questions.all():
    #         answers_count = question.answers.count()
    #         correct_answers_count = question.answers.filter(is_correct=True).count()
    #         if correct_answers_count == 0:
    #             raise ValidationError('Должен быть хотя бы один верный ответ')
    #         elif answers_count == correct_answers_count:
    #             raise ValidationError('Количество верных ответов не должно совпадать с количеством ответов')
    #
    #     super().save_model(request, obj, form, change)