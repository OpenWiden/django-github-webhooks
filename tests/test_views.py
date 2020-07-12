import json
from unittest import mock

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import RequestFactory

from github_webhooks import constants, signals, views


class TestGitHubWebhookView:
    def test_signature_header_is_missing(self, rf: RequestFactory):
        request = rf.post("/fake-url/")
        response: HttpResponse = views.GitHubWebhookView().post(request)

        assert response.status_code == 400
        assert json.loads(response.content.decode()) == {
            "detail": constants.X_HUB_SIGNATURE_HEADER_IS_MISSING
        }

    def test_event_header_is_missing(self, rf: RequestFactory):
        headers = {
            constants.Headers.SIGNATURE: "{digest}=12345".format(
                digest=constants.SHA1_DIGEST
            )
        }
        request = rf.post("/fake-url/", **headers)
        response: HttpResponse = views.GitHubWebhookView().post(request)

        assert response.status_code == 400
        assert json.loads(response.content.decode()) == {
            "detail": constants.X_GITHUB_EVENT_HEADER_IS_MISSING
        }

    def test_signature_header_is_invalid_split(self, rf: RequestFactory):
        headers = {
            constants.Headers.SIGNATURE: "invalid_header",
            constants.Headers.EVENT: "test",
        }
        request = rf.post("/fake-url/", **headers)
        response: HttpResponse = views.GitHubWebhookView().post(request)

        assert response.status_code == 400
        assert json.loads(response.content.decode()) == {
            "detail": constants.X_HUB_SIGNATURE_HEADER_IS_INVALID
        }

    def test_digest_is_not_supported(self, rf: RequestFactory):
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

    def test_signature_value_is_invalid(self, rf: RequestFactory, settings):
        settings.DJANGO_GITHUB_WEBHOOKS = {"SECRET": "6789"}
        headers = {
            constants.Headers.SIGNATURE: "{digest}=12345".format(
                digest=constants.SHA1_DIGEST
            ),
            constants.Headers.EVENT: "test",
        }
        request = rf.post("/fake-url/", **headers)
        response: HttpResponse = views.GitHubWebhookView().post(request)

        assert response.status_code == 400
        assert json.loads(response.content.decode()) == {
            "detail": constants.X_HUB_SIGNATURE_HEADER_IS_INVALID
        }

    def test_get_secret_improperly_configured(self, settings):
        settings.DJANGO_GITHUB_WEBHOOKS = {}
        with pytest.raises(ImproperlyConfigured):
            views.GitHubWebhookView().get_secret()

    @pytest.mark.parametrize(
        "config, expected_is_allowed", [
            pytest.param({"SECRET": "12345", "ALLOWED_EVENTS": []}, False),
            pytest.param(
                {"SECRET": "12345", "ALLOWED_EVENTS": [constants.Events.ISSUES]}, True
            ),
        ],
    )
    def test_event_is_allowed_method(
        self, rf: RequestFactory, settings, config: dict, expected_is_allowed: bool
    ):
        settings.DJANGO_GITHUB_WEBHOOKS = config
        headers = {constants.Headers.EVENT: constants.Events.ISSUES}
        request = rf.post("/fake-url/", **headers)
        view = views.GitHubWebhookView(request=request)
        assert view.event_is_allowed() == (expected_is_allowed, constants.Events.ISSUES)

    @pytest.mark.parametrize("event", constants.Events.values())
    def test_get_signal_method(self, event):
        signal = getattr(signals, "{event}".format(event=event))
        assert views.GitHubWebhookView.get_signal(event) == signal

    @pytest.mark.parametrize("config, expected_status_code, expected_response", [
        pytest.param(
            {"SECRET": "12345", "ALLOWED_EVENTS": []},
            400,
            {
                "detail": constants.EVENT_IS_NOT_ALLOWED.format(
                    event=constants.Events.ISSUES
                )
            },
            id="event is not allowed",
        ),
        pytest.param(
            {"SECRET": "12345", "ALLOWED_EVENTS": [constants.Events.ISSUES]},
            200,
            {"detail": "Ok"},
            id="event is allowed",
        ),
    ])
    @mock.patch.object(views.utils, "compare_signatures")
    def test_event_not_allowed(
        self,
        patched_compare_signatures,
        rf: RequestFactory,
        settings,
        config: dict,
        expected_status_code: int,
        expected_response: dict,
    ):
        settings.DJANGO_GITHUB_WEBHOOKS = config
        patched_compare_signatures.return_value = True
        headers = {
            constants.Headers.SIGNATURE: "{digest}=12345".format(
                digest=constants.SHA1_DIGEST
            ),
            constants.Headers.EVENT: constants.Events.ISSUES,
        }
        request = rf.post("/fake-url/", **headers)
        request._body = '{"test": "ok"}'.encode()
        view = views.GitHubWebhookView(request=request)
        response = view.post(request)

        assert response.status_code == expected_status_code
        assert json.loads(response.content.decode()) == expected_response
