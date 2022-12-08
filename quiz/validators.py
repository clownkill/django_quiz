from django.core.exceptions import ValidationError

def answers_validator(question):
    answers = question.answers.all()
    correct_answers_count = answers.filter(is_correct=True).count()
    if correct_answers_count == answers.count():
        raise ValidationError('Количество правильных ответов не может быть равно количеству ответов')
    elif correct_answers_count == 0:
        raise ValidationError('Должен быть хотябы один правильный ответ')
    return True