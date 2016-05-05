# -*- coding : utf-8 -*-

""" -- interface.py

Permet de lancer l'interface et de la mettre à jour lors d'actions.

VARIABLES GLOBALES

 - fenetre          - tk.Tk - la fenêtre principale,
 - fr_reglages      - tk.Frame - le panneau de réglages,
 - cv_plateau       - tk.Canvas - le plateau de jeu,
 - sc_largeur       - tk.Scale - l'échelle du choix de largeur,
 - sc_hauteur       - tk.Scale - l'échelle du choix de hauteur,
 - sc_mines         - tk.Scale - l'échelle du choix du nombre de mines,
 - but_rejouer      - tk.Button - le bouton pour rejouer,
 - cases            - dict(tk.Label: (int, int)) - les cases et leur position,
 - cases_pos        - dict((int, int): tk.Label) - les positions et leur case,
 - cases_taille     - int - la taille en pixel des côtés des cases,
 - cases_img        - dict(int: tk.PhotoImage) - les type de case et les \
images correspondantes.

FONCTIONS

    MISES À JOUR
 - maj_taille_cases(largeur: int, hauteur: int)                  -> (bool),
 - maj_images(racine: tk.Canvas, taille: int)                    -> (None),
 - maj_revele_case(x: int, y: int)                               -> (None),

    ÉVÈNEMENTS
 - event_max_mines(event: tk.Event)                              -> (None),
 - event_case(c: tk.Event)                                       -> (None),
 - event_drapeau(c: tk.Event)                                    -> (None),

    PLATEAU DU JEU
 - label_case(racine: tk.Canvas, x: int, y: int)                 -> (tk.Label),
 - canvas_plateau(racine: tk.Tk,
                  largeur: int, hauteur: int,
                  col=0, lig=0)                                  -> (None),

    RÉGLAGES DU JEU
 - scale_largeur()                                               -> (None),
 - scale_hauteur()                                               -> (None),
 - scale_mines()                                                 -> (None),
 - button_rejouer()                                              -> (None),
 - frame_reglages(col=1, lig=0)                                  -> (None),

    INTERFACE GÉNÉRALE
 - interface(titre: str, largeur_min: int, hauteur_min: int)     -> (None).
"""

# Pour gérer l'accès aux ressources sur Windows/Unix
from os import sep, name
# Les fonctions pour l'interface graphique
import tkinter as tk
# Les constantes représentants les éléments du jeu
from constantes import *
# Les actions de l'utilisateur
import actions_joueur as actions
# Le chronomètre pour mesurer la durée d'une partie
from chronometre import Chrono

# LES VARIABLES GLOBALES ######################################################

# La fenêtre principale
fenetre = tk.Tk()

# Les composants de la fenêtre principle
fr_reglages = tk.Frame(fenetre)
cv_plateau = tk.Canvas(fenetre)

# Le chronomètre
lb_chrono = Chrono(fr_reglages)

# Les échelles pour les réglages
sc_largeur = tk.Scale(fr_reglages)
sc_hauteur = tk.Scale(fr_reglages)
sc_mines = tk.Scale(fr_reglages)

# Le bouton pour rejouer
but_rejouer = tk.Button(fr_reglages)

# Les cases du plateau
cases = {}
cases_pos = {}

# La taille des cases du plateau
cases_taille = 0

# Les images utilisables dans les cases du plateau
cases_img = {}


# LES MISES À JOUR ############################################################


def maj_taille_cases(largeur: int, hauteur: int) -> (bool):
    """Adapte la taille des images au nombre de cases du plateau.

Arguments:
 - largeur          - int - largeur en case du terrain,
 - hauteur          - int - hauteur en case du terrain.

Modifie:
 - cases_taille     - int - la taille en pixel du côté d'une case.

Retoune:
 - bool             - bool - True si la taille a bien changé, False sinon."""

    global cases_taille

    # On récupère la valeur du plus grand côté
    cote_max = max(largeur, hauteur)

    # On ajuste la taille du côté d'une case en fonction de cette valeur
    if 10 <= cote_max < 15:
        cases_taille = 45
        return True
    elif 15 <= cote_max < 20:
        cases_taille = 30
        return True
    elif 20 <= cote_max:
        cases_taille = 15
        return True
    else:
        cases_taille = 60
        return True

    # Erreur d'ajustement
    return False


def maj_images(racine: tk.Canvas, taille: int) -> (None):
    """Adapte les images utilisées pour afficher le terrain.

Arguments:
 - racine=cv_plateau    - tk.Canvas - juste là pour éviter un bug de \
référencement des images dans la mémoire
 - taille               - int - la taille en pixel des images

Modifie:
 - cases_img            - dict - les liens vers les images du jeu."""

    global cases_img

    # Libère les anciennes images chargés
    cases_img.clear()

    # Le chemin d'accès aux images
    chemin = 'ressources%s%s%s' % (sep, taille, sep)

    # Toutes les images sont liées
    cases_img = {
        0:        tk.PhotoImage(master=racine, file='%scase_0.gif' % chemin),
        1:        tk.PhotoImage(master=racine, file='%scase_1.gif' % chemin),
        2:        tk.PhotoImage(master=racine, file='%scase_2.gif' % chemin),
        3:        tk.PhotoImage(master=racine, file='%scase_3.gif' % chemin),
        4:        tk.PhotoImage(master=racine, file='%scase_4.gif' % chemin),
        5:        tk.PhotoImage(master=racine, file='%scase_5.gif' % chemin),
        6:        tk.PhotoImage(master=racine, file='%scase_6.gif' % chemin),
        7:        tk.PhotoImage(master=racine, file='%scase_7.gif' % chemin),
        8:        tk.PhotoImage(master=racine, file='%scase_8.gif' % chemin),
        BASE:     tk.PhotoImage(master=racine, file='%sbase.gif' % chemin),
        DRAPEAU:  tk.PhotoImage(master=racine, file='%sdrapeau.gif' % chemin),
        MINE:     tk.PhotoImage(master=racine, file='%smine.gif' % chemin),
        PERDU:    tk.PhotoImage(master=racine, file='%sperdu.gif' % chemin)
    }


def maj_revele_case(x: int, y: int) -> (None):
    """Révèle la case de coordonnées (x, y) plus les cases environnantes si \
la case est une case sans mines dans son entourage direct (de valeur 0).

Arguments:
 - x                - int - la position en x de la case,
 - y                - int - la position en y de la case.

Note:
 Ceci est une fonction récursive, sur un grand plateau avec peu de mines elle \
risque de prendre un peu de temps."""

    global cases, cases_pos, cases_img

    # On récupère la valeur de la case et on continue dans la fonction
    # uniquement si la case n'a pas déjà été révélé
    try:
        valeur_case = actions.terrain[y][x]
    except IndexError:
        return
    finally:
        if (x, y) in actions.cases_vues:
            return

    # On récupère la case sous sa forme de tk.Label
    case = cases_pos[(x, y)]

    # Si la case est un chiffre basique, on l'afiche
    if 0 < valeur_case < 9:
        actions.cases_vues.append((x, y))
        case['image'] = cases_img[valeur_case]
        return
    # Si la case vaut zéro, on révèle l'entourage
    elif valeur_case == 0:
        actions.cases_vues.append((x, y))
        case['image'] = cases_img[valeur_case]

        # Pour éviter les indices négatifs et les problèmes qui vont avec, on
        # provoque une IndexError dans les appels suivants
        y_moins = y - 1 if y - 1 >= 0 else len(actions.terrain)
        x_moins = x - 1 if x - 1 >= 0 else len(actions.terrain[0])

        # On teste les cases autour, pour les révéler ou propager la révélation
        # si elles sont de valeur 0
        # Haut, à gauche
        maj_revele_case(x_moins, y_moins)

        # Haut, au milieu
        maj_revele_case(x, y_moins)

        # Haut, à droite
        maj_revele_case(x+1, y_moins)

        # Milieu, à droite
        maj_revele_case(x+1, y)

        # Bas, à droite
        maj_revele_case(x+1, y+1)

        # Bas, au milieu
        maj_revele_case(x, y+1)

        # Bas, à gauche
        maj_revele_case(x_moins, y+1)

        # Milieu, à gauche
        maj_revele_case(x_moins, y)
    # Si la case n'était pas chiffrée (une mine donc), on la révèle simplement
    else:
        actions.cases_vues.append((x, y))
        case['image'] = cases_img[valeur_case]

# LES ÉVÈNEMENTS ##############################################################


def event_max_mines(event: tk.Event) -> (None):
    """Adpate le maximum de l'échelle du nombre de mines aux changements sur \
les échelles de largeur et de hauteur.

Modifie:
 - sc_mines['to']       - int - le maximum de mines plaçables."""

    global sc_mines, sc_largeur, sc_hauteur

    sc_mines['to'] = sc_largeur.get() * sc_hauteur.get()


def event_case(c: tk.Event) -> (None):
    """Lors d'un clic gauche sur une case, celle-ci est révélée si elle \
n'est pas un drapeau. Si la valeur de la case est 0, toutes les cases autour \
seront révélées elles-aussi."""

    global cases, cases_img

    # On récupère les coordonnées
    x, y = cases[c.widget]

    # S'il y a un drapeau, on ne fait rien
    if actions.terrain[y][x] == DRAPEAU:
        return
    # Si ce n'est pas un drapeau, alors on ajoute la case à la liste des
    # cases du terrain vues et on affiche la case
    else:
        # Gère la propagation de la révélation si la case vaut 0
        maj_revele_case(x, y)


def event_drapeau(c: tk.Event) -> (None):
    """Place ou supprime un drapeau si il est possible d'en placer/supprimer \
un."""

    global cases, cases_img

    # On récupère la case cliquée, ses coordonnées et la case du terrain
    # correspondante
    case = c.widget
    x, y = cases[case]
    valeur_case = actions.terrain[y][x]

    # S'il y a déjà un drapeau, on le supprime et on remplace par
    # l'ancienne valeur
    if valeur_case == DRAPEAU:
        # On remet l'image de base
        case['image'] = cases_img[BASE]
        actions.terrain[y][x] = actions.terrain_complet[y][x]
        # On 'return' pour éviter de faire le test suivant si la case était
        # un drapeau
        return

    # S'il n'y a pas de drapeau (vérifié au dessus) et que la case est encore
    # cachée, on peut placer un drapeau
    if not ((x, y) in actions.cases_vues):
        case['image'] = cases_img[DRAPEAU]
        actions.terrain[y][x] = DRAPEAU


# LE PLATEAU DU JEU ###########################################################


def label_case(racine: tk.Canvas, x: int, y: int) -> (tk.Label):
    """Dessine une case de base non-découverte.

Arguments:
 - racine       - tk.Canvas - la fenêtre/sous-fenêtre où dessiner la case,
 - x            - int - la position en x de la case dans 'racine',
 - y            - int - la position en y de la case dans 'racine'.

Retourne:
 - case         - tk.Label - la référence vers la case créée."""

    global cases_img

    # Initialise la case
    case = tk.Label(racine,
                    borderwidth=1,
                    relief='sunken',
                    image=cases_img[BASE])

    # Lie la case à ses évènements
    case.bind('<Button-1>', event_case)
    # Pour Mac/Linux/Autres unix
    if name == 'posix':
        case.bind('<Button-2>', event_drapeau)
    # Pour Windows
    else:
        case.bind('<Button-3>', event_drapeau)
    # Place la case
    case.grid(column=x, row=y)

    return case


def canvas_plateau(racine: tk.Tk,
                   largeur: int, hauteur: int,
                   col=0, lig=0) -> (None):
    """Dessine le plateau de base du jeu, avant que l'utilisateur commence à \
jouer.

Argument:
 - racine       - tk.Tk - la fenêtre dans laquelle dessiner le plateau,
 - largeur      - int - largeur en case du terrain,
 - hauteur      - int - hauteur en case du terrain,
 - col=0        - int - la colonne de la racine où sera placé le plateau,
 - lig=0        - int - la ligne de la racine où sera placé le plateau.

Retourne:
 - plateau      - tk.Canvas - le plateau du jeu."""

    global cv_plateau, cases_taille, cases, cases_pos

    # On nettoie le plateau précédent
    cv_plateau.destroy()

    # On met à jour les images
    maj_taille_cases(largeur, hauteur)
    maj_images(cv_plateau, cases_taille)

    # Initialise le nouveau plateau
    cv_plateau = tk.Canvas(racine,
                           width=largeur * cases_taille,
                           height=hauteur * cases_taille)
    # Place le plateau
    cv_plateau.grid(column=col, row=lig, padx=10, pady=10)

    # Dessine les cases du jeu
    for y in range(hauteur):
        for x in range(largeur):
            # Récupère la référence en dessinant la case
            case = label_case(cv_plateau, x, y)
            # Associe la référence de la case à ses coordonnées (x, y)
            cases[case] = (x, y)
            # Associe les coordonnées (x, y) à la référence de la case
            cases_pos[(x, y)] = case


#  LES RÉGLAGES DU JEU ########################################################


def label_chrono() -> (None):
    """Le chronmètre pour mesurer la durée d'une partie."""

    lb_chrono.grid(column=0, row=0, pady=5)


def scale_largeur() -> (None):
    """L'échelle pour choisir la largeur."""

    global sc_largeur

    # Pour choisir le nombre de case en largeur
    sc_largeur['from'] = MIN_CASES
    sc_largeur['to'] = MAX_CASES
    sc_largeur['orient'] = 'horizontal'
    sc_largeur['label'] = 'Largeur:'

    sc_largeur.bind('<ButtonRelease>', event_max_mines)

    sc_largeur.grid(column=0, row=1, pady=5)


def scale_hauteur() -> (None):
    """L'échelle pour choisir la hauteur"""

    global sc_hauteur

    # Pour choisir le nombre de case en hauteur
    sc_hauteur['from'] = MIN_CASES
    sc_hauteur['to'] = MAX_CASES
    sc_hauteur['orient'] = 'horizontal'
    sc_hauteur['label'] = 'Hauteur'

    sc_hauteur.bind('<ButtonRelease>', event_max_mines)

    sc_hauteur.grid(column=0, row=2, pady=5)


def scale_mines() -> (None):
    """L'échelle pour choisir le nombre de mines."""

    global sc_mines, sc_largeur, sc_hauteur

    sc_mines['from'] = 0
    sc_mines['to'] = sc_largeur.get() * sc_hauteur.get()
    sc_mines['orient'] = 'horizontal'
    sc_mines['label'] = 'Mines:'

    # Place une valeur de base pour le nombre de mines
    # La première partie est donc générée avec MINES_DEPART mines sur 5x5
    sc_mines.set(MINES_DEPART)

    sc_mines.grid(column=0, row=3, pady=5)


def button_rejouer() -> (None):
    """Le bouton permettant de relancer une partie."""

    # Le bouton pour rejouer
    but_rejouer['text'] = 'Nouvelle partie'
    but_rejouer['command'] = actions.command_rejouer

    but_rejouer.grid(column=0, row=4, pady=5)


def frame_reglages(col=1, lig=0) -> (None):
    """Le panneau des réglages de base du jeu, pour que l'utilisateur puisse \
personnaliser sa partie.

Arguments:
 - col=1        - int - la colonne de la racine où sera placé le panneau,
 - lig=0        - int - la ligne de la racine où sera placé le panneau."""

    # Le chronomètre
    label_chrono()

    # Les échelles pour les réglages
    scale_largeur()
    scale_hauteur()
    scale_mines()

    # Le bouton pour rejouer
    button_rejouer()

    fr_reglages.grid(column=col, row=lig)


# L'INTERFACE GÉNÉRALE ########################################################


def interface(titre: str, largeur_min: int, hauteur_min: int) -> (None):
    """Lance l'interface du jeu."""

    global fenetre

    # Initialise quelques bases de la fenêtre
    fenetre.minsize(largeur_min, hauteur_min)
    fenetre.title(titre)

    # Initialise le panneau de réglages
    frame_reglages()

    # Initialise le plateau de jeu et un terrain vide en même temps
    actions.command_rejouer()

    # Lance l'interface
    fenetre.mainloop()
