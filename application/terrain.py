# -*- coding : utf-8 -*-

""" -- terrain.py

Permet d'initaliser et de contrôler le terrain de jeu du démineur.

classe:
    - Terrain:
        - __init__(largeur, hauteur)
        - affiche_terrain()
        - places_mines(nombres_mines)
        - entourage(x, y)
        - place_nombre_mines()
        - place_drapeau(x, y)
        - supprime_drapeau(x, y)
"""

from random import randint, shuffle # Pour effectuer l'aléatoire du
                                    # placement des mines
from copy import deepcopy # Pour éviter un problème de référence lors de copies
from constantes import * # Les constantes représentants les éléments du jeu


class Terrain:
    """ >> classe Terrain(Object)

INITIALISATION
 - largeur : int - largeur du terrain en case
 - hauteur : int - hauteur du terrain en case

VARIABLES
 - pos_mines : list - coordonnées (x, y) représentant les positions des \
différentes mines
 - pos_vues : list - coordonnées des cases découvertes par le joueur
 - terrain_complet : list - le terrain constitué des mines et de leur entourage

MÉTHODES
 - __init__(largeur, hauteur)        -> None
 - affiche_terrain()                 -> None
 - place_mines(nombre_mines=10)      -> self.terrain, liste
 - entourage(x, y)                   -> entourage, liste
 - place_nombre_mines()              -> self.terrain, liste
 - place_drapeau(x, y)               -> self.terrain, liste
 - supprime_drapeau(x, y)            -> self.terrain, liste
"""

    def __init__(self, largeur, hauteur):
        """Initialisation:
 - largeur : int - largeur du terrain en case
 - hauteur : int - hauteur du terrain en case
"""

        self.largeur = largeur
        self.hauteur = hauteur

        self.pos_mines = []
        self.pos_vues = []
        self.terrain_complet = []

        # Initialise le terrain avec des tableaux remplis de cases INCONNU
        self.terrain = [[CASE] * self.largeur for _ in range(self.hauteur)]

    def affiche_terrain(self, terrain):
        """Affiche le terrain formaté en console et le retourne."""

        for y in terrain:
            for x in y:
                print(x, end=' ')
            print()
        print()

        return terrain

    def place_mines(self, nombre_mines):
        """Place les mines dans self.terrain de façon aléatoire, selon le \
nombre demandé."""

        mines = 0

        # Tant que l'on a pas placé toutes les mines demandées
        while mines < nombre_mines:

            # On parcourt self.terrain
            for y in range(self.hauteur):
                for x in range(self.largeur):

                    # On place une mine si il n'y en a pas déjà une et qu'il
                    # reste un emplacement de libre (P(MINE)=0.1)
                    if randint(0, 9) == MINE and self.terrain[y][x] != MINE \
                            and mines < nombre_mines:

                        # On place la mine au point (x, y)
                        self.terrain[y][x] = MINE
                        mines += 1

        # On utilise shuffle pour mélanger les mines sur l'ensemble du terrain
        # car en cas de petit nombre de mines sur un grand terrain, elles
        # auront tendances à se placer dans les premières lignes
        shuffle(self.terrain)

        return self.terrain

    def entourage(self, x, y):
        """Retourne l'entourage d'une case donnée sous forme d'une liste. \
Aucune vérification sur la validité des coordonnées n'est effectuée."""

        # Si y-1 ou x-1 = -1, on risque d'accéder au mauvais élément de
        # self.terrain lors de la vérification de l'entourage de la case
        # donc on le place volontairement en dehors des possibilités
        # d'accès afin de lever une erreur et d'ajouter une CASE au lieu
        # d'une potentielle MINE lors de la vérification
        y_moins = y - 1 if y - 1 >= 0 else self.hauteur + 1
        x_moins = x - 1 if x - 1 >= 0 else self.largeur + 1

        # L'entourage de la case vérifiée
        entourage = []

        # Haut, à gauche
        try: entourage.append(self.terrain[y_moins][x_moins])
        except IndexError: entourage.append(CASE)

        # Haut, au milieu
        try: entourage.append(self.terrain[y_moins][x])
        except IndexError: entourage.append(CASE)

        # Haut, à droite
        try: entourage.append(self.terrain[y_moins][x+1])
        except IndexError: entourage.append(CASE)

        # Milieu, à droite
        try: entourage.append(self.terrain[y][x+1])
        except IndexError: entourage.append(CASE)

        # Bas, à droite
        try: entourage.append(self.terrain[y+1][x+1])
        except IndexError: entourage.append(CASE)

        # Bas, au milieu
        try: entourage.append(self.terrain[y+1][x])
        except IndexError: entourage.append(CASE)

        # Bas, à gauche
        try: entourage.append(self.terrain[y+1][x_moins])
        except IndexError: entourage.append(CASE)

        # Milieu, à gauche
        try: entourage.append(self.terrain[y][x_moins])
        except IndexError: entourage.append(CASE)

        return entourage

    def place_nombre_mines(self):
        """Met à jour self.terrain de façon à ce que chaque case n'étant pas \
une mine ni un drapeau prenne en compte le nombre de mine autour d'elle."""

        # On parcourt self.terrain
        for y in range(self.hauteur):
            for x in range(self.largeur):

                # La case n'est ni une mine ni un drapeau:
                # On procède à la vérification.
                # Pour cela, on vérifie les 8 cases l'entourant et on ajoute
                # leur contenu à 'entourage' si elles sont accessibles
                # (pas d'IndexError), sinon CASE: pas une mine
                if self.terrain[y][x] < MINE:
                    self.terrain[y][x] = self.entourage(x, y).count(MINE)
                # Sinon on ajoute la position à la liste des mines
                else:
                    self.terrain[y][x] = MINE
                    self.pos_mines.append((x, y))

        # self.terrain_complet ne doit pas être modifiable
        self.terrain_complet = tuple(deepcopy(self.terrain))

        return self.terrain

# Exemples en console, toutes les valeurs ici sont des valeurs de test.
if __name__ == "__main__":

    t = Terrain(10, 10)
    t.affiche_terrain()

    print("----------------")

    t.place_mines(25)
    t.affiche_terrain()

    print("----------------")

    t.place_nombre_mines()
    t.affiche_terrain()
