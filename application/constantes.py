# -*- coding : utf-8 -*-

""" -- constantes.py

Initialise les constantes représentants les différents états possibles:
 - MINE
 - MINE_EXPLOSE
 - DRAPEAU
 - CASE
 - INCONNU
"""

# Représente une mine visible
MINE = 9

# Représente une mine venant d'exploser (> partie perdue)
MINE_EXPLOSE = 10

# Représente un drapeau (ajoutable/supprimable par le joueur)
DRAPEAU = -1

# Représente une case de base vide visible.
# La valeur peut varier entre 0 et 8 inclus.
CASE = 0

# Représente une case inconnue de l'utilisateur
INCONNU = -2
