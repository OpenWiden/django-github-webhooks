from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings, ImproperlyConfigured

from . import constants, utils


@method_decorator(csrf_exempt, "dispatch")
class GitHubWebhookView(View):
    def get_secret(self) -> str:
        """
        Returns webhook's secret key.
        """
        secret = settings.DJANGO_GITHUB_WEBHOOKS.get("SECRET")
        if secret is None:
            raise ImproperlyConfigured("SECRET key for DJANGO_GITHUB_WEBHOOKS is not specified!")
        else:
            return secret

    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Handles GitHub webhook income request.
        """
        if request.META.get(constants.Headers.SIGNATURE) is None:
            return JsonResponse({"detail": constants.X_HUB_SIGNATURE_HEADER_IS_MISSING}, status=400)
        elif request.META.get(constants.Headers.EVENT) is None:
            return JsonResponse({"detail": constants.X_GITHUB_EVENT_HEADER_IS_MISSING}, status=400)
        else:
            # Try to split signature header into digest and signature value
            try:
                digest, signature = request.META[constants.Headers.SIGNATURE].split("=")
            except ValueError:
                return JsonResponse({"detail": constants.X_HUB_SIGNATURE_HEADER_IS_INVALID}, status=400)

            # Check digest type
            if digest != constants.SHA1_DIGEST:
                return JsonResponse({"detail": constants.DIGEST_IS_NOT_SUPPORTED.format(digest=digest)}, status=400)

            # Validate signature value
            if utils.compare_signatures(signature, self.get_secret(), request.body) is False:
                return JsonResponse({"detail": constants.X_HUB_SIGNATURE_HEADER_IS_INVALID}, status=400)

            return JsonResponse({"detail": "Ok"})


github_webhook_view = GitHubWebhookView.as_view()
