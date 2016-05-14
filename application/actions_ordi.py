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
 - fin_partie(message: str)                                 -> (None),
 - reset(hauteur: int, largeur: int, mines: int)            -> (None).
"""

# l'interface de la fenêtre pour la fin de partie
import tkinter as tk
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
            fin_partie("Vous avez perdu ! :'(")
            fini = True
            revele_plateau()
            return False

        # Si le joueur a découvert toutes les cases non-minées, alors on
        # termine aussi la partie en le faisant gagner et on révèle les mines
        if nb_mines + nb_cases_vues == nb_cases:
            fin_partie("Vous avez gagné ! :D")
            fini = True
            revele_plateau()
            return True


def fin_partie(message: str) -> (None):
    """Affiche le message signalant la fin de partie.

Argument:
 - message      - str - le message de fin de partie."""

    # Une fenêtre pop-up
    toplevel = tk.Toplevel()

    # Le message de fin de partie
    lb_message = tk.Label(master=toplevel, text=message)
    lb_message.pack()

    # Le bouton pour fermer la fenêtre
    btn_ok = tk.Button(master=toplevel, text='Ok', command=toplevel.destroy)
    btn_ok.pack()

    # Force la focus sur cette pop-up
    toplevel.focus_force()


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
