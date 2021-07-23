
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
