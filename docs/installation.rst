Installation
============

Install via pip:

.. code-block:: console

    $ pip install django-github-webhooks


Add app to `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        "github_webhooks",
        ...
    )


Add `SECRET` for `DJANGO_GITHUB_WEBHOOKS` in settings:

.. code-block:: python

    DJANGO_GITHUB_WEBHOOKS = {
        "SECRET": "secret-key"
    }

Add URL patterns:

.. code-block:: python

    from github_webhooks import urls as github_webhooks_urls


    urlpatterns = [
        ...
        url("webhooks/github/receive/", include(github_webhooks_urls)),
        ...
    ]
