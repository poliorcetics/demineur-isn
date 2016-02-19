# -*- coding : utf-8 -*-

"""
TODO: binder le Terrain.terrain et le Interface.plateau -> dessine_plateau()
"""

import tkinter as tk

from constantes import *
from terrain import *
import actions_user as action

""" -- interface.py

Permet d'initialiser et de contrôler l'interface du programme.

classe:
    - Interface:
        - __init__(nom_app, largeur_min, hauteur_min, largeur, hauteur)
        - determine_taille_case()
        - maj_images()
        - maj_max_mines()
        - dessine_plateau()
        - dessine_case(x, y)
        - taille_scale(frame)
        - mines_scale(frame)
        - rejouer_button(frame)
        - reglages_frame()
        - nouveau_plateau()
"""



class Interface:
    """ >> classe Interface(Object)

INITIALISATION
 - nom_app : str - titre de l'application
 - largeur_min_fen : int - largeur minimale de la fenêtre en pixel
 - hauteur_min_fen : int - hauteur minimale de la fenêtre en pixel
 - largeur : int - largeur du terrain en case
 - hauteur : int - hauteur du terrain en case

VARIABLES
 - interface : Tk - la racine de la fenêtre
 - nouvelle_largeur : IntVar - la valeur de l'échelle de la largeur
 - nouvelle_hauteur : IntVar - la valeur de l'échelle de la hauteur
 - cases : list - liste des cases du plateau (objet Tk.Label)
 - taille_case : int - la taille de case à utiliser (15, 30, 45 ou 60) en pixel
 - chemin_images : str - le chemin vers le dossier contenant les images de la \
taille choisie
 - base, drapeau, mine, mine_explose, case_[0..8]: tk.PhotoImage - les images \
des différentes cases du jeu

MÉTHODES
 - __init__(nom_app, largeur_min, hauteur_min, largeur, hauteur)    -> None
 - determine_taille_case()                  -> int
 - maj_images()                             -> None
 - maj_max_mines()                          -> None
 - dessine_plateau()                        -> plateau, tk.Canvas
 - dessine_case(x, y)                       -> case, tk.Label
 - taille_scale(frame)                      -> None
 - mines_scale(frame)                       -> None
 - rejouer_button(frame)                    -> None
 - reglages_frame()                         -> frame, tk.Frame
 - nouveau_plateau()                        -> None
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

        # Mise en place des images
        self.cases = []
        self.maj_images()

        # Création du plateau de base
        self.plateau = self.dessine_plateau()

        # On active le Frame de réglages
        self.reglages = self.reglages_frame()

        print(self.cases)

        # Une fois que tout est configuré, on lance l'interface
        self.interface.mainloop()

    def determine_taille_case(self):
        """Adapte la taille des images aux nombres de cases du plateau.

Retourne un int: 15, 30, 45 ou 60 (taille des images utilisées, en pixel)."""
        
        if 10 <= max(self.hauteur, self.largeur) < 15: return 45
        
        if 15 <= max(self.hauteur, self.largeur) < 20: return 30

        if 20 <= max(self.hauteur, self.largeur): return 15

        return 60

    def maj_images(self):
        """Met à jour les images utilisées pour dessiner le plateau.
Appelée à chaque fois qu'un nouveau plateau est généré.
        """

        self.taille_case = self.determine_taille_case()
        self.chemin_images = 'ressources/%s/' % self.taille_case

        self.base = tk.PhotoImage(file='%sbase.gif' % self.chemin_images)
        self.drapeau = tk.PhotoImage(file='%sdrapeau.gif' % self.chemin_images)
        self.mine = tk.PhotoImage(file='%smine.gif' % self.chemin_images)
        self.mine_explose = tk.PhotoImage(file='%smine_explose.gif' \
                                          % self.chemin_images)
        self.case_0 = tk.PhotoImage(file='%scase_0.gif' % self.chemin_images)
        self.case_1 = tk.PhotoImage(file='%scase_1.gif' % self.chemin_images)
        self.case_2 = tk.PhotoImage(file='%scase_2.gif' % self.chemin_images)
        self.case_3 = tk.PhotoImage(file='%scase_3.gif' % self.chemin_images)
        self.case_4 = tk.PhotoImage(file='%scase_4.gif' % self.chemin_images)
        self.case_5 = tk.PhotoImage(file='%scase_5.gif' % self.chemin_images)
        self.case_6 = tk.PhotoImage(file='%scase_6.gif' % self.chemin_images)
        self.case_7 = tk.PhotoImage(file='%scase_7.gif' % self.chemin_images)
        self.case_8 = tk.PhotoImage(file='%scase_8.gif' % self.chemin_images)

    def maj_max_mines(self, e):
        """Met à jour le nombre maximum de mines sélectionnables à chaque \
changement de la largeur ou de la hauteur (via les scales de réglages).
        """

        self.largeur = self.nouvelle_largeur.get()
        self.hauteur = self.nouvelle_hauteur.get()

        self.nombre_mines.destroy()
        self.mines_scale(self.reglages)

    def dessine_plateau(self):
        """Dessine le plateau du jeu et y place les cases avec l'image de base."""

        self.maj_images()

        # Initialise le plateau du jeu
        plateau = tk.Canvas(self.interface,
                            width=self.largeur * self.taille_case,
                            height=self.hauteur * self.taille_case)

        plateau.grid(column=0, row=0, padx=10, pady=10)

        # Dessine les cases du jeu
        self.cases = [[self.dessine_case(plateau, x, y)
                      for x in range(self.largeur)]
                      for y in range(self.hauteur)]

        return plateau

    def dessine_case(self, racine, x, y):
        """Dessine une case simple."""

        case = tk.Label(racine,
                        relief='raised',
                        borderwidth=1,
                        image=self.base)

        case.grid(column=x, row=y)

        return case

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
        """Place les échelles pour choisir la largeur et la hauteur du plateau \
en nombre de cases. Elles sont automatiquement liées à self.maj_max_mines() \
pour mettre à jour l'échelle du choix du nombre de mines à chaque changement."""

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
        nouvelle_partie['command'] = self.nouveau_plateau
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


    def nouveau_plateau(self):
        """Regénère un plateau après avoir détruit l'ancien. Prend en compte \
les choix de hauteur et de largeur fait via les échelles."""

        self.largeur = self.nouvelle_largeur.get()
        self.hauteur = self.nouvelle_hauteur.get()

        self.plateau.destroy()
        self.plateau = self.dessine_plateau()







# Valeurs de test uniquement
if __name__ == '__main__':

    fenetre = Interface(NOM_APP, LARGEUR_MIN, HAUTEUR_MIN, 5, 5)
