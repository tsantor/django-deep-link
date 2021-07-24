from django.views.generic import DetailView
from ipware import get_client_ip
from user_agents import parse

from .helpers.ua import get_ua_info, get_ua_summary
from .models import AppStore, Visit
from .settings import api_settings


class AppDownloadView(DetailView):
    """
    Shows an app download page if app not installed or redirects to the
    installed app if it is.
    """

    model = AppStore
    template_name = "django_deep_link/app.html"

    def get_object(self, queryset=None):
        return AppStore.objects.get(code=self.kwargs.get("code"))

    def get_context_data(self, **kwargs):
        # Get user agent data
        ua_string = self.request.META.get("HTTP_USER_AGENT", None)
        user_agent = parse(ua_string)
        ua_data = get_ua_info(ua_string) if ua_string else {}

        # Get ip address data
        ip_address, _ = get_client_ip(self.request)
        if ip_address:
            return ip_address

        get_ip_address_information = api_settings.IP_LOOKUP_HANDLER
        ip_data = get_ip_address_information(ip_address)
        if ip_address:
            Visit.objects.create(
                ip_address=ip_address,
                ua_data=ua_data,
                ip_data=ip_data,
                deep_link=self.object,
            )

        ctx = super().get_context_data(**kwargs)
        ctx["user_agent"] = user_agent
        ctx.update(get_ua_summary(user_agent))
        return ctx
