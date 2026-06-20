from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class ChatRequest(BaseModel):
    query: str
    context: Optional[str] = None
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    reasoning: str
    style_score: float
    latency_ms: float
    tags: List[str]
    metadata: Dict[str, Any]


class EvaluationRecord(BaseModel):
    query: str
    response: str
    reasoning_pass: bool
    style_pass: bool
    issue_codes: List[str]
    predicted_quality: float
    latency_ms: float


class EvaluationSummary(BaseModel):
    total_queries: int
    passed: int
    failed: int
    accuracy: float
    average_latency_ms: float
    failures_by_code: Dict[str, int]
    prompt_refinement: str


class FeedbackAdvice(BaseModel):
    issue_type: str
    recommendation: str
    target_improvement: str
