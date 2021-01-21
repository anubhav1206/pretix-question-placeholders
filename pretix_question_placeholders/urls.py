from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/question-placeholders/",
        views.QuestionPlaceholderList.as_view(),
        name="list",
    ),
    url(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/question-placeholders/new/",
        views.QuestionPlaceholderCreate.as_view(),
        name="create",
    ),
    url(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/question-placeholders/(?P<pk>[0-9]+)/",
        views.QuestionPlaceholderEdit.as_view(),
        name="edit",
    ),
    url(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/question-placeholders/(?P<pk>[0-9]+)/delete/",
        views.QuestionPlaceholderCreate.as_view(),
        name="delete",
    ),
]
