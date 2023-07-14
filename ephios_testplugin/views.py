from django import forms
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView

from ephios.core.services.notifications.backends import send_all_notifications
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
        TestNotification.send(self.request.user, form.cleaned_data["title"], form.cleaned_data["body"])
        send_all_notifications()
        messages.success(self.request, "Test notification sent.")
        return super().form_valid(form)
