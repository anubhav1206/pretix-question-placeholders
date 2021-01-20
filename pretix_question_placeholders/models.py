from django.db import models
from django.utils.translation import gettext_lazy as _
from django_scopes import ScopedManager

from pretix.base.models import Question


class QuestionPlaceholder(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_("Question"),
        related_name="plugin_question_placeholders",
    )
    fallback_content = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Fallback"),
        help_text=_("Will be used when no other condition matches. Can be empty."),
    )
    use_fallback_when_unanswered = models.BooleanField(
        default=False,
        verbose_name=_("Use fallback when the question was not answered"),
        help_text=_(
            "Turn on if you always want to use the fallback. Otherwise, the placeholder will be ignored when the user has not answered the question."
        ),
    )

    objects = ScopedManager(organizer="question__event__organizer")


class PlaceholderRule(models.Model):
    class ComparisonOperation(models.TextChoices):
        EQUALS = "eq", _("Equals")
        IEQUALS = "ieq", _("Equals (case insensitive)")
        LESS_THAN = "lt", _("Less than / earlier than")
        LESS_OR_EQUAL_THAN = "lte", _("Less or same as / earlier or same as")
        MORE_THAN = "gt", _("Greater than / later than")
        MORE_OR_EQUAL_THAN = "gte", _("Greater or same as / later or same as")
        IS_TRUE = "bool", _("Is true / has been answered")

    placeholder = models.ForeignKey(
        QuestionPlaceholder, on_delete=models.CASCADE, related_name="rules"
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Content"),
        help_text=_("Will be inserted into the email if the condition matches."),
    )
    condition_content = models.TextField()
    condition_operation = models.CharField(
        max_length=4, choices=ComparisonOperation.choices
    )
