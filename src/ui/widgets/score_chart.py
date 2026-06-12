import matplotlib.pyplot as plt

from src.data.score_manager import load_scores

BG_DEEP = "#0d0821"
BG_PANEL = "#1e0f3a"
VIOLET = "#7c3aed"
VIOLET_HI = "#a78bfa"
TEXT = "#e9d5ff"


def show_scores_chart() -> None:
    """Open a matplotlib bar chart with all player scores."""
    scores = load_scores()
    if not scores:
        print("Aucun score à afficher.")
        return

    items = sorted(scores.items(), key=lambda x: -x[1])
    names = [name for name, _ in items]
    values = [score for _, score in items]

    fig, ax = plt.subplots(facecolor=BG_DEEP)
    ax.set_facecolor(BG_PANEL)

    bars = ax.bar(names, values, color=VIOLET, edgecolor=VIOLET_HI)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom",
            color=TEXT,
        )

    ax.set_title("Scores des joueurs", color=TEXT)
    ax.set_xlabel("Joueur", color=TEXT)
    ax.set_ylabel("Score", color=TEXT)
    ax.tick_params(colors=TEXT)
    for spine in ax.spines.values():
        spine.set_color(VIOLET)

    plt.tight_layout()
    plt.show()
