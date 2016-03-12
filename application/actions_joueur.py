# -*- coding : utf-8 -*-

""" -- actions_joueur.py

VARIABLES GLOBALES

 - terrain              - list - le terrain de jeu,
 - terrain_complet      - tuple - la sauvegarde non-modifiable du terrain,
 - cases_vues           - list - les cases découvertes par le joueur,
 - pos_mines            - tuple - les positions des mines sur le terrain.


FONCTIONS

    COMMANDES
- rejouer(largeur, hauteur, nombre_mines)                           -> (None).
"""

# Pour faire une sauvegarde sans références problématiques
from copy import deepcopy
from constantes import *
import terrain as jeu
import interface as iu

# LES GLOBALES ################################################################

terrain = []
terrain_complet = ()

cases_vues = []

pos_mines = ()

# LES COMMANDES ###############################################################


def command_rejouer() -> (None):
    """Prépare une nouvelle partie complète.

Commande pour le bouton 'but_rejouer'."""

    global terrain, terrain_complet, cases_vues, pos_mines

    # On récupère les nouveaux paramètres
    largeur = iu.sc_largeur.get()
    hauteur = iu.sc_hauteur.get()
    nb_mines = iu.sc_mines.get()

    # On remet à zéro les positions vues
    cases_vues = []

    # On génère un terrain et on récupère le terrain et les positions des mines
    terrain, pos_mines = jeu.genere_terrain(largeur, hauteur, nb_mines)

    # On sauvegarde le terrain non-modifié
    terrain_complet = tuple(deepcopy(terrain))

    # On génère le plateau
    iu.canvas_plateau(iu.fenetre, largeur, hauteur)


# Exemples en console, toutes les valeurs ici sont des valeurs de test
if __name__ == "__main__":

    iu.interface(NOM_APP, LARGEUR_MIN, HAUTEUR_MIN)
