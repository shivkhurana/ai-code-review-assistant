# Conversational AI Evaluation Pipeline

## Overview

This project implements a Python-based conversational AI evaluation pipeline using FastAPI and a simulated prompt/response framework.
It is designed to train, annotate, and evaluate autonomous AI agents with a focus on low-latency response generation, automated quality scoring, and explicit feedback-driven prompt refinement.

## Key Capabilities

- `POST /chat` endpoint for contextual queries with sub-800ms response targets
- Automated batch annotation and evaluation for 10,000+ mock queries
- Style and reasoning error detection with strict quality standards
- Feedback loop for accuracy metrics, issue logging, and prompt refinement suggestions
- Structured pytest suite to track latency and response quality over time

## Architecture

- `app/models.py` — typed request/response/evaluation models
- `app/conversation.py` — core conversational logic and prompt template execution
- `app/evaluator.py` — bulk annotation and response quality evaluation
- `app/feedback.py` — failure-driven feedback loop and prompt refinement guidance
- `app/logger.py` — structured logging for metrics and failure tracking
- `app/node_api.py` — FastAPI app exposing conversation and evaluation endpoints
- `main.py` — start the application server or run a local evaluation cycle

## Installation

```bash
cd conversational_ai_evaluation_pipeline
python -m pip install -r requirements.txt
```

## Run the API

```bash
uvicorn app.node_api:app --host 0.0.0.0 --port 8100
```

## Core Endpoints

- `POST /chat` — accept contextual queries and return an annotated AI response
- `POST /evaluate` — run a batch evaluation pass for a configurable number of queries
- `GET /health` — service health and metrics

## Testing

Run the validation suite with:

```bash
pytest -q
```

## Evaluation Protocol

1. Generate 10,000+ synthetic query variations using realistic assistant prompts.
2. Score responses for:
   - reasoning clarity
   - style compliance
   - edge-case handling
   - task alignment
3. Log failures and compute metrics:
   - accuracy rate
   - reasoning error rate
   - style compliance rate
4. Use the feedback loop to recommend prompt refinements when performance drops below 95%.

## Notes

This system simulates an evaluation environment with strict quality monitoring, enabling iterative prompt improvement without requiring an external LLM backend.
