class Player:
    """Represents a human player with a name and cumulative score."""

    def __init__(self, name: str):
        self.name = name
        self.total_score: int = 0

    def apply_score(self, delta: int) -> None:
        self.total_score += delta

    def __repr__(self) -> str:
        return f"Player(name={self.name!r}, score={self.total_score})"
