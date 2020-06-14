=============
Configuration
=============

Minimal configuration
---------------------

.. code-block:: python

     DJANGO_GITHUB_WEBHOOKS = {
        "SECRET": "secret-key"
     }

SECRET
------

Required: True

GitHub docs: https://developer.github.com/webhooks/creating/#secret

Setting a webhook secret allows you to ensure that `POST` requests sent to the payload URL are from GitHub. When you set a `SECRET`, you'll receive the `X-Hub-Signature` header in the webhook `POST` request.

You can also extend webhook view from `github_webhooks.views.GitHubWebhookView` to override `get_secret` method. More about that in :ref:`advanced_user_guide:Secret key customization`.

ALLOWED_EVENTS
--------------

Required: False

Default:

.. code-block:: python

    DJANGO_GITHUB_WEBHOOKS = {
        ...
        "ALLOWED_EVENTS": [
            "issues",
        ],
        ...
    }

GitHub docs: https://developer.github.com/webhooks/event-payloads/

ALLOWED_EVENTS is a list of all allowed events, that you want to handle.
