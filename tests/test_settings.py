import pytest
from django.core.exceptions import ImproperlyConfigured

from github_webhooks import settings as github_webhook_settings, constants


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


def test_allowed_events_defaults_set(settings) -> None:
    assert (
        settings.DJANGO_GITHUB_WEBHOOKS["ALLOWED_EVENTS"] == constants.Events.values()
    )
