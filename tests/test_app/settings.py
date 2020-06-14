SECRET_KEY = "fake-key"
ROOT_URLCONF = "tests.test_app.urls"
INSTALLED_APPS = (
    "github_webhooks",
)
DJANGO_GITHUB_WEBHOOKS = {
    "SECRET": "12345"
}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}
