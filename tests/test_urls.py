from django.urls import resolve, reverse


def test_receive_url():
    assert reverse("github-webhook:receive") == "/github/webhook/receive/"
    assert resolve("/github/webhook/receive/").view_name == "github-webhook:receive"
