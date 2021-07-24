
# Django Deep Link

## Overview
Simple app to get mobile app deep linking in place with basic tracking.

## Documentation

The full documentation is at ...

## Quickstart

Install Django Deep Link::

```bash
pip install django-deep-link
```

Add it to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    'django_deep_link.apps.DjangoDeepLinkConfig',
    ...
)
```

Add Django Deep Link's URL patterns:


```python
from django_deep_link import urls as django_deep_link_urls


urlpatterns = [
    ...
    path(r"", include(django_deep_link_urls)),
    ...
]
```

## Provide Your Own IP Geodata Handler

```
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

    DEEP_LINK = {
        'IP_GEO_HANDLER': 'my_project.my_app.utils.get_ip_geodata'
    }

If not specified, the `'IP_GEO_HANDLER'` setting defaults to the geodata provided by Deep Link, which leverages [IP Stack](https://ipstack.com/):

    DEEP_LINK = {
        'IP_GEO_HANDLER': 'django_deep_link.helpers.ip.get_ip_geodata'
    }

## Features

* TODO

## Running Tests


Does the code actually work?

```bash
source <YOURVIRTUALENV>/bin/activate
(myenv) $ pip install tox
(myenv) $ tox
```


## Development commands

```bash
pip install -r requirements_dev.txt
invoke -l
```
