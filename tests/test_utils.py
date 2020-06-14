import hashlib
import hmac

from github_webhooks import utils


class TestCompareSignatures:
    def test_true(self) -> None:
        secret = "12345"
        message = "test".encode()
        signature = hmac.new(secret.encode(), message, hashlib.sha1).hexdigest()
        utils.compare_signatures(signature, secret, message)

    def test_false(self) -> None:
        secret = "12345"
        message = "test".encode()
        signature = hmac.new(secret.encode(), message, hashlib.sha1).hexdigest()
        utils.compare_signatures(signature, "fail_secret", message)
