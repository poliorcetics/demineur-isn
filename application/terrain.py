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
        - place_nombre_mines()
"""


class Terrain:
    """ >> class Terrain

largeur : int - largeur du terrain
hauteur : int - hauteur du terrain

- __init__(largeur, hauteur) -> None
- affiche_terrain() -> None
- place_mines(nombre_mines=10) -> self.terrain, liste
- place_nombre_mines() -> self.terrain, liste
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
nombre demandé.

Soulève une ValueError si le nombre de mines demandé est plus grand que la \
taille du terrain."""

        # Le nombre de mine déjà placées
        mines = 0

        # Si l'on demande trop de mines, on indique que c'est impossible
        if nombre_mines > self.largeur * self.hauteur: raise ValueError

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

    def place_nombre_mines(self):
        """"Met à jour self.terrain de façon à ce que chaque case n'étant pas \
une mine prenne en compte le nombre de mine autour d'elle."""

        # On parcourt self.terrain
        for y in range(self.hauteur):
            for x in range(self.largeur):

                # Si y-1 ou x-1 = -1, on risque d'accéder au mauvais élément de
                # self.terrain lors de la vérification de l'entourage de la case
                # donc on le place volontairement en dehors des possibilités
                # d'accès afin de lever une erreur et d'ajouter un 0 au lieu
                # d'un potentiel 9 lors de la vérification
                y_moins = y - 1 if y - 1 >= 0 else self.hauteur + 1
                x_moins = x - 1 if x - 1 >= 0 else self.largeur + 1

                entourage = [] # L'entourage de la case vérifiée

                # Si la case n'est pas une mine, on procède à la vérification
                # Pour cela, on vérifie les 8 cases l'entourant et on ajoute
                # leur contenu à 'entourage' si elles sont accessibles
                # (pas d'IndexError), sinon 0 (pas une mine)
                if self.terrain[y][x] < 9:                    

                    try: entourage.append(self.terrain[y_moins][x_moins])
                    except IndexError: entourage.append(0)

                    try: entourage.append(self.terrain[y_moins][x])
                    except IndexError: entourage.append(0)

                    try: entourage.append(self.terrain[y_moins][x+1])
                    except IndexError: entourage.append(0)

                    try: entourage.append(self.terrain[y][x+1])
                    except IndexError: entourage.append(0)

                    try: entourage.append(self.terrain[y+1][x+1])
                    except IndexError: entourage.append(0)

                    try: entourage.append(self.terrain[y+1][x])
                    except IndexError: entourage.append(0)

                    try: entourage.append(self.terrain[y+1][x_moins])
                    except IndexError: entourage.append(0)

                    try: entourage.append(self.terrain[y][x_moins])
                    except IndexError: entourage.append(0)
  
                    # En comptant le nombre de 9 dans l'entourage, on obtient le
                    # nombre de mines. On passe cette valeur à la case vérifiée.
                    self.terrain[y][x] = entourage.count(9)

        return self.terrain


# Exemples en console, toutes les valeurs ici sont des valeurs de test.
if __name__ == "__main__":
    
    t = Terrain(12, 12)
    t.affiche_terrain()

    print("----------------")
    
    t.place_mines(12*12//3)
    t.affiche_terrain()
    
    print("----------------")
    
    t.place_nombre_mines()
    t.affiche_terrain()