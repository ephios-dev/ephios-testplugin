from django.urls import reverse

from ephios.core.models import Notification
from ephios.core.services.notifications.types import AbstractNotificationHandler

from django.utils.translation import gettext_lazy as _


class TestNotification(AbstractNotificationHandler):
    slug = "testplugin_testnotification"
    title = _("The testplugin sends a test notification")

    @classmethod
    def send(cls, user, title, body):
        Notification.objects.create(
            slug=cls.slug,
            user=user,
            data={"title": title, "body": body},
        )

    @classmethod
    def get_subject(cls, notification):
        return notification.data.get("title")

    @classmethod
    def as_plaintext(cls, notification):
        return notification.data.get("body")

    @classmethod
    def get_url(cls, notification):
        return reverse("testplugin:test_notifications")
