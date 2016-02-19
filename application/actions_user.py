# -*- coding : utf-8 -*-

""" -- actions_user.py

- nouveau_terrain(largeur, hauteur, nombre_mines)               -> Terrain()
"""

from terrain import Terrain # On fait appel au fichier terrain


def nouveau_terrain(largeur, hauteur, nombre_mines):
    """Regénère le terrain pour préparer une nouvelle partie. \
Retourne un objet Terrain."""

    # Génération du terrain de base
    terrain = Terrain(largeur, hauteur)

    # minage
    terrain.place_mines(nombre_mines)

    # entourage calculé
    terrain.place_nombre_mines()

    # retourne un objet Terrain
    return terrain

# Exemples en console, toutes les valeurs ici sont des valeurs de test
if __name__ == "__main__":

    jeu = nouveau_terrain(8, 8, 10)
    jeu.affiche_terrain(jeu.terrain_complet)
