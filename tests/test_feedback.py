from collections import Counter
from app.feedback import FeedbackLoop, classify_failure


def test_feedback_suggests_refinement_for_failures():
    failures = Counter({"style_score_below_threshold": 15, "missing_reasoning_clarity": 5})
    feedback = FeedbackLoop().suggest_refinement(failures)
    assert "prompt" in feedback.lower()
    assert "reasoning" in feedback.lower()


def test_classify_failure_returns_actionable_advice():
    advice = classify_failure("missing_reasoning_clarity")
    assert advice.issue_type == "Reasoning Quality"
    assert "reasoning" in advice.recommendation.lower()
