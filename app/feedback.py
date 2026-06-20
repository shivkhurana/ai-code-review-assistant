from collections import Counter
from app.models import FeedbackAdvice
from typing import Dict


class FeedbackLoop:
    def suggest_refinement(self, failures: Counter[str]) -> str:
        if not failures:
            return "No prompt refinements required; performance is within target margins."

        recommendations = []
        if failures.get("style_score_below_threshold", 0) > 0:
            recommendations.append(
                "Update the prompt to enforce shorter, direct answers with explicit instructions for tone and sentence count."
            )
        if failures.get("missing_reasoning_clarity", 0) > 0:
            recommendations.append(
                "Add a stronger reasoning requirement to the prompt: 'Always provide a clear reasoning trace with at least three steps.'"
            )
        if failures.get("latency_exceeded", 0) > 0:
            recommendations.append(
                "Optimize the response generator or simplify the prompt template to ensure latency stays below 800ms."
            )

        if not recommendations:
            return "Monitor the batch results and adjust the prompt only if any new failure mode appears."

        return " | ".join(recommendations)


def classify_failure(issue_code: str) -> FeedbackAdvice:
    mapping = {
        "style_score_below_threshold": FeedbackAdvice(
            issue_type="Style Compliance",
            recommendation="Reinforce brevity and explicit formatting constraints in the prompt.",
            target_improvement="Increase style score consistency to 0.8+."
        ),
        "missing_reasoning_clarity": FeedbackAdvice(
            issue_type="Reasoning Quality",
            recommendation="Require the assistant to mention each reasoning step clearly and include causal language.",
            target_improvement="Reduce reasoning misses to fewer than 5% of queries."
        ),
        "latency_exceeded": FeedbackAdvice(
            issue_type="Latency",
            recommendation="Simplify inference rules or avoid expensive generation patterns."
            ,
            target_improvement="Keep response latency under 800ms for 99% of calls."
        ),
    }
    return mapping.get(issue_code, FeedbackAdvice(issue_type="Unknown", recommendation="Review issue details.", target_improvement="Investigate root cause."))
