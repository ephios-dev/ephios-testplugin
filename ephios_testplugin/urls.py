from django.urls import path

from ephios_testplugin.views import (
    CrashView,
    EmailTemplateView,
    TestIndexView,
    TestNotificationsView, Http500View,
)

app_name = "testplugin"
urlpatterns = [
    path("test/", TestIndexView.as_view(), name="test_index"),
    path("test/crash/", CrashView.as_view(), name="test_crash"),
    path("test/500/", Http500View.as_view(), name="test_500"),
    path(
        "test/notifications/",
        TestNotificationsView.as_view(),
        name="test_notifications",
    ),
    path("test/email/", EmailTemplateView.as_view(), name="test_email_template"),
]
