import asyncio
from app.evaluator import generate_mock_queries, evaluate_batch


def test_generate_mock_queries_returns_requested_count():
    queries = generate_mock_queries(25)
    assert len(queries) == 25
    assert queries[0].query


def test_evaluate_batch_computes_accuracy():
    queries = generate_mock_queries(50)
    summary = asyncio.run(evaluate_batch(queries))
    assert summary.total_queries == 50
    assert 0.0 <= summary.accuracy <= 100.0
    assert summary.prompt_refinement


def test_evaluate_batch_latency_metric_is_numeric():
    queries = generate_mock_queries(10)
    summary = asyncio.run(evaluate_batch(queries))
    assert isinstance(summary.average_latency_ms, float)
    assert summary.average_latency_ms >= 0.0
