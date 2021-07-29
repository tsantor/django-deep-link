from django.urls import path
from .views import AppDownloadView

app_name = "django-deep-link"

urlpatterns = [
    path("<uuid:code>/", AppDownloadView.as_view(), name="deep-link"),
]
