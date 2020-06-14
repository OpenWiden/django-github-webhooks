from django.conf import settings as django_settings, ImproperlyConfigured
from github_webhooks import constants


def load_settings() -> None:
    try:
        settings = django_settings.DJANGO_GITHUB_WEBHOOKS
    except AttributeError:
        raise ImproperlyConfigured("DJANGO_GITHUB_WEBHOOKS settings is missing!")

    if not isinstance(settings, dict):
        raise ImproperlyConfigured("DJANGO_GITHUB_WEBHOOKS is not a dict!")

    if "ALLOWED_EVENTS" not in settings:
        settings["ALLOWED_EVENTS"] = constants.Events.values()
