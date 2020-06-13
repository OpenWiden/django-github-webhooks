from django.test import Client
from django.urls import reverse


def test_github_webhook_view(client: Client):
    url = reverse("github:receive")
    response = client.post(url)

    assert response.status_code == 200
