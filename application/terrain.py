# -*- coding : utf-8 -*-

from random import randint # Pour effectuer l'aléatoire du placement des mines
from pprint import pprint # Pour afficher correctement un tableau

""" -- terrain.py

Permet d'initaliser le terrain de jeu du démineur.

classes:
    - Terrain:
        - __init__(largeur, hauteur)
        - affiche_terrain()
        - places_mines(nombres_mines)
"""


class Terrain:
    """ >> Terrain
largeur : int - largeur du terrain
hauteur : int - hauteur du terrain

- __init__(largeur, hauteur) -> None
- affiche_terrain() -> None
- place_mines(nombre_mines=10) -> self.terrain, liste
    """

    def __init__(self, largeur, hauteur):

        self.largeur = largeur
        self.hauteur = hauteur

        # Initialise le terrain avec des tableaux remplis de 0
        self.terrain = [[0] * self.largeur for _ in range(self.hauteur)]

    def affiche_terrain(self):
        """Affiche le terrain formaté en console."""

        # Affiche le terrain formaté
        pprint(self.terrain)

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
                    # reste un emplacement de libre avec une probabilité de 1/10
                    if randint(0, 9) == 9 and \
                            self.terrain[y][x] != 9 and \
                            mines < nombre_mines:
                        
                        # On place la mine au point (x, y) 
                        self.terrain[y][x] = 9
                        mines += 1

        return self.terrain

# Exemples en console
if __name__ == "__main__":
    
    t = Terrain(6, 6)
    t.affiche_terrain()
    print("----------------")
    t.place_mines(10)
    t.affiche_terrain()
