from django.dispatch import receiver

from ephios.core.signals import footer_link


@receiver(
    footer_link, dispatch_uid="ephios.plugins.test_plugin.signals.pages_footer_links"
)
def pages_footer_links(sender, request, **kwargs):
    return {"Test Plugin is enabled.": "https://github.com/ephios-dev/ephios-testplugin"}
