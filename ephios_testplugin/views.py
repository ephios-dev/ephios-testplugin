import io
import tempfile
from urllib.parse import urljoin
from email import generator as email_generator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from csp.decorators import csp_exempt
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import TemplateView, FormView

from ephios.core.models import Notification, Event, LocalParticipation, Consequence
from ephios.core.services.notifications.backends import send_all_notifications
from ephios.core.services.notifications.types import (
    NewProfileNotification,
    NewEventNotification,
    notification_type_from_slug,
    ProfileUpdateNotification,
    ParticipationConfirmedNotification,
    ResponsibleParticipationRequestedNotification,
    EventReminderNotification,
    installed_notification_types,
)
from ephios.extra.mixins import StaffRequiredMixin
from ephios_testplugin.notification import TestNotification


class TestIndexView(StaffRequiredMixin, TemplateView):
    template_name = "testplugin/test_index.html"


class CrashView(StaffRequiredMixin, View):
    def get(self, request):
        raise Exception("This is a test exception")


class TestNotificationForm(forms.Form):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)


class TestNotificationsView(StaffRequiredMixin, FormView):
    form_class = TestNotificationForm
    template_name = "testplugin/test_notifications.html"
    success_url = reverse_lazy("testplugin:test_notifications")

    def form_valid(self, form):
        TestNotification.send(
            self.request.user, form.cleaned_data["title"], form.cleaned_data["body"]
        )
        send_all_notifications()
        messages.success(self.request, "Test notification sent.")
        return super().form_valid(form)


class NotificationTypeForm(forms.Form):
    notification_type = forms.ChoiceField(
        choices=[(t.slug, t.title) for t in installed_notification_types()],
        widget=forms.Select(attrs={"onchange": "this.form.submit()"}),
    )


class EmailTemplateView(StaffRequiredMixin, TemplateView):
    template_name = "testplugin/test_email_template.html"

    def rendered_email_context(self, notification_type):
        data = {
            # some common data for testing various notification types
            "uidb64": urlsafe_base64_encode(force_bytes(self.request.user.id)),
            "token": default_token_generator.make_token(self.request.user),
            "event_id": Event.objects.first().id,
            "participation_id": LocalParticipation.objects.first().id,
            "disposition_url": urljoin(
                settings.GET_SITE_URL(),
                reverse(
                    "core:shift_disposition",
                    kwargs={"pk": LocalParticipation.objects.first().shift.pk},
                ),
            ),
            "email": self.request.user.email,
            "claims": [
                "Start time was changed from 14:00 to 15:00.",
            ],
            "event_title": Event.objects.first().title,
            "content": "Remember to wear sunscreen.",
        }
        try:
            data["consequence_id"] = Consequence.objects.first().id
        except AttributeError:
            pass

        notification = Notification(
            slug=notification_type.slug,
            user=self.request.user,
            data=data,
        )
        try:
            return dict(
                notification_type=notification_type,
                notification_type_class=str(notification_type.__name__),
                subject=notification_type.get_subject(notification),
                email=notification_type.as_html(notification),
                plaintext=notification_type.as_plaintext(notification),
            )
        except Exception as e:
            return {
                "email": f"Error: {e}",
            }

    def get(self, request, *args, **kwargs):
        form = NotificationTypeForm(self.request.GET)
        if form.is_valid():
            notification_type = notification_type_from_slug(
                form.cleaned_data["notification_type"]
            )
            context = super().get_context_data(
                **kwargs,
                form=form,
                **self.rendered_email_context(notification_type),
            )
            if self.request.GET.get("action", "") == "eml":
                return self.as_eml_download(context)
            response = self.render_to_response(context)
            response._csp_exempt = True
            return response
        return super().render_to_response({"form": form})

    def as_eml_download(self, context):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = str(context["subject"])
        msg["From"] = settings.DEFAULT_FROM_EMAIL
        msg["To"] = self.request.user.email
        msg.attach(MIMEText((context["email"]), "html"))
        msg.attach(MIMEText((context["plaintext"]), "plain"))
        buffer = io.StringIO()
        gen = email_generator.Generator(buffer)
        gen.flatten(msg)
        buffer.seek(0)
        response = HttpResponse(buffer.read().encode(), content_type="message/rfc822")
        response["Content-Disposition"] = 'attachment; filename="test.eml"'
        return response
