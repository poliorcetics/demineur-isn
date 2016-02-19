# -*- coding : utf-8 -*-

from terrain import * # On fait appel au fichier terrain

def nouveau_terrain(largeur, hauteur, nombre_mines):
    """Regénère le terrain pour préparer une nouvelle partie. \
Retourne un objet Terrain."""

    terrain = Terrain(largeur, hauteur) # Génération du terrain de base
    
    terrain.place_mines(nombre_mines) # minage

    terrain.place_nombre_mines() # entourage calculé

    return terrain # retourne un objet Terrain



# Exemples en console, toutes les valeurs ici sont des valeurs de test.
if __name__ == "__main__":

    print(nouveau_terrain(8,8,10).terrain_complet)

