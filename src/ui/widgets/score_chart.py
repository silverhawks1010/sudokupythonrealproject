import matplotlib.pyplot as plt

from src.data.score_manager import load_scores


def show_scores_chart() -> None:
    """Open a matplotlib bar chart with all player scores."""
    scores = load_scores()
    if not scores:
        print("No scores to display.")
        return
    names = list(scores.keys())
    values = [scores[n] for n in names]
    fig, ax = plt.subplots()
    ax.bar(names, values)
    ax.set_title("Player Scores")
    ax.set_xlabel("Player")
    ax.set_ylabel("Score")
    plt.tight_layout()
    plt.show()
