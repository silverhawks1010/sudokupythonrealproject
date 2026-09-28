from copy import deepcopy


class ErreurPlacement(Exception):
    """Exception levée quand un chiffre ne peut pas être placé."""
    pass


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
        Valide le placement avant d'écrire (sauf pour effacer avec 0).

        Args:
            ligne: Index de ligne (0-8).
            col: Index de colonne (0-8).
            valeur: Valeur à écrire (0 pour effacer, 1-9 pour placer un chiffre).

        Raises:
            ValueError: Si la case est fixe ou si la valeur est hors intervalle.
            ErreurPlacement: Si le placement viole les règles du Sudoku.
        """
        if self.fixes[ligne][col]:
            raise ValueError(f"La case ({ligne}, {col}) est fixe et ne peut pas être modifiée.")
        if not (0 <= valeur <= 9):
            raise ValueError(f"Valeur {valeur!r} invalide : doit être entre 0 et 9.")
        # On ne valide pas le placement pour une suppression (valeur == 0)
        if valeur != 0:
            self.valider_placement(ligne, col, valeur)
        self.grille[ligne][col] = valeur

    # ------------------------------------------------------------------ 
    #  Validation                                                        
    # ------------------------------------------------------------------ 

    def valider_placement(self, ligne: int, col: int, val: int) -> None:
        """
        Vérifie qu'un chiffre peut être placé dans une case.
        Lève une ErreurPlacement détaillée si une règle est violée.

        La vérification porte sur :
          - les coordonnées et la valeur (préconditions)
          - la ligne
          - la colonne
          - le bloc 3×3

        Args:
            ligne: Index de ligne (0-8).
            col: Index de colonne (0-8).
            val: Chiffre à tester (1-9).

        Raises:
            ValueError: Si les coordonnées ou la valeur sont hors limites.
            ErreurPlacement: Si le placement viole une règle du Sudoku.
        """
        # --- Préconditions ---
        if not (0 <= ligne <= 8) or not (0 <= col <= 8):
            raise ValueError(
                f"Coordonnées ({ligne}, {col}) hors limites. "
                "Les index doivent être compris entre 0 et 8."
            )
        if not (1 <= val <= 9):
            raise ValueError(
                f"Valeur {val!r} invalide pour une validation : doit être entre 1 et 9."
            )

        raisons = []  # On collecte toutes les violations avant de lever l'exception

        # --- Vérification de la ligne ---
        if val in self.grille[ligne]:
            col_conflit = self.grille[ligne].index(val)
            raisons.append(
                f"La ligne {ligne + 1} contient déjà le chiffre {val} "
                f"(case ({ligne}, {col_conflit}))."
            )

        # --- Vérification de la colonne ---
        colonne = [self.grille[l][col] for l in range(9)]
        if val in colonne:
            ligne_conflit = colonne.index(val)
            raisons.append(
                f"La colonne {col + 1} contient déjà le chiffre {val} "
                f"(case ({ligne_conflit}, {col}))."
            )

        # --- Vérification du bloc 3×3 ---
        bl, bc = (ligne // 3) * 3, (col // 3) * 3
        for l in range(bl, bl + 3):
            for c in range(bc, bc + 3):
                if self.grille[l][c] == val:
                    raisons.append(
                        f"Le bloc 3×3 ({bl // 3 + 1}, {bc // 3 + 1}) contient déjà "
                        f"le chiffre {val} (case ({l}, {c}))."
                    )

        if raisons:
            detail = "\n  - ".join(raisons)
            raise ErreurPlacement(
                f"Impossible de placer {val} en ({ligne}, {col}) :\n  - {detail}"
            )

    def est_valide(self, ligne: int, col: int, val: int) -> bool:
        """
        Vérifie silencieusement si une valeur peut être placée (sans lever d'exception).
        Utile pour le solveur automatique.

        Args:
            ligne: Index de ligne (0-8).
            col: Index de colonne (0-8).
            val: Valeur à tester (1-9).

        Returns:
            True si le placement est valide, False sinon.
        """
        try:
            self.valider_placement(ligne, col, val)
            return True
        except (ValueError, ErreurPlacement):
            return False

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


# ------------------------------------------------------------------ #
#  Lecture du fichier                                                 #
# ------------------------------------------------------------------ #

def lire_grille(chemin: str) -> list[list[int]]:
    """
    Lit une grille de Sudoku depuis un fichier texte.
    Ignore les lignes vides et les commentaires (commençant par #).
    Le fichier doit contenir exactement 9 lignes de 9 entiers séparés par des espaces.

    Args:
        chemin: Chemin du fichier à lire.
    Returns:
        La grille sous forme de liste de listes d'entiers.
    Raises:
        ValueError: Si le format du fichier est invalide.
    """
    grille = []
    with open(chemin, "r") as f:
        for numero, ligne in enumerate(f, start=1):
            ligne = ligne.strip()
            if not ligne or ligne.startswith("#"):   # ignore commentaires
                continue
            try:
                chiffres = list(map(int, ligne.split()))
            except ValueError:
                raise ValueError(
                    f"Ligne {numero} : caractère non numérique détecté → {ligne!r}"
                )
            if len(chiffres) != 9:
                raise ValueError(
                    f"Ligne {numero} : attendu 9 chiffres, trouvé {len(chiffres)} → {ligne!r}"
                )
            if any(not (0 <= c <= 9) for c in chiffres):
                raise ValueError(
                    f"Ligne {numero} : les valeurs doivent être entre 0 et 9 → {ligne!r}"
                )
            grille.append(chiffres)

    if len(grille) != 9:
        raise ValueError(
            f"La grille doit contenir exactement 9 lignes, trouvé {len(grille)}."
        )
    return grille


class Board:
    """Modern board used by GameSession, IASolver and grid_loader."""

    def __init__(self):
        self._grid: list[list[int]] = [[0] * 9 for _ in range(9)]
        self._locked: list[list[bool]] = [[False] * 9 for _ in range(9)]

    def load(self, grid: list[list[int]]) -> None:
        self._grid = deepcopy(grid)
        self._locked = [[grid[r][c] != 0 for c in range(9)] for r in range(9)]

    def get(self, row: int, col: int) -> int:
        return self._grid[row][col]

    def is_locked(self, row: int, col: int) -> bool:
        return self._locked[row][col]

    def is_valid_placement(self, row: int, col: int, value: int) -> bool:
        if value in self._grid[row]:
            return False
        if value in [self._grid[r][col] for r in range(9)]:
            return False
        br, bc = (row // 3) * 3, (col // 3) * 3
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if self._grid[r][c] == value:
                    return False
        return True

    def place(self, row: int, col: int, value: int) -> bool:
        if self._locked[row][col]:
            return False
        if not self.is_valid_placement(row, col, value):
            return False
        self._grid[row][col] = value
        return True

    def clear(self, row: int, col: int) -> bool:
        if self._locked[row][col]:
            return False
        self._grid[row][col] = 0
        return True

    def is_complete(self) -> bool:
        return all(self._grid[r][c] != 0 for r in range(9) for c in range(9))

    def to_list(self) -> list[list[int]]:
        return deepcopy(self._grid)

    def initial_grid(self) -> list[list[int]]:
        """Returns the puzzle grid (only locked/initial cells, 0 elsewhere)."""
        return [
            [self._grid[r][c] if self._locked[r][c] else 0 for c in range(9)]
            for r in range(9)
        ]