from django.test import RequestFactory
from github_webhooks import views


def test_github_webhook_view(rf: RequestFactory):
    request = rf.post("/fake-url/")
    response = views.GitHubWebhookView().post(request)

    assert response.status_code == 200
