from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class JobState(str, Enum):
    DISCOVERED = "DISCOVERED"
    WAIT_INPUT = "WAIT_INPUT"
    VALIDATED = "VALIDATED"
    CLAIMED = "CLAIMED"
    REVIEW_RUNNING = "REVIEW_RUNNING"
    RESULT_SAVED = "RESULT_SAVED"
    UPLOAD_PENDING = "UPLOAD_PENDING"
    COMPLETED = "COMPLETED"
    AUTH_REQUIRED = "AUTH_REQUIRED"
    CONFLICT = "CONFLICT"
    FAILED = "FAILED"
    REVIEW_UNCERTAIN = "REVIEW_UNCERTAIN"
    REJECTED = "REJECTED"


class ValidationOutcome(str, Enum):
    VALIDATED = "VALIDATED"
    WAIT_INPUT = "WAIT_INPUT"
    CONFLICT = "CONFLICT"
    REJECTED = "REJECTED"
    DUPLICATE = "DUPLICATE"
    IN_PROGRESS = "IN_PROGRESS"


@dataclass
class ValidationResult:
    outcome: ValidationOutcome
    reason: str
    processing_key: str | None = None
    request_id: str | None = None
    request_revision: str | None = None
    package_sha256: str | None = None
    package_path: str | None = None
    fields: dict[str, Any] = field(default_factory=dict)
    needs_package_download: bool = False


@dataclass
class ReviewResult:
    ok: bool
    output_text: str
    output_format: str
    exit_code: int
    model_calls: int
    usage: dict[str, Any] | None
    error: str | None = None
    # Claude plan usage limit (the 5-hour / weekly window). "BEFORE_START": the CLI refused before any model work
    # (no turns, no cost) so the review may be retried later; "DURING": work had started, outcome unknown.
    usage_limit: str | None = None
    retry_after_sec: int | None = None


@dataclass
class JobRecord:
    processing_key: str
    request_id: str
    request_revision: str
    package_sha256: str
    state: JobState
    created_at: str
    updated_at: str
    attempt_count: int
    last_error: str | None = None
    result_path: str | None = None
