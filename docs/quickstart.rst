Quickstart
===========

Add URL patterns:

.. code-block:: python

    from github_webhooks import urls as github_webhooks_urls


    urlpatterns = [
        ...
        url("webhooks/github/receive/", include(github_webhooks_urls)),
        ...
    ]
