=====
Usage
=====

To use Django Deep Link in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_deep_link.apps.DjangoDeepLinkConfig',
        ...
    )

Add Django Deep Link's URL patterns:

.. code-block:: python

    from django_deep_link import urls as django_deep_link_urls


    urlpatterns = [
        ...
        url(r'^', include(django_deep_link_urls)),
        ...
    ]
