from django import forms
from django.forms.widgets import CheckboxSelectMultiple


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [answer for answer in question.get_answers()]
        self.fields['answers'] = forms.MultipleChoiceField(
            choices=choice_list,
            widget=CheckboxSelectMultiple
        )