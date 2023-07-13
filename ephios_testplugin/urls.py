from django.urls import path
from django.views import View


class CrashView(View):
    def get(self, request):
        raise Exception("This is a test exception")


app_name = "testplugin"
urlpatterns = [
    path("crash/", CrashView.as_view(), name="test_crash"),
]
