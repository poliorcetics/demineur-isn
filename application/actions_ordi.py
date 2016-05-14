# -*- coding : utf-8 -*-

""" -- actions_ordi.py
"""

import tkinter as tk
import interface as iu
import actions_joueur as actions

nb_cases = 0
nb_cases_vues = 0
nb_mines = 0
fini = False

def verif_etat_partie(valeur_case) -> (bool):

    global fini

    if not fini:
        if valeur_case == 9:
            fin_partie("Vous avez perdu ! :'(")
            fini = True
            return False

        if nb_mines + nb_cases_vues == nb_cases:
            fin_partie("Vous avez gagné ! :D")
            fini = True
            return True


def fin_partie(message: str) -> (None):

    toplevel_fen = tk.Toplevel()

    lb_message = tk.Label(master=toplevel_fen, text=message)
    lb_message.pack()
    
    btn_ok = tk.Button(master=toplevel_fen, text='Ok', command=toplevel_fen.destroy)
    btn_ok.pack()
    
    toplevel_fen.focus_force()


if __name__ == "__main__":

    t = tk.Tk()

    def fin():
        fin_partie('yeh')
    
    btn = tk.Button(t, text='test', command=fin)
    btn.pack()

    t.mainloop()
