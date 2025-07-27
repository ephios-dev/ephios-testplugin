from django.dispatch import receiver
from django.template.loader import get_template
from django.urls import reverse
from ephios.core.signals import footer_link, register_notification_types, insert_html, HTML_HOMEPAGE_INFO

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

@receiver(
    insert_html,
    sender=HTML_HOMEPAGE_INFO,
    dispatch_uid="ephios-testplugin.signals.homepage_warning",
)
def homepage_warning(sender, request, **kwargs):
    return get_template("testplugin/homepage_content.html").render()