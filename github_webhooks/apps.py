from django.apps import AppConfig


class GitHubWebhooksApp(AppConfig):
    name = "github_webhooks"

    def ready(self):
        from . import settings
        settings.load_settings()
