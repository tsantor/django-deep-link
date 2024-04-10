# Django Deep Link

![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)

<!-- ![Code Style](https://img.shields.io/badge/code_style-ruff-black) -->

## Overview

Simple app to get mobile app deep linking in place with basic tracking.

## Quickstart

Install Django Deep Link::

```bash
python3 -m pip install django-deep-link
```

### Settings

To enable `django_deep_link` in your project you need to add it to `INSTALLED_APPS` in your projects `settings.py` file:

```python
INSTALLED_APPS = (
    ...
    'django_deep_link',
    ...
)
```

Add Django Deep Link's URL patterns:

```python
from django_deep_link import urls as django_deep_link_urls


urlpatterns = [
    ...
    path(r"", include(django_deep_link_urls, namespace='django-deep-link')),
    ...
]
```

## Provide Your Own IP Geodata Handler

```python
import requests
from django.core.cache import cache

def get_ip_geodata(ip_address):
    """Use 3rd party API to obtain Geodata from a given IP."""
    if cache.get(ip_address):
        return cache.get(ip_address)

    params = {}
    r = requests.get(f"https://domain.com/{ip_address}", params=params)
    r.raise_for_status()
    cache.set(ip_address, r.json(), 60*60*24)  # 24 hrs
    return r.json()
```

The IP geodata handler must also be configured in your settings, using the `IP_GEO_HANDLER` setting key. For example:

```python
DEEP_LINK = {
    'IP_GEO_HANDLER': 'my_project.my_app.utils.get_ip_geodata'
}
```

If not specified, the `'IP_GEO_HANDLER'` setting defaults to the geodata provided by Deep Link, which leverages [IP Stack](https://ipstack.com/):

```python
DEEP_LINK = {
    'IP_GEO_HANDLER': 'django_deep_link.helpers.ip.get_ip_geodata'
}
```

## Local Development

```bash
make env
make pip_install
make migrations
make migrate
make superuser
make serve
```

or simply `make from_scratch`

- Visit `http://127.0.0.1:8000/admin/` for the Django Admin

### Testing

```bash
make pytest
make coverage
make open_coverage
```

## Issues

If you experience any issues, please create an [issue](https://bitbucket.org/tsantor/django-deep-link/issues) on Bitbucket.
