from copy import deepcopy

class GrilleSudoku:
    def __init__(self, grille: list[list[int]]):
        """
        Initialise la grille de Sudoku à partir d'une matrice 9x9.
        Args:
            grille: Liste de listes d'entiers représentant la grille.
        """
        self.grille = deepcopy(grille)
        # Cases fixes (données initiales, non modifiables par le joueur)
        self.fixes = [
            [grille[l][c] != 0 for c in range(9)]
            for l in range(9)
        ]

    @classmethod
    def depuis_fichier(cls, chemin: str) -> "GrilleSudoku":
        """
        Charge une grille depuis un fichier texte et crée une instance.
        Args:
            chemin: Chemin du fichier contenant la grille.
        Returns:
            Une instance de GrilleSudoku.
        """
        return cls(lire_grille(chemin))

    def get(self, ligne: int, col: int) -> int:
        """
        Retourne la valeur de la case donnée.
        Args:
            ligne: Index de ligne (0-8).
            col: Index de colonne (0-8).
        Returns:
            La valeur entière de la case.
        """
        return self.grille[ligne][col]

    def set(self, ligne: int, col: int, valeur: int) -> None:
        """
        Écrit une valeur dans une case si elle n'est pas fixe.

        Args:
            ligne: Index de ligne (0-8).
            col: Index de colonne (0-8).
            valeur: Valeur à écrire (0 pour effacer, 1-9 pour placer un chiffre).

        Raises:
            ValueError: Si la case est fixe ou si la valeur est hors de l'intervalle.
        """
        if self.fixes[ligne][col]:
            raise ValueError("Case fixe, non modifiable")
        if not (0 <= valeur <= 9):
            raise ValueError("Valeur hors intervalle [0-9]")
        self.grille[ligne][col] = valeur

    def est_valide(self, ligne: int, col: int, val: int) -> bool:
        """Vérifie si une valeur peut être placée dans une case.

        La vérification porte sur la ligne, la colonne et le bloc 3x3.

        Args:
            ligne: Index de ligne (0-8).
            col: Index de colonne (0-8).
            val: Valeur à tester.

        Returns:
            True si la valeur est valide, False sinon.
        """
        # Vérifier la ligne
        if val in self.grille[ligne]:
            return False
        # Vérifier la colonne
        if val in [self.grille[l][col] for l in range(9)]:
            return False
        # Vérifier le bloc 3×3
        bl, bc = (ligne // 3) * 3, (col // 3) * 3
        for l in range(bl, bl + 3):
            for c in range(bc, bc + 3):
                if self.grille[l][c] == val:
                    return False
        return True

    def est_resolue(self) -> bool:
        """
        Indique si la grille est complètement remplie.
        Returns:
            True si toutes les cases sont non nulles, False sinon.
        """
        return all(
            self.grille[l][c] != 0
            for l in range(9) for c in range(9)
        )


def lire_grille(chemin: str) -> list[list[int]]:
    """
    Lit une grille de Sudoku depuis un fichier texte.
    Le fichier doit contenir 9 lignes, chacune composée de 9 entiers séparés par des espaces.

    Args:
        chemin: Chemin du fichier à lire.
    Returns:
        La grille sous forme de liste de listes d'entiers.
    Raises:
        ValueError: Si le format du fichier est invalide.
    """
    grille = []
    with open(chemin, "r") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            chiffres = list(map(int, ligne.split())) # renvoie une liste d'entiers 
            if len(chiffres) != 9:
                raise ValueError(f"Ligne invalide : {ligne!r}")
            grille.append(chiffres)
    if len(grille) != 9:
        raise ValueError(f"La grille doit avoir 9 lignes, pas {len(grille)}")
    return grille