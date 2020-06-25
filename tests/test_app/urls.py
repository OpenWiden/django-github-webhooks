from django.urls import include, path

from github_webhooks import urls

urlpatterns = [
    path(
        "github/webhook/receive/",
        include(urls, namespace="github-webhook"),
        name="receive",
    ),
]
