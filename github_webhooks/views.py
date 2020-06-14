from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . import constants


@method_decorator(csrf_exempt, "dispatch")
class GitHubWebhookView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        if request.META.get(constants.Headers.SIGNATURE) is None:
            return JsonResponse({"detail": constants.X_HUB_SIGNATURE_HEADER_IS_MISSING}, status=400)
        elif request.META.get(constants.Headers.EVENT) is None:
            return JsonResponse({"detail": constants.X_GITHUB_EVENT_HEADER_IS_MISSING}, status=400)
        else:
            return JsonResponse({"detail": "Ok"})


github_webhook_view = GitHubWebhookView.as_view()
