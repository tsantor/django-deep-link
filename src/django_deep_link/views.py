from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from user_agents import parse

from .helpers.ip import get_ip, get_ip_info
from .helpers.ua import get_platform_bools, get_ua, get_ua_info
from .helpers.url import get_querystring_as_dict
from .models import App, Visit


class AppDownloadView(DetailView):
    """
    Shows an app download page if app not installed or redirects to the
    installed app if it is.
    """

    model = App
    template_name = "django_deep_link/app.html"

    def get_object(self, queryset=None):
        # return App.objects.get(code=self.kwargs.get("code"))
        return get_object_or_404(self.model, code=self.kwargs.get("code"))

    def get_context_data(self, **kwargs):

        ip = get_ip(self.request)
        user_agent = get_ua(self.request)

        Visit.objects.create(
            ip_address=ip,
            ua_data=get_ua_info(user_agent),
            ip_data=get_ip_info(ip),
            query_data=get_querystring_as_dict(self.request),
            deep_link=self.object,
        )

        user_agent = parse(user_agent)
        ctx = super().get_context_data(**kwargs)
        ctx["user_agent"] = user_agent
        ctx.update(get_platform_bools(user_agent))
        return ctx
