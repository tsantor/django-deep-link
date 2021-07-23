from django.contrib import admin
from django.utils.html import mark_safe

from django_deep_link.models import AppStore, Visit


@admin.register(AppStore)
class AppStoreAdmin(admin.ModelAdmin):
    list_display = (
        "android_package_name",
        "apple_app_id",
        "deep_link",
        "app_store_url",
        "play_store_url",
    )
    list_display_links = (
        "android_package_name",
        "apple_app_id",
    )
    # search_fields = (
    #     "android_package_name",
    #     "apple_app_id",
    # )
    readonly_fields = ("code",)

    fieldsets = (
        (
            None,
            {
                "fields": ("code",),
            },
        ),
        (
            "iOS",
            {
                # "classes": ("collapse",),
                "fields": ("apple_app_id",),
            },
        ),
        (
            "Android",
            {
                # "classes": ("collapse",),
                "fields": ("android_package_name",),
            },
        ),
    )

    # def has_add_permission(self, request):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def deep_link(self, obj):
        return mark_safe(
            f'<a href="{obj.get_absolute_url()}" target="_blank">Visit</a>'
        )

    deep_link.short_description = "Deep link"

    def app_store_url(self, obj):
        if obj.app_store_url:
            return mark_safe(f'<a href="{obj.app_store_url}" target="_blank">Visit</a>')

    def play_store_url(self, obj):
        if obj.play_store_url:
            return mark_safe(f'<a href="{obj.play_store_url}" target="_blank">Visit</a>')



@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = (
        "ip_address",
        # "qr_code",
        "browser",
        "os",
        "device",
        "platform",
        "created",
    )
    readonly_fields = (
        "ip_address",
        "ip_data",
        "ua_data",
        # "qr_code",
    )
    date_hierarchy = "created"
    list_filter = (
        # "qr_code__event__company",
        # "qr_code",
    )

    def has_add_permission(self, request):
        # You can't add scans manually
        return False

    def has_change_permission(self, request, obj=None):
        # You can't edit scans
        return False

    class Media:
        css = {
            "all": (
                "//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.1.0/styles/default.min.css",
            ),
        }
        js = (
            "//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.1.0/highlight.min.js",
            "django_deep_link/js/ace-builds/ace.js",
            "django_deep_link/js/django_deep_links.js",
        )
