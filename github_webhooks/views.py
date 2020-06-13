from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, "dispatch")
class GitHubWebhookView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"detail": "Ok."})


github_webhook_view = GitHubWebhookView.as_view()
