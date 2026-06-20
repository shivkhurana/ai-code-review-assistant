from fastapi import FastAPI, HTTPException
from typing import Any
from app.models import ChatRequest, ChatResponse, EvaluationSummary
from app.conversation import generate_response, recall_prompt
from app.evaluator import generate_mock_queries, evaluate_batch
from app.logger import configure_logger

app = FastAPI(title="Conversational AI Evaluation API")
logger = configure_logger()


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    if not payload.query or payload.query.strip() == "":
        logger.warning("Received empty query payload")
        raise HTTPException(status_code=400, detail="Query text is required.")
    response = generate_response(payload.query, payload.context)
    if response.latency_ms > 800:
        logger.warning(f"Latency threshold exceeded: {response.latency_ms}ms")
    logger.info(f"Chat response generated for session={payload.session_id or 'unknown'}")
    return response


@app.post("/evaluate", response_model=EvaluationSummary)
async def evaluate_endpoint(total_queries: int = 10000) -> EvaluationSummary:
    if total_queries < 1 or total_queries > 50000:
        raise HTTPException(status_code=400, detail="total_queries must be between 1 and 50000.")

    queries = generate_mock_queries(total_queries)
    summary = await evaluate_batch(queries)
    return summary


@app.get("/health")
async def health_check() -> dict[str, Any]:
    return {
        "service": "conversational_ai_evaluation_pipeline",
        "status": "healthy",
        "prompt": recall_prompt(),
    }
