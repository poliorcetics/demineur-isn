# -*- coding : utf-8 -*-

""" -- terrain.py

Permet de générer un terrain miné avec les valeurs des cases calculées.

FONCTIONS

- entourage_case(terrain: list, x: int, y: int)               -> (list),
- place_mines(terrain: list, nb_mines: int)                   -> (list),
- place_nb_mines(terrain: list)                               -> (list, tuple),
- genere_terrain(largeur: int, hauteur: int, nb_mines: int)   -> (list, tuple),
- affiche_terrain(terrain: list)                              -> (None).
"""


# Pour effectuer l'aléatoire du placement des mines
from random import randint, shuffle
# Les constantes représentants les éléments du jeu
from constantes import *


def entourage_case(terrain: list, x: int, y: int) -> (list):
    """Retourne l'entourage d'une case donnée dans un terrain donné.

Arguments:
 - terrain      - list - le terrain dans lequel agir,
 - x            - int - la coordonnée x de la case dont on veut l'entourage,
 - y            - int - la coordonnée y de la case dont on veut l'entourage.

Retourne:
 - entourage    - list - la liste contenant l'entourage de la case."""

    # Si y-1 ou x-1 = -1, on risque d'accéder au mauvais élément de terrain
    # lors de la vérification de l'entourage de la case donc on le place
    # volontairement en dehors des possibilités d'accès afin de lever une
    # erreur et d'ajouter une CASE au lieu de recompter une MINE lors de
    # la vérification
    y_moins = y - 1 if y - 1 >= 0 else len(terrain)
    x_moins = x - 1 if x - 1 >= 0 else len(terrain[0])

    # L'entourage de la case vérifiée
    entourage = []

    # Haut, à gauche
    try: entourage.append(terrain[y_moins][x_moins])
    except IndexError: entourage.append(CASE)

    # Haut, au milieu
    try: entourage.append(terrain[y_moins][x])
    except IndexError: entourage.append(CASE)

    # Haut, à droite
    try: entourage.append(terrain[y_moins][x+1])
    except IndexError: entourage.append(CASE)

    # Milieu, à droite
    try: entourage.append(terrain[y][x+1])
    except IndexError: entourage.append(CASE)

    # Bas, à droite
    try: entourage.append(terrain[y+1][x+1])
    except IndexError: entourage.append(CASE)

    # Bas, au milieu
    try: entourage.append(terrain[y+1][x])
    except IndexError: entourage.append(CASE)

    # Bas, à gauche
    try: entourage.append(terrain[y+1][x_moins])
    except IndexError: entourage.append(CASE)

    # Milieu, à gauche
    try: entourage.append(terrain[y][x_moins])
    except IndexError: entourage.append(CASE)

    return entourage


def place_mines(terrain: list, nb_mines: int) -> (list):
    """Place le nombre de mines demandé dans un terrain donné.

Arguments:
 - terrain          - list - le terrain dans lequel on veut placer les mines,
 - nb_mines         - int - le nombre de mines à placer.

 Retourne:
  - terrain         - list - le terrain avec les mines placées."""

    try:
        # On vérifie que le nombre de mines demandés est correct
        assert(not (len(terrain[0]) * len(terrain) < nb_mines))
    except AssertionError:
        # Sinon on réduit le nombres de mines à la taille du terrain
        nb_mines = len(terrain[0]) * len(terrain)

    mines = 0

    # Tant que l'on a pas placé toutes les mines demandées
    while mines < nb_mines:

        # Parcours du terrain
        for y in range(len(terrain)):
            for x in range(len(terrain[0])):

                # On place une mine si il n'y en a pas déjà une et qu'il reste
                # un emplacement de libre (P(MINE)=0.1)
                if randint(0, 9) == MINE and terrain[y][x] != MINE \
                        and mines < nb_mines:

                    # On place la mine à la case (x, y)
                    terrain[y][x] = MINE

                    # Pour éviter de placer toutes les mines au début
                    shuffle(terrain)

                    # On prend en compte la mine ajoutée
                    mines += 1

    return terrain


def place_nb_mines(terrain: list) -> (list, tuple):
    """Place le nombre de mines autour des cases dans chaque case du terrain \
qui n'est pas une mine, sinon ajoute la position à la liste des cases minées.

Argument:
 - terrain      - list - le terrain dans lequel on veut l'entourage des cases.

Retourne:
 - terrain       - list - le terrain avec les valeurs d'entourage calculées,
 - pos_mines     - tuple - les positions des mines."""

    pos_mines = []

    # Parcours du terrain
    for y in range(len(terrain)):
        for x in range(len(terrain[0])):

            # Si la case n'est pas une mine ni un drapeau, on place le nombre
            # de mines entourant la case dans la case
            if DRAPEAU < terrain[y][x] < MINE:
                terrain[y][x] = entourage_case(terrain, x, y).count(MINE)
            # Sinon on ajoute la position à la liste des mines
            else:
                pos_mines.append((x, y))

    return terrain, tuple(pos_mines)


def genere_terrain(largeur: int, hauteur: int, nb_mines: int) -> (list, tuple):
    """Génère un terrain comportant nb_mines dans un jeu de largeur * hauteur.

Arguments:
 - largeur          - int - largeur en case du terrain,
 - hauteur          - int - hauteur en case du terrain,
 - nb_mines         - int - le nombre de mines à placer dans le terrain.

Retourne:
 - terrain          - list - le terrain miné avec ses entourages calculés,
 - pos_mines        - tuple - les positions des mines."""

    # On génère un terrain vide
    terrain = [[CASE] * largeur for _ in range(hauteur)]

    # On y place les mines
    terrain = place_mines(terrain, nb_mines)

    # On calcule l'entourage et on récupère le terrain et la position des mines
    terrain, pos_mines = place_nb_mines(terrain)

    return terrain, pos_mines


def affiche_terrain(terrain: list) -> (None):
    """Affiche un terrain formaté en console.

Argument:
 - terrain      - list - le terrain à afficher."""

    for y in terrain:
        for x in y:
            print(x, end=' ')
        print()
    print()

# Valeurs de tests uniquement
if __name__ == '__main__':

    affiche_terrain(genere_terrain(8, 8, 10)[0])
    affiche_terrain(genere_terrain(10, 10, 10)[0])
    affiche_terrain(genere_terrain(5, 5, 15)[0])
    affiche_terrain(genere_terrain(30, 30, 150)[0])
