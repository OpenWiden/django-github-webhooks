Advanced User Guide
===================

Secret key customization
------------------------

You don't have to configure anything, except base setting, but if you want to store webhook secret key in the DB, or you have several webhooks, then you may need your own secret key retrieve implementation.

By default, secret key is obtained from `DJANGO_GITHUB_WEBHOOKS` settings, or rather, it happens in a view method, called `get_secret`.

.. code-block:: python

    class GitHubWebhookView(View):
        def get_secret(self) -> str:
            """
            Returns webhook's secret key.
            """
            secret = settings.DJANGO_GITHUB_WEBHOOKS.get("SECRET")
            if secret is None:
                raise ImproperlyConfigured("SECRET key for DJANGO_GITHUB_WEBHOOKS is not specified!")
            else:
                return secret


For example, we want to handle multiple webhooks and retrieve secret key from DB by webhook id.

First of all, we need a model:

.. code-block:: python

    from django.db import models


    class Webhook(models.Model):
        id = models.PositiveIntegerField(primary_key=True)
        secret = models.CharField(max_length=40)

Then, we need to override `github_webhooks.views.GitHubWebhookView`:

.. code-block:: python

    from github_webhooks.views import GitHubWebhookView
    from .models import Webhook


    class CustomWebhookView(GitHubWebhookView):
        def get_secret(self) -> str:
            return Webhook.objects.get(id=self.kwargs["id"]).secret

And also we need to override URLS:

.. code-block:: python

    from django.urls import path
    from .views import CustomWebhookView

    urlpatterns = [
        path("github/webhook/<int:id>/receive/", CustomWebhookView, name="github-webhook-receive"),
    ]

That's it!
