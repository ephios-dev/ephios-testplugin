from django.dispatch import receiver
from django.urls import reverse
from ephios.core.signals import footer_link, register_notification_types

from ephios_testplugin.notification import TestNotification


@receiver(footer_link, dispatch_uid="ephios-testplugin.signals.pages_footer_links")
def pages_footer_links(sender, request, **kwargs):
    return {"Test Plugin": reverse("testplugin:test_index")}


@receiver(
    register_notification_types,
    dispatch_uid="ephios-testplugin.signals.register_notification_backends",
)
def register_notifcation_types(sender, **kwargs):
    return [TestNotification]
