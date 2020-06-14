import pytest
from django.core.exceptions import ImproperlyConfigured

from github_webhooks import settings as github_webhook_settings


def test_load_settings_success() -> None:
    github_webhook_settings.load_settings()


def test_missed_github_webhooks_settings(settings) -> None:
    del settings.DJANGO_GITHUB_WEBHOOKS
    with pytest.raises(ImproperlyConfigured):
        github_webhook_settings.load_settings()


def test_github_webhooks_settings_is_not_a_dict(settings) -> None:
    settings.DJANGO_GITHUB_WEBHOOKS = list()
    with pytest.raises(ImproperlyConfigured):
        github_webhook_settings.load_settings()
