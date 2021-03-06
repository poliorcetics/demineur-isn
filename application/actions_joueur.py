# -*- coding : utf-8 -*-

""" -- actions_joueur.py

VARIABLES GLOBALES

 - terrain              - list - le terrain de jeu,
 - terrain_complet      - tuple - la sauvegarde non-modifiable du terrain,
 - cases_vues           - list - les cases découvertes par le joueur,
 - pos_mines            - tuple - les positions des mines sur le terrain.


FONCTIONS

- command_rejouer()     -> (None).
"""

# Pour faire une sauvegarde sans références problématiques
from copy import deepcopy
from constantes import *
import terrain as jeu
import interface as iu
import actions_ordi as ordi

# LES GLOBALES ################################################################

# le terrain modifiable pour la partie et le terrain de base sauvegardé
terrain = []
terrain_complet = ()

# les cases vues par le joueur
cases_vues = []

# la position des mines sur le terrain
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

    # On prépare les éléments pour pouvoir finir la partie
    ordi.reset(hauteur, largeur, nb_mines)

    # On remet à zéro les positions vues
    cases_vues = []

    # On génère un terrain et on récupère le terrain et les positions des mines
    terrain, pos_mines = jeu.genere_terrain(largeur, hauteur, nb_mines)

    # On sauvegarde le terrain non-modifié
    terrain_complet = tuple(deepcopy(terrain))

    # On génère le plateau
    iu.canvas_plateau(iu.fenetre, largeur, hauteur)

    iu.lb_chrono.stop_chrono()
    iu.lb_chrono.lance_chrono()


# Exemples en console, toutes les valeurs ici sont des valeurs de test
if __name__ == "__main__":

    iu.interface(NOM_APP, LARGEUR_MIN, HAUTEUR_MIN)
