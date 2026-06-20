import asyncio
from collections import Counter
from typing import List, Dict
from app.models import ChatRequest, EvaluationRecord, EvaluationSummary
from app.conversation import generate_response
from app.feedback import FeedbackLoop
from app.logger import log_event


def generate_mock_queries(total: int = 10000) -> List[ChatRequest]:
    base_queries = [
        "Explain why the model should prefer explicit logic over heuristics.",
        "Summarize the system behavior in one concise paragraph.",
        "Identify the bug in this workflow and suggest a fix.",
        "How would you justify the recommended route for this decision?",
        "Provide a brief answer to this user query.",
        "What is the root cause of the failure in the example?",
    ]
    queries = []
    for idx in range(total):
        prompt = base_queries[idx % len(base_queries)]
        if idx % 5 == 0:
            prompt = f"{prompt} Use a formal tone and keep it tight."
        if idx % 7 == 0:
            prompt = f"{prompt} Do not be verbose."
        queries.append(ChatRequest(query=prompt, context="Session context placeholder."))
    return queries


def evaluate_single(chat_request: ChatRequest) -> EvaluationRecord:
    response = generate_response(chat_request.query, chat_request.context)
    issues = []

    reasoning_pass = True
    if "requires_reasoning" in response.tags and "because" not in response.reasoning.lower():
        issues.append("missing_reasoning_clarity")
        reasoning_pass = False

    style_pass = response.style_score >= 0.80
    if not style_pass:
        issues.append("style_score_below_threshold")

    if response.latency_ms > 800:
        issues.append("latency_exceeded")

    predicted_quality = round(
        (1.0 if reasoning_pass else 0.0) * 0.5 + (response.style_score * 0.5),
        4,
    )

    return EvaluationRecord(
        query=chat_request.query,
        response=response.response,
        reasoning_pass=reasoning_pass,
        style_pass=style_pass,
        issue_codes=issues,
        predicted_quality=predicted_quality,
        latency_ms=response.latency_ms,
    )


async def evaluate_batch(queries: List[ChatRequest]) -> EvaluationSummary:
    log_event(f"Starting batch evaluation for {len(queries)} queries")
    records = []
    failures = Counter()
    total_latency = 0.0

    async def task(req: ChatRequest):
        nonlocal total_latency
        record = evaluate_single(req)
        records.append(record)
        total_latency += record.latency_ms
        for code in record.issue_codes:
            failures[code] += 1

    await asyncio.gather(*(task(query) for query in queries))
    passed = sum(1 for record in records if record.reasoning_pass and record.style_pass)
    failed = len(records) - passed
    accuracy = round(passed / len(records) * 100.0, 2) if records else 0.0
    average_latency_ms = round(total_latency / len(records), 2) if records else 0.0

    feedback = FeedbackLoop()
    refinement = feedback.suggest_refinement(failures)

    summary = EvaluationSummary(
        total_queries=len(records),
        passed=passed,
        failed=failed,
        accuracy=accuracy,
        average_latency_ms=average_latency_ms,
        failures_by_code=dict(failures),
        prompt_refinement=refinement,
    )
    log_event("Batch evaluation completed", {"summary": summary.model_dump()})
    return summary
