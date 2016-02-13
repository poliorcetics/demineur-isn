# -*- coding : utf-8 -*-

from random import randint, shuffle # Pour effectuer l'aléatoire du
                                    # placement des mines
from constantes import * # Les constantes représentants les éléments du jeu

""" -- terrain.py

Permet d'initaliser le terrain de jeu du démineur.

classes:
    - Terrain:
        - __init__(largeur, hauteur)
        - affiche_terrain()
        - places_mines(nombres_mines)
        - entourage(x, y)
        - place_nombre_mines()
        - place_drapeau(x, y)
        - supprime_drapeau(x, y)
"""


class Terrain:
    """ >> class Terrain

largeur : int - largeur du terrain
hauteur : int - hauteur du terrain

- __init__(largeur, hauteur) -> None
- affiche_terrain() -> None
- place_mines(nombre_mines=10) -> self.terrain, liste
- entourage(x, y) -> entourage, liste
- place_nombre_mines() -> self.terrain, liste
- place_drapeau(x, y) -> self.terrain, liste
- supprime_drapeau(x, y) -> self.terrain, liste 
"""

    def __init__(self, largeur, hauteur):

        self.largeur = largeur
        self.hauteur = hauteur
        self.pos_mines = []

        # Initialise le terrain avec des tableaux remplis de 0
        self.terrain = [[INCONNU] * self.largeur for _ in range(self.hauteur)]

    def affiche_terrain(self):
        """Affiche le terrain formaté en console et le retourne."""

        for y in self.terrain:
            for x in y:
                print(x, end=' ')
            print()

        return self.terrain

    def place_mines(self, nombre_mines):
        """Place les mines dans self.terrain de façon aléatoire, selon le \
nombre demandé.

Lève une ValueError si le nombre de mines demandé est plus grand que la \
taille du terrain."""

        # Si l'on demande trop de mines, on indique que c'est impossible
        if nombre_mines > self.largeur * self.hauteur: raise ValueError

        # Tant que l'on a pas placé toutes les mines demandées
        while len(self.pos_mines) < nombre_mines:

            # On parcourt self.terrain
            for y in range(self.hauteur):
                for x in range(self.largeur):
                    
                    # On place une mine si il n'y en a pas déjà une et qu'il
                    # reste un emplacement de libre avec une probabilité de 1/10
                    if randint(0, 9) == 9 and self.terrain[y][x] != MINE \
                            and len(self.pos_mines) < nombre_mines:
                        
                        # On place la mine au point (x, y) 
                        self.terrain[y][x] = MINE
                        
                        # On retient la position de la mine ajoutée
                        self.pos_mines.append((x, y))

        # On utilise shuffle pour mélanger les mines sur l'ensemble du terrain
        # car en cas de petit nombre de mines sur un grand terrain, elles auront
        # tendances à se placer dans les premières lignes
        return shuffle(self.terrain)

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

        entourage = [] # L'entourage de la case vérifiée                   

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
        """"Met à jour self.terrain de façon à ce que chaque case n'étant pas \
une mine ni un drapeau prenne en compte le nombre de mine autour d'elle."""

        # On parcourt self.terrain
        for y in range(self.hauteur):
            for x in range(self.largeur):

                # La case n'est ni une mine ni un drapeau:
                # On procède à la vérification.
                # Pour cela, on vérifie les 8 cases l'entourant et on ajoute
                # leur contenu à 'entourage' si elles sont accessibles
                # (pas d'IndexError), sinon CASE: pas une mine
                if -1 < self.terrain[y][x] < 9:

                    self.terrain[y][x] = self.entourage(x, y).count(MINE)

        return self.terrain

    def place_drapeau(self, x, y):
        """Place un drapeau à la case de coordonnées (x, y). Retourne le \
terrain modifié."""

        self.terrain[y][x] = DRAPEAU

        return self.terrain

    def supprime_drapeau(self, x, y):
        """Enlève le drapeau de la case de coordonnées (x, y) s'il y en a un \
et le remplace par sa valeur normale. Retourne le terrain modifié.

Lève une ValueError si la case n'est pas un drapeau."""

        if self.terrain[y][x] != DRAPEAU:
            raise ValueError("La case n'est pas un drapeau")

        self.terrain[y][x] = MINE if (x, y) in self.pos_mines \
                                  else self.entourage(x, y).count(MINE)

        return self.terrain



# Exemples en console, toutes les valeurs ici sont des valeurs de test.
if __name__ == "__main__":
    
    t = Terrain(10, 10)
    t.affiche_terrain()

    print("----------------")
    
    t.place_mines(10)
    t.affiche_terrain()

    print("----------------")
    
    t.place_nombre_mines()
    t.affiche_terrain()