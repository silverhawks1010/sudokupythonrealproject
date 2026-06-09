import json
import os

from src.utils.constants import SCORES_FILE


def load_scores() -> dict[str, int]:
    """Return all saved scores as {player_name: total_score}."""
    if not os.path.exists(SCORES_FILE):
        return {}
    with open(SCORES_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_score(player_name: str, total_score: int) -> None:
    """Persist a player's total score."""
    scores = load_scores()
    scores[player_name] = total_score
    os.makedirs(os.path.dirname(SCORES_FILE), exist_ok=True)
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)


def best_player() -> tuple[str, int] | None:
    """Return (name, score) for the player with the highest score, or None."""
    scores = load_scores()
    if not scores:
        return None
    name = max(scores, key=lambda n: scores[n])
    return name, scores[name]
