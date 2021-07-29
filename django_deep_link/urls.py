from django.urls import path
from .views import AppDownloadView

app_name = "django_deep_link"

urlpatterns = [
    path("<uuid:code>/", AppDownloadView.as_view(), name="deep-link"),
]
