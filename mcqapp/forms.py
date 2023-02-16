from django import forms

from mcqapp.models import Chapter, Course, Questions, Subject


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = "__all__"
        widgets = {"question": forms.Textarea(attrs={"rows": 3})}
