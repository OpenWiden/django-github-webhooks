from enum import Enum

from django.utils.translation import gettext_lazy as _

X_HUB_SIGNATURE_HEADER_IS_MISSING = _("HTTP_X_HUB_SIGNATURE header is missing.")
X_GITHUB_EVENT_HEADER_IS_MISSING = _("HTTP_X_GITHUB_EVENT header is missing.")


class Headers(str, Enum):
    SIGNATURE = "HTTP_X_HUB_SIGNATURE"
    EVENT = "HTTP_X_GITHUB_EVENT"
