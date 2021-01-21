from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from pretix.control.permissions import EventPermissionRequiredMixin

from .forms import (
    PlaceholderRuleFormSet,
    QuestionPlaceholderCreateForm,
    QuestionPlaceholderEditForm,
)
from .models import PlaceholderRule, QuestionPlaceholder


class QuestionPlaceholderList(EventPermissionRequiredMixin, ListView):
    permission = "can_change_event_settings"
    context_object_name = "question_placeholders"
    model = QuestionPlaceholder

    def get_queryset(self):
        from .signals import get_placeholders_for_event

        return get_placeholders_for_event(self.request.event)


class QuestionPlaceholderCreate(EventPermissionRequiredMixin, CreateView):
    permission = "can_change_event_settings"
    form_class = QuestionPlaceholderCreateForm
    model = QuestionPlaceholder

    def get_form_kwargs(self):
        result = super().get_form_kwargs()
        result["event"] = self.request.event

    def form_valid(self, form):
        super().form_valid(form)
        return redirect(
            reverse(
                "plugins:pretix_question_placeholders:edit",
                kwargs={
                    "organizer": self.request.event.organizer.slug,
                    "event": self.request.event.slug,
                    "layout": form.instance.pk,
                },
            )
        )


class QuestionPlaceholderEdit(EventPermissionRequiredMixin, UpdateView):
    permission = "can_change_event_settings"
    form_class = QuestionPlaceholderEditForm
    model = QuestionPlaceholder

    def get_object(self):
        from .signals import get_placeholders_for_event

        return get_object_or_404(
            get_placeholders_for_event(self.request.event), pk=self.kwargs["pk"]
        )

    @cached_property
    def formset(self):
        return PlaceholderRuleFormSet(
            data=self.request.POST if self.request.method == "POST" else None,
            placeholder=self.get_object(),
        )

    def form_valid(self, form):
        super().form_valid(form)
        return redirect(
            reverse(
                "plugins:pretix_question_placeholders:list",
                kwargs={
                    "organizer": self.request.event.organizer.slug,
                    "event": self.request.event.slug,
                },
            )
        )


class QuestionPlaceholderDelete(EventPermissionRequiredMixin, DeleteView):
    permission = "can_change_event_settings"
    model = QuestionPlaceholder

    def get_object(self):
        from .signals import get_placeholders_for_event

        return get_object_or_404(
            get_placeholders_for_event(self.request.event), pk=self.kwargs["pk"]
        )

    def get_success_url(self):
        return reverse(
            "plugins:pretix_question_placeholders:list",
            kwargs={
                "organizer": self.request.event.organizer.slug,
                "event": self.request.event.slug,
            },
        )
