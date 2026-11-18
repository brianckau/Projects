#!/usr/bin/env python3
"""Compute the default thesis index from JSON on stdin; null means unknown."""
import json
import sys

WEIGHTS = {"market_variance": 25, "evidence": 30, "investment_impact": 25,
           "catalyst_strength": 10, "timeliness": 10}

def calculate(scores):
    if not isinstance(scores, dict) or set(scores) != set(WEIGHTS):
        raise ValueError("Supply exactly these dimensions: " + ", ".join(WEIGHTS))
    known = 0.0
    missing = 0
    rows = {}
    for name, weight in WEIGHTS.items():
        score = scores[name]
        if score is None:
            missing += weight
            contribution = None
        else:
            if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 5 or score * 2 != int(score * 2):
                raise ValueError(name + " must be 0–5 in half-point increments, or null")
            contribution = weight * score / 5
            known += contribution
        rows[name] = {"score": score, "weight": weight, "contribution": contribution}
    return {"label": "Thesis confidence index — uncalibrated research judgment",
            "index": None if missing else round(known, 2),
            "range": [round(known, 2), round(known + missing, 2)], "dimensions": rows}

if __name__ == "__main__":
    try:
        print(json.dumps(calculate(json.load(sys.stdin)), indent=2, allow_nan=False))
    except (ValueError, TypeError, OverflowError) as exc:
        print("Invalid input: " + str(exc), file=sys.stderr)
        sys.exit(2)
