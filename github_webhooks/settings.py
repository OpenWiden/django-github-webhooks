from django.conf import settings as django_settings, ImproperlyConfigured


def load_settings() -> None:
    try:
        settings = django_settings.DJANGO_GITHUB_WEBHOOKS
    except AttributeError:
        raise ImproperlyConfigured("DJANGO_GITHUB_WEBHOOKS settings is missing!")

    if not isinstance(settings, dict):
        raise ImproperlyConfigured("DJANGO_GITHUB_WEBHOOKS is not a dict!")
