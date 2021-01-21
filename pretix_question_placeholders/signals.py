from django.dispatch import receiver
from pretix.base.signals import register_mail_placeholders

from .models import QuestionPlaceholder
from .placeholder import QuestionMailPlaceholder


@receiver(register_mail_placeholders, dispatch_uid="placeholder_custom")
def register_mail_question_placeholders(sender, **kwargs):
    return [
        QuestionMailPlaceholder(placeholder)
        for placeholder in QuestionPlaceholder.objects.filter(question__event=sender)
    ]
