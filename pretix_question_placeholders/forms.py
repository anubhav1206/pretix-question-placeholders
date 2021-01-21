from django import forms
from django_scopes.forms import SafeModelChoiceField
from pretix.base.models.items import Question

from .models import PlaceholderRule, QuestionPlaceholder


class QuestionPlaceholderCreateForm(forms.ModelForm):
    def __init__(self, *args, event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["question"].queryset = Question.objects.filter(event=event)

    class Meta:
        model = QuestionPlaceholder
        fields = ("question", "slug")
        field_classes = {
            "question": SafeModelChoiceField,
        }


class QuestionPlaceholderEditForm(forms.ModelForm):
    class Meta:
        model = QuestionPlaceholder
        fields = ("fallback_content", "use_fallback_when_unanswered")


class PlaceholderRuleForm(forms.ModelForm):
    def __init__(self, *args, placeholder=None, **kwargs):
        self.placeholder = placeholder
        super().__init__(*args, **kwargs)
        # Set appropriate options for the question type

    class Meta:
        model = PlaceholderRule
        fields = ("content", "condition_content", "condition_operation")
