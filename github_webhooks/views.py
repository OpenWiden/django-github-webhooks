import json
import typing as t

from django.conf import ImproperlyConfigured, settings
from django.dispatch import Signal
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from . import constants, signals, utils


@method_decorator(csrf_exempt, "dispatch")
class GitHubWebhookView(View):
    def get_secret(self) -> str:
        """
        Returns webhook's secret key.
        """
        secret = settings.DJANGO_GITHUB_WEBHOOKS.get("SECRET")
        if secret is None:
            raise ImproperlyConfigured(
                "SECRET key for DJANGO_GITHUB_WEBHOOKS is not specified!"
            )
        else:
            return secret

    def event_is_allowed(self) -> t.Tuple[bool, constants.Events]:
        """
        Validates that event is allowed.
        """
        event = self.request.META[constants.Headers.EVENT]
        return event in settings.DJANGO_GITHUB_WEBHOOKS["ALLOWED_EVENTS"], event

    @classmethod
    def get_signal(cls, event: constants.Events) -> Signal:
        return getattr(signals, event)

    def post(self, request: HttpRequest, **kwargs) -> JsonResponse:
        """
        Handles GitHub webhook income request.
        """
        if request.META.get(constants.Headers.SIGNATURE) is None:
            return JsonResponse(
                {"detail": constants.X_HUB_SIGNATURE_HEADER_IS_MISSING}, status=400
            )
        elif request.META.get(constants.Headers.EVENT) is None:
            return JsonResponse(
                {"detail": constants.X_GITHUB_EVENT_HEADER_IS_MISSING}, status=400
            )
        else:
            # Try to split signature header into digest and signature value
            try:
                digest, signature = request.META[constants.Headers.SIGNATURE].split("=")
            except ValueError:
                return JsonResponse(
                    {"detail": constants.X_HUB_SIGNATURE_HEADER_IS_INVALID}, status=400
                )

            # Check digest type
            if digest != constants.SHA1_DIGEST:
                return JsonResponse(
                    {"detail": constants.DIGEST_IS_NOT_SUPPORTED.format(digest=digest)},
                    status=400,
                )

            # Validate signature value
            if (
                utils.compare_signatures(signature, self.get_secret(), request.body)
                is False
            ):
                return JsonResponse(
                    {"detail": constants.X_HUB_SIGNATURE_HEADER_IS_INVALID}, status=400
                )

            # Validate that event is allowed
            is_allowed, event = self.event_is_allowed()
            if is_allowed is False:
                return JsonResponse(
                    {"detail": constants.EVENT_IS_NOT_ALLOWED.format(event=event)},
                    status=400,
                )

            # Send signal on success event
            signal = self.get_signal(event)
            signal.send(sender=self.__class__, payload=json.loads(request.body))

            return JsonResponse({"detail": "Ok"})


github_webhook_view = GitHubWebhookView.as_view()
