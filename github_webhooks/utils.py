import hashlib
import hmac


def compare_signatures(signature: str, secret: str, message: bytes) -> bool:
    generated = hmac.new(secret.encode("utf-8"), message, hashlib.sha1)
    return hmac.compare_digest(generated.hexdigest(), signature)
