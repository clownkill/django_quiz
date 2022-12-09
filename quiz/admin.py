from django.contrib import admin
from nested_admin import NestedTabularInline, NestedModelAdmin

from .models import Category, Quiz, Question, Answer


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
