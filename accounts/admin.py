from django.contrib import admin

from .models import UserQuizResult

@admin.register(UserQuizResult)
class UserQuizResultAdmin(admin.ModelAdmin):
    fields = [
        'user',
        'quiz',
        'question_counts',
        'correct_answers',
        'created_at',
    ]
    readonly_fields = ['created_at',]

    def has_add_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='',
                        extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(UserQuizResultAdmin, self).changeform_view(request, object_id,
                                                           extra_context=extra_context)
