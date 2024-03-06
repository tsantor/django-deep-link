from django.contrib import admin
from django.urls import include, path

admin.site.enable_nav_sidebar = False

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django_deep_link.urls", namespace="django_deep_link")),
]
