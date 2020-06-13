from django.urls import path, include
from github_webhooks import urls

urlpatterns = [
    path("github/", include(urls, namespace="github")),
]
