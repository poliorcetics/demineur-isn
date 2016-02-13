# -*- coding : utf-8 -*-

from terrain import * # On fait appel au fichier terrain

# On créer une fonction qui nous permet de régénéré le terrain
# On réutilise les variables largeur, hauteur et nombre_mines 

def rejouer(largeur, hauteur, nombre_mines):

    # On réutilise les valeurs déjà connu de largeur et hauteur
    terrain = Terrain(largeur, hauteur)
    
    # On réutilise les valeurs déjà connu de nombre_mines
    terrain.place_mines(nombre_mines)

    # On réutilise la variable place_nombre_mines qui va changer la place des mines
    terrain.place_nombre_mines()

    return terrain.affiche_terrain() 

# Exemples en console, toutes les valeurs ici sont des valeurs de test.

if __name__ == "__main__":

    rejouer(8,8,10)

