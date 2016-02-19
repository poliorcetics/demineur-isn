# -*- coding : utf-8 -*-

""" -- constantes_jeu.py

Initialise les constantes représentants les différents états possibles du jeu:
 - MINE
 - MINE_EXPLOSE
 - DRAPEAU
 - CASE
 - INCONNU

Initialise les constantes servant à l'interface du jeu:
 - NOM_APP
 - LARGEUR_MIN
 - HAUTEUR_MIN

Initialise les constantes servant aux réglages du jeu
 - MIN_CASES
 - MAX_CASES
"""
#####################
# CONSTANTES DU JEU #
#####################

# Représente une mine visible
MINE = 9

# Représente une mine venant d'exploser (> partie perdue)
MINE_EXPLOSE = 10

# Représente un drapeau (ajoutable/supprimable par le joueur)
DRAPEAU = -1

# Représente une case de base vide visible.
CASE = 0

# Représente une case inconnue de l'utilisateur
INCONNU = -2

#############################
# CONSTANTES DE L'INTERFACE #
#############################

# Le nom de l'application
NOM_APP = 'Démineur ISN'

# La taille minimum de la fenêtre de jeu en largeur, en pixel
LARGEUR_MIN = 300

# La taille minimum de la fenêtre de jeu en hauteur, en pixel
HAUTEUR_MIN = 150

###########################
# CONSTANTES DES RÉGLAGES #
###########################

# Nombre minimum de cases (largeur comme hauteur)
MIN_CASES = 5

# Nombres maximum de cases (largeur comme hauteur)
MAX_CASES = 30
