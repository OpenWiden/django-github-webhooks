from django.urls import path
from .views import github_webhook_view

app_name = "github_webhook"

urlpatterns = [
    path("", github_webhook_view, name="receive"),
]
