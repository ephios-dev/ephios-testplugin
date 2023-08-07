from urllib.parse import urljoin

from django.conf import settings
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
    def get_body(cls, notification):
        return notification.data.get("body")

    @classmethod
    def get_actions(cls, notification):
        return [
            (
                _("Look at test notification"),
                urljoin(
                    settings.GET_SITE_URL(), reverse("testplugin:test_notifications")
                ),
            )
        ]
