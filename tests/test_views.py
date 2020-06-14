import json

from django.http import HttpResponse
from django.test import RequestFactory
from github_webhooks import views, constants


def test_github_webhook_view_success(rf: RequestFactory) -> None:
    headers = {
        constants.Headers.SIGNATURE: "test",
        constants.Headers.EVENT: "test",
    }
    request = rf.post("/fake-url/", **headers)
    response: HttpResponse = views.GitHubWebhookView().post(request)

    assert response.status_code == 200


def test_github_webhook_view_signature_header_is_missing(rf: RequestFactory) -> None:
    request = rf.post("/fake-url/")
    response: HttpResponse = views.GitHubWebhookView().post(request)

    assert response.status_code == 400
    assert json.loads(response.content.decode()) == {"detail": constants.X_HUB_SIGNATURE_HEADER_IS_MISSING}


def test_github_webhook_view_event_header_is_missing(rf: RequestFactory) -> None:
    headers = {constants.Headers.SIGNATURE: "test"}
    request = rf.post("/fake-url/", **headers)
    response: HttpResponse = views.GitHubWebhookView().post(request)

    assert response.status_code == 400
    assert json.loads(response.content.decode()) == {"detail": constants.X_GITHUB_EVENT_HEADER_IS_MISSING}
