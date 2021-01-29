from django.dispatch import receiver

from ephios.extra.signals import footer_link

@receiver(footer_link, dispatch_uid="ephios.plugins.test_plugin.signals.pages_footer_links")
def pages_footer_links(sender, request, **kwargs):
    return {"Test Plugin is here": "https://example.com"}
