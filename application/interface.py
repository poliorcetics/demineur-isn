# -*- coding : utf-8 -*-

""" -- interface.py

Permet d'initialiser et de contrôler l'interface du programme.

classe:
    - Interface:
        - __init__(nom_app, largeur_min, hauteur_min, largeur, hauteur)
        - maj_images()
        - maj_max_mines()
        - maj_case()
        - maj_drapeau()

        - dessine_plateau()
        - dessine_case(x, y)
        - taille_scale(frame)
        - mines_scale(frame)
        - rejouer_button(frame)
        - reglages_frame()

        - determine_taille_case()
"""

import tkinter as tk
from os import sep # pour gérer l'accès aux ressources sur Windows/Unix

from constantes import *
import actions_user as action


class Interface:
    """ >> classe Interface(Object)

INITIALISATION
 - nom_app : str - titre de l'application
 - largeur_min_fen : int - largeur minimale de la fenêtre en pixel
 - hauteur_min_fen : int - hauteur minimale de la fenêtre en pixel
 - largeur : int - largeur du terrain en case
 - hauteur : int - hauteur du terrain en case

VARIABLES
 - interface : Tk - la racine de la fenêtre du programme
 - nouvelle_largeur : IntVar - la valeur de l'échelle de la largeur
 - nouvelle_hauteur : IntVar - la valeur de l'échelle de la hauteur
 - cases : dict - dictionnaire des cases du plateau. Forme: {Tk.Label: (x, y)}
 - taille_case : int - la taille de case à utiliser (15, 30, 45, 60) en pixel
 - chemin_images : str - le chemin vers le dossier contenant les images de \
la taille choisie
 - base, drapeau, mine, mine_explose : tk.PhotoImage - les images des \
différentes cases du jeu
 - cases_img : list - listes les cases chiffrées (0 à 8), tk.PhotoImage
 - terrain : Terrain - un terrain généré dans terrain.py

MÉTHODES
 - __init__(nom_app, largeur_min, hauteur_min, largeur, hauteur)    -> None

 - maj_images()                             -> None
 - maj_max_mines()                          -> None
 - maj_case()                               -> None
 - maj_drapeau()                            -> None

 - dessine_plateau()                        -> plateau, tk.Canvas
 - dessine_case(x, y)                       -> case, tk.Label
 - taille_scale(frame)                      -> None
 - mines_scale(frame)                       -> None
 - rejouer_button(frame)                    -> None
 - reglages_frame()                         -> frame, tk.Frame

 - determine_taille_case()                  -> int
"""

    def __init__(self, nom_app, largeur_min_fen, hauteur_min_fen,
                 largeur, hauteur):
        """Initialisation:
 - nom_app : str - titre de l'application
 - largeur_min_fen : int - largeur minimale de la fenêtre en pixel
 - hauteur_min_fen : int - hauteur minimale de la fenêtre en pixel
 - largeur : int - largeur du terrain en case
 - hauteur : int - hauteur du terrain en case
"""

        # Création de la fenêtre principale
        self.interface = tk.Tk()
        self.interface.minsize(largeur_min_fen, hauteur_min_fen)
        self.interface.title(nom_app)

        # Variables du plateau
        self.largeur = largeur
        self.hauteur = hauteur
        self.nouvelle_largeur = tk.IntVar(self.interface)
        self.nouvelle_hauteur = tk.IntVar(self.interface)

        # Mise en place des images et des cases
        self.cases = {}
        self.maj_images()

        # Préparation du jeu
        self.terrain = None

        # On active le Frame de réglages
        self.reglages = self.reglages_frame()

        # Création du plateau de base
        self.plateau = self.dessine_plateau()

        # Une fois que tout est configuré, on lance l'interface
        self.interface.mainloop()

    # ÉVÈNEMENTS ##############################################################

    def maj_images(self):
        """Met à jour les images utilisées pour dessiner le plateau.
Appelée à chaque fois qu'un nouveau plateau est généré.
        """

        self.taille_case = self.determine_taille_case()
        self.chemin_images = 'ressources%s%s%s' % (sep, self.taille_case, sep)

        self.base = tk.PhotoImage(file='%sbase.gif' % self.chemin_images)
        self.drapeau = tk.PhotoImage(file='%sdrapeau.gif' % self.chemin_images)
        self.mine = tk.PhotoImage(file='%smine.gif' % self.chemin_images)
        self.mine_explose = tk.PhotoImage(file='%smine_explose.gif'
                                          % self.chemin_images)

        self.cases_img = [
            tk.PhotoImage(file='%scase_0.gif' % self.chemin_images),
            tk.PhotoImage(file='%scase_1.gif' % self.chemin_images),
            tk.PhotoImage(file='%scase_2.gif' % self.chemin_images),
            tk.PhotoImage(file='%scase_3.gif' % self.chemin_images),
            tk.PhotoImage(file='%scase_4.gif' % self.chemin_images),
            tk.PhotoImage(file='%scase_5.gif' % self.chemin_images),
            tk.PhotoImage(file='%scase_6.gif' % self.chemin_images),
            tk.PhotoImage(file='%scase_7.gif' % self.chemin_images),
            tk.PhotoImage(file='%scase_8.gif' % self.chemin_images)]

    def maj_max_mines(self, e):
        """Met à jour le nombre maximum de mines sélectionnables à chaque \
changement de la largeur ou de la hauteur (via les scales de réglages)."""

        self.largeur = self.nouvelle_largeur.get()
        self.hauteur = self.nouvelle_hauteur.get()

        self.nombre_mines.destroy()
        self.mines_scale(self.reglages)

    def maj_case(self, c):
        """Lors d'un clic gauche sur une case, celle-ci est révélée si elle \
n'est pas un drapeau."""

        # On récupère la case cliquée, ses coordonnées et la case du terrain
        # correspondante
        case = c.widget

        x = self.cases[case][0]
        y = self.cases[case][1]

        valeur_case = self.terrain.terrain[y][x]

        # S'il y a un drapeau, on ne fait rien
        if valeur_case == DRAPEAU:
            return
        # Si ce n'est pas un drapeau, alors on ajoute la case à la liste des
        # cases du terrain vues
        # Si c'est une mine on affiche une mine (le fait d'avoir perdu n'est
        # pas encore pris en compte)
        elif valeur_case == MINE:
            case['image'] = self.mine
            self.terrain.pos_vues.append((x, y))
            return
        # Si ce n'est ni une mine ni un drapeau, on affiche la case chiffrée
        # correspondante
        else:
            case['image'] = self.cases_img[valeur_case]
            self.terrain.pos_vues.append((x, y))
            return

    def maj_drapeau(self, c):
        """Place ou supprime un drapeau si il est possible d'en placer/\
supprimer un."""

        # On récupère la case cliquée, ses coordonnées et la case du terrain
        # correspondante
        case = c.widget

        x = self.cases[case][0]
        y = self.cases[case][1]

        valeur_case = self.terrain.terrain[y][x]

        # S'il y a déjà un drapeau, on le supprime et on remplace par
        # l'ancienne valeur
        if valeur_case == DRAPEAU:
            case['image'] = self.base
            self.terrain.terrain[y][x] = self.terrain.terrain_complet[y][x]
            return

        # S'il ny'a pas de drapeau et que la case est encore cachée, on peut
        # placer un drapeau
        if not ((x, y) in self.terrain.pos_vues):
            case['image'] = self.drapeau
            self.terrain.terrain[y][x] = DRAPEAU
            return

    # ÉLÉMENTS DE L'INTERFACE #################################################

    def dessine_plateau(self):
        """Dessine le plateau du jeu et y place les cases avec l'image de base.
        """

        # On supprime self.plateau s'il existe déjà afin de le 'nettoyer'
        try: self.plateau.destroy()
        except: pass

        self.largeur = self.nouvelle_largeur.get()
        self.hauteur = self.nouvelle_hauteur.get()

        self.maj_images()
        self.cases.clear()

        # Initialise le plateau du jeu
        plateau = tk.Canvas(self.interface,
                            width=self.largeur * self.taille_case,
                            height=self.hauteur * self.taille_case)

        plateau.grid(column=0, row=0, padx=10, pady=10)

        # Dessine les cases du jeu
        for y in range(self.hauteur):
            for x in range(self.largeur):
                # Dessine la case de coordonnées (x, y)
                case = self.dessine_case(plateau, x, y)
                # Associe la case à ses coordonnées (x, y)
                self.cases[case[0]] = case[1]

                del case

        # Génère un terrain adapté à la grille choisie
        self.terrain = action.nouveau_terrain(
            self.largeur,
            self.hauteur,
            self.nombre_mines.get())

        return plateau

    def dessine_case(self, racine, x, y):
        """Dessine une case simple."""

        case = tk.Label(racine,
            borderwidth=1,
            relief='sunken',
            image=self.base)

        # Lie les cases aux actions possible
        case.bind('<Button-1>', self.maj_case)
        case.bind('<Button-2>', self.maj_drapeau)

        case.grid(column=x, row=y)

        return case, (x, y)

    def mines_scale(self, racine):
        """Place l'échelle pour choisir le nombre de mines dans la partie."""

        # Pour choisir le nombre de mines
        self.nombre_mines = tk.Scale(racine)
        self.nombre_mines['from'] = 0
        self.nombre_mines['to'] = self.hauteur * self.largeur
        self.nombre_mines['orient'] = 'horizontal'
        self.nombre_mines['label'] = 'Mines:'
        self.nombre_mines.grid(column=0, row=2, pady=5)

    def taille_scale(self, racine):
        """Place les échelles pour choisir la largeur et la hauteur du \
plateau en nombre de cases. Elles sont automatiquement liées à \
self.maj_max_mines() pour mettre à jour l'échelle du choix du nombre de mines \
à chaque changement."""

        # Pour choisir le nombre de case en largeur
        self.choix_largeur = tk.Scale(racine)
        self.choix_largeur['from'] = MIN_CASES
        self.choix_largeur['to'] = MAX_CASES
        self.choix_largeur['orient'] = 'horizontal'
        self.choix_largeur['label'] = 'Largeur:'
        self.choix_largeur['variable'] = self.nouvelle_largeur
        self.choix_largeur.bind('<ButtonRelease>', self.maj_max_mines)
        self.choix_largeur.grid(column=0, row=0, pady=5)

        # Pour choisir le nombre de case en hauteur
        self.choix_hauteur = tk.Scale(racine)
        self.choix_hauteur['from'] = MIN_CASES
        self.choix_hauteur['to'] = MAX_CASES
        self.choix_hauteur['orient'] = 'horizontal'
        self.choix_hauteur['label'] = 'Hauteur:'
        self.choix_hauteur['variable'] = self.nouvelle_hauteur
        self.choix_hauteur.bind('<ButtonRelease>', self.maj_max_mines)
        self.choix_hauteur.grid(column=0, row=1, pady=5)

    def rejouer_button(self, racine):
        """Place le bouton permettant de relancer une partie."""

        # Le bouton pour rejouer
        nouvelle_partie = tk.Button(racine)
        nouvelle_partie['text'] = 'Nouvelle partie'
        nouvelle_partie['command'] = self.dessine_plateau
        nouvelle_partie.grid(column=0, row=3, pady=5)

    def reglages_frame(self):
        """Place le Frame qui contient l'ensemble des outils de réglages du \
jeu."""

        # Defini le tk.Frame() qui va contenir les outils de réglages du jeu
        frame = tk.Frame(self.interface)

        # Les échelles pour les réglages
        self.taille_scale(frame)
        self.mines_scale(frame)

        # Le bouton pour rejouer
        self.rejouer_button(frame)

        frame.grid(column=1, row=0)

        return frame

    # AUTRES MÉTHODES #########################################################

    def determine_taille_case(self):
        """Adapte la taille des images aux nombres de cases du plateau.

Retourne un int: 15, 30, 45 ou 60 (taille des images utilisées, en pixel)."""

        if 10 <= max(self.hauteur, self.largeur) < 15: return 45

        if 15 <= max(self.hauteur, self.largeur) < 20: return 30

        if 20 <= max(self.hauteur, self.largeur): return 15

        return 60

# Valeurs de test uniquement
if __name__ == '__main__':

    Interface(NOM_APP, LARGEUR_MIN, HAUTEUR_MIN, 5, 5)
