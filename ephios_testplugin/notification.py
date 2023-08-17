from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ephios.core.models import Notification
from ephios.core.services.notifications.types import AbstractNotificationHandler
from ephios.core.templatetags.settings_extras import make_absolute


class TestNotification(AbstractNotificationHandler):
    slug = "testplugin_testnotification"
    title = _("The testplugin sends a test notification")

    @classmethod
    def send(cls, user, subject, body):
        Notification.objects.create(
            slug=cls.slug,
            user=user,
            data={"test_subject": subject, "test_body": body},
        )

    @classmethod
    def get_subject(cls, notification):
        return notification.data.get("test_subject")

    @classmethod
    def get_body(cls, notification):
        return notification.data.get("test_body")

    @classmethod
    def get_actions(cls, notification):
        return [
            (
                _("Look at test notification"),
                make_absolute( reverse("testplugin:test_notifications")
                ),
            )
        ]
