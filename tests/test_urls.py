from django.urls import reverse, resolve


def test_receive_url():
    assert reverse("github-webhook:receive") == "/github/webhook/receive/"
    assert resolve("/github/webhook/receive/").view_name == "github-webhook:receive"
