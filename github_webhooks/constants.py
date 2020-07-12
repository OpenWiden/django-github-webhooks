import typing as t
from enum import Enum

from django.utils.translation import gettext_lazy as _

X_HUB_SIGNATURE_HEADER_IS_MISSING = _("HTTP_X_HUB_SIGNATURE header is missing.")
X_HUB_SIGNATURE_HEADER_IS_INVALID = _("HTTP_X_HUB_SIGNATURE header is invalid.")
X_GITHUB_EVENT_HEADER_IS_MISSING = _("HTTP_X_GITHUB_EVENT header is missing.")
DIGEST_IS_NOT_SUPPORTED = _("{digest} is not supported digest.")
EVENT_IS_NOT_ALLOWED = _("{event} is not allowed!")

SHA1_DIGEST = "sha1"


class Headers(str, Enum):
    SIGNATURE = "HTTP_X_HUB_SIGNATURE"
    EVENT = "HTTP_X_GITHUB_EVENT"


class Events(str, Enum):
    CHECK_RUN = "check_run"
    CHECK_SUITE = "check_suite"
    COMMIT_COMMENT = "commit_comment"
    CONTENT_REFERENCE = "content_reference"
    CREATE = "create"
    DELETE = "delete"
    DEPLOY_KEY = "deploy_key"
    DEPLOYMENT = "deployment"
    DEPLOYMENT_STATUS = "deployment_status"
    FORK = "fork"
    GITHUB_APP_AUTHORIZATION = "github_app_authorization"
    GOLLUM = "gollum"
    INSTALLATION = "installation"
    INSTALLATION_REPOSITORIES = "installation_repositories"
    ISSUE_COMMENT = "issue_comment"
    ISSUES = "issues"
    LABEL = "label"
    MARKETPLACE_PURCHASE = "marketplace_purchase"
    MEMBER = "member"
    MEMBERSHIP = "membership"
    META = "meta"
    MILESTONE = "milestone"
    ORGANIZATION = "organization"
    ORG_BLOCK = "org_block"
    PACKAGE = "package"
    PAGE_BUILD = "page_build"
    PING = "ping"
    PROJECT_CARD = "project_card"
    PROJECT_COLUMN = "project_column"
    PROJECT = "project"
    PUBLIC = "public"
    PULL_REQUEST = "pull_request"
    PULL_REQUEST_REVIEW = "pull_request_review"
    PULL_REQUEST_REVIEW_COMMENT = "pull_request_review_comment"
    PUSH = "push"
    RELEASE = "release"
    REPOSITORY_DISPATCH = "repository_dispatch"
    REPOSITORY = "repository"
    REPOSITORY_IMPORT = "repository_import"
    REPOSITORY_VULNERABILITY_ALERT = "repository_vulnerability_alert"
    SECURITY_ADVISORY = "security_advisory"
    SPONSORSHIP = "sponsorship"
    STAR = "star"
    STATUS = "status"
    TEAM = "team"
    TEAM_ADD = "team_add"
    WATCH = "watch"

    @classmethod
    def values(cls) -> t.List[str]:
        return [event.value for event in cls]
