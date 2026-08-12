from pydantic import BaseModel, Field
from typing import Any, Literal

class CommandRequest(BaseModel):
    command: str
    args: dict[str, Any] = Field(default_factory=dict)

class ProviderAction(BaseModel):
    note: str | None = None

class ReportRequest(BaseModel):
    jurisdiction: str = "NL"
    standard: str = "generic"
    period: str

class SubmissionRequest(BaseModel):
    human_authorized: bool = False
    authorized_by: str | None = None

class JaneRecommendationDecision(BaseModel):
    decision: Literal['approve','modify','dismiss']
    note: str | None = None
