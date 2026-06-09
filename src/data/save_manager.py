import json
import os

from src.utils.constants import SAVE_FILE


def has_save() -> bool:
    return os.path.exists(SAVE_FILE)


def write_save(data: dict) -> None:
    """Persist a paused game state to disk."""
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def read_save() -> dict:
    """Load and return the saved game state."""
    with open(SAVE_FILE, encoding="utf-8") as f:
        return json.load(f)


def delete_save() -> None:
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
