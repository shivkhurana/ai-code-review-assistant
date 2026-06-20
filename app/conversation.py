import time
from typing import Optional, List
from app.models import ChatResponse


PROMPT_TEMPLATE = (
    "You are a concise autonomous assistant. Always answer in 1-3 sentences. "
    "If the user asks for reasoning, give a numbered or structured justification. "
    "Avoid hallucinations, state uncertainty clearly, and follow strict style standards."
)


REASONING_CUES = {"why", "how", "explain", "reason", "justify", "because"}
STYLE_SCORE_WEIGHTS = {
    "length": 0.3,
    "clarity": 0.3,
    "structure": 0.2,
    "tone": 0.2,
}


def compute_style_score(response: str, reasoning: str, tags: List[str]) -> float:
    score = 1.0
    if len(response.split()) > 45:
        score -= 0.15
    if "because" not in reasoning.lower() and any(cue in response.lower() for cue in REASONING_CUES):
        score -= 0.2
    if "I" in response and "I think" in response:
        score -= 0.1
    if "please" in response.lower():
        score -= 0.05
    if any(tag == "ambiguous" for tag in tags):
        score -= 0.2
    return max(0.0, round(score, 4))


def infer_tags(query: str) -> List[str]:
    tags = []
    lowered = query.lower()
    if any(cue in lowered for cue in REASONING_CUES):
        tags.append("requires_reasoning")
    if "error" in lowered or "bug" in lowered or "fix" in lowered:
        tags.append("debugging")
    if "summarize" in lowered or "brief" in lowered:
        tags.append("summarization")
    return tags


def generate_response(query: str, context: Optional[str] = None) -> ChatResponse:
    start = time.perf_counter()
    tags = infer_tags(query)
    if context:
        query_text = f"Context: {context.strip()}\nQuestion: {query.strip()}"
    else:
        query_text = query.strip()

    if any(cue in query_text.lower() for cue in REASONING_CUES):
        response = (
            "The answer is grounded in clear logic: first identify the goal, then connect each step to it, "
            "and finally summarize the result."
        )
        reasoning = (
            "1. Identify the core requirement. "
            "2. Map the requirement to the possible decision paths. "
            "3. Select the path that aligns with the stated constraints."
        )
    elif "summarize" in query_text.lower() or "brief" in query_text.lower():
        response = "This recommendation is concise and focuses on the main result without extra detail."
        reasoning = "The response removes noise and highlights the primary outcome to satisfy the summarization request."
    elif "debug" in query_text.lower() or "problem" in query_text.lower():
        response = "The issue appears to arise from a misaligned assumption; verify the input shape and the boundary conditions."
        reasoning = "I first isolate the likely failure mode, then propose the minimal verification step to confirm it."
    else:
        response = "The most reliable solution is to follow established best practices while keeping the answer short and precise."
        reasoning = "I choose the proven approach that balances correctness and clarity for the given request."

    latency_ms = round((time.perf_counter() - start) * 1000, 2)
    style_score = compute_style_score(response, reasoning, tags)
    return ChatResponse(
        response=response,
        reasoning=reasoning,
        style_score=style_score,
        latency_ms=latency_ms,
        tags=tags,
        metadata={"prompt": PROMPT_TEMPLATE, "query_length": len(query_text)},
    )


def recall_prompt() -> str:
    return PROMPT_TEMPLATE
