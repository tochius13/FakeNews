from __future__ import annotations

from typing import Any


def calculate_score(results: list[dict[str, Any]]) -> float:
    total = 0.0
    count = 0

    for result in results:
        verdict = result.get("verdict")

        if verdict == "Supported":
            total += 1.0
            count += 1
        elif verdict == "Misleading":
            total += 0.5
            count += 1
        elif verdict == "Contradicted":
            total += 0.0
            count += 1
        elif verdict == "Unverifiable":
            continue

    if count == 0:
        return 0.0

    return round((total / count) * 100, 2)