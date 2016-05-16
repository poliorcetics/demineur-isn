# -*- coding : utf-8 -*-

""" -- actions_ordi.py

Les actions de l'ordinateur pendant une partie.

VARIABLES GLOBALES

 - nb_cases             - int - le nombre de cases sur le nouveau terrain,
 - nb_mines             - int - le nombre de mines sur le nouveau terrain,
 - nb_cases_vues        - int - le nombre de cases vues par le joueur,
 - fini                 - bool - l'état de finition de la partie.

FONCTIONS

 - verif_etat_partie(valeur_case: int)                      -> (bool or None),
 - reset(hauteur: int, largeur: int, mines: int)            -> (None).
"""

# l'interface de la fenêtre pour la fin de partie
import tkinter as tk
import tkinter.messagebox as mb
import interface as iu


# LES VARIABLES GLOBALES ######################################################


nb_cases = 0
nb_cases_vues = 0
nb_mines = 0
fini = False


# LES FONCTIONS ###############################################################


def verif_etat_partie(valeur_case: int) -> (bool or None):
    """Vérifie si la partie doit se terminer après un clic sur une case ou non.

Argument:
 - valeur_case      - int - la valeur de la case qui a été cliquée.

Modifie:
 - fini             - bool - Passe à True si la partie se termine à ce moment.

Retourne:
 - bool or None     - bool - True si la partie est gagné, False si la partie
                             est perdue, None si rien."""

    global fini

    def revele_plateau():
        """Révèle le plateau complet à la fin d'une partie."""
        for x, y in iu.cases_pos.keys():
            iu.maj_revele_case(x, y)

    # Si la partie n'est pas déjà finie
    if not fini:
        # Si la case est une mine, on fait perdre le joueur et on révèle le
        # plateau complet (les drapeaux sont remplacés par leur vraie valeur)
        if valeur_case == 9:
            fini = True
            iu.lb_chrono.stop_chrono()
            revele_plateau()
            mb.showinfo("Partie finie !", "Vous avez perdu ! :(")
            return False

        # Si le joueur a découvert toutes les cases non-minées, alors on
        # termine aussi la partie en le faisant gagner et on révèle les mines
        if nb_mines + nb_cases_vues == nb_cases:
            fini = True
            iu.lb_chrono.stop_chrono()
            revele_plateau()
            mb.showinfo("Partie finie !", "Vous avez gagné ! :D")
            return True


def reset(hauteur: int, largeur: int, mines: int) -> (None):
    """Remet à zéro les éléments qui vérifient que l'on a fini une partie.

Arguments:
 - hauteur      - int - la hauteur du nouveau terrain,
 - largeur      - int - la largeur du nouveau terrain,
 - mines        - int - le nombre de mines sur le nouveau terrain.

Modifie:
 - nb_cases             - int - le nombre de cases sur le nouveau terrain,
 - nb_mines             - int - le nombre de mines sur le nouveau terrain,
 - nb_cases_vues        - int = 0 - le nombre de cases vues par le joueur,
 - fini                 - bool = False - l'état de finition de la partie."""

    global nb_cases, nb_mines, nb_cases_vues, fini

    # On prépare les éléments pour pouvoir finir la partie
    nb_cases = hauteur * largeur
    nb_mines = mines
    nb_cases_vues = 0
    fini = False


if __name__ == "__main__":

    t = tk.Tk()

    def fin():
        fin_partie('yeh')

    btn = tk.Button(t, text='test', command=fin)
    btn.pack()

    t.mainloop()
