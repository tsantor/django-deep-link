from django.contrib import admin
from django.utils.html import mark_safe

from django_deep_link.models import App, Visit


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "android_app",
        "ios_app",
        "mac_app",
        "windows_app",
        "deep_link",
        "app_store_url",
        "play_store_url",
    )
    list_display_links = (
        "name",
        # "android_package_name",
        # "ios_bundle_id",
    )
    search_fields = (
        "name",
        # "android_package_name",
        # "ios_bundle_id",
    )
    readonly_fields = ("code",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "code",
                    "name",
                    # "default_url",
                ),
            },
        ),
        (
            "iOS Mobile",
            {
                # "classes": ("collapse",),
                "fields": (
                    "ios_url",
                    "ios_app",
                    "ios_uri_scheme",
                    "ios_bundle_id",
                    "ios_custom_url",
                ),
            },
        ),
        (
            "Android Mobile",
            {
                # "classes": ("collapse",),
                "fields": (
                    "android_url",
                    "android_app",
                    "android_uri_scheme",
                    "android_package_name",
                    "android_custom_url",
                ),
            },
        ),
        (
            "Mac Desktop",
            {
                # "classes": ("collapse",),
                "fields": (
                    "mac_app",
                    "mac_uri_scheme",
                    "mac_app_store_url",
                ),
            },
        ),
        (
            "Windows Desktop",
            {
                # "classes": ("collapse",),
                "fields": (
                    "windows_app",
                    "windows_uri_scheme",
                    "windows_app_store_url",
                    "windows_package_name",
                ),
            },
        ),
    )

    def deep_link(self, obj):
        return mark_safe(
            f'<a href="{obj.get_absolute_url()}" target="_blank">Visit</a>'
        )

    def app_store_url(self, obj):
        if obj.get_app_store_url:
            return mark_safe(
                f'<a href="{obj.get_app_store_url()}" target="_blank">Visit</a>'
            )

    def play_store_url(self, obj):
        if obj.get_play_store_url:
            return mark_safe(
                f'<a href="{obj.get_play_store_url()}" target="_blank">Visit</a>'
            )

    class Media:
        js = ("django_deep_link/js/app.js",)


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = (
        "ip_address",
        "deep_link",
        "browser",
        "os",
        "device",
        "platform",
        "created_at",
    )
    readonly_fields = (
        "ip_address",
        "ip_data",
        "ua_data",
        "query_data",
        "deep_link",
    )
    date_hierarchy = "created_at"
    list_filter = ("deep_link__name",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    class Media:
        css = {
            "all": (
                "//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.1.0/styles/default.min.css",
            ),
        }
        js = (
            "//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.1.0/highlight.min.js",
            # "django_deep_link/js/ace-builds/ace.js",
            "django_deep_link/js/scan.js",
        )
