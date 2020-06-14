from github_webhooks import constants


def test_events_values() -> None:
    assert constants.Events.values() == ["issues"]
