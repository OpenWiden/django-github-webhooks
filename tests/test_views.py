import json

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import RequestFactory
from github_webhooks import views, constants


class TestGitHubWebhookView:
    def test_signature_header_is_missing(self, rf: RequestFactory) -> None:
        request = rf.post("/fake-url/")
        response: HttpResponse = views.GitHubWebhookView().post(request)

        assert response.status_code == 400
        assert json.loads(response.content.decode()) == {"detail": constants.X_HUB_SIGNATURE_HEADER_IS_MISSING}

    def test_event_header_is_missing(self, rf: RequestFactory) -> None:
        headers = {constants.Headers.SIGNATURE: "{digest}=12345".format(digest=constants.SHA1_DIGEST)}
        request = rf.post("/fake-url/", **headers)
        response: HttpResponse = views.GitHubWebhookView().post(request)

        assert response.status_code == 400
        assert json.loads(response.content.decode()) == {"detail": constants.X_GITHUB_EVENT_HEADER_IS_MISSING}

    def test_signature_header_is_invalid_split(self, rf: RequestFactory) -> None:
        headers = {constants.Headers.SIGNATURE: "invalid_header", constants.Headers.EVENT: "test"}
        request = rf.post("/fake-url/", **headers)
        response: HttpResponse = views.GitHubWebhookView().post(request)

        assert response.status_code == 400
        assert json.loads(response.content.decode()) == {"detail": constants.X_HUB_SIGNATURE_HEADER_IS_INVALID}

    def test_digest_is_not_supported(self, rf: RequestFactory) -> None:
        digest = "not_supported_digest"
        headers = {
            constants.Headers.SIGNATURE: "{digest}=12345".format(digest=digest),
            constants.Headers.EVENT: "test",
        }
        request = rf.post("/fake-url/", **headers)
        response: HttpResponse = views.GitHubWebhookView().post(request)

        assert response.status_code == 400
        assert json.loads(response.content.decode()) == {
            "detail": constants.DIGEST_IS_NOT_SUPPORTED.format(digest=digest)
        }

    def test_signature_value_is_invalid(self, rf: RequestFactory, settings) -> None:
        settings.DJANGO_GITHUB_WEBHOOKS = {"SECRET": "6789"}
        headers = {
            constants.Headers.SIGNATURE: "{digest}=12345".format(digest=constants.SHA1_DIGEST),
            constants.Headers.EVENT: "test",
        }
        request = rf.post("/fake-url/", **headers)
        response: HttpResponse = views.GitHubWebhookView().post(request)

        assert response.status_code == 400
        assert json.loads(response.content.decode()) == {"detail": constants.X_HUB_SIGNATURE_HEADER_IS_INVALID}

    def test_get_secret_improperly_configured(self, settings) -> None:
        settings.DJANGO_GITHUB_WEBHOOKS = {}
        with pytest.raises(ImproperlyConfigured):
            views.GitHubWebhookView().get_secret()
