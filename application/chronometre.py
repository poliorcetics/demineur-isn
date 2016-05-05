# -*- coding: utf-8 -*-

""" -- chronometre.py

class Chrono(self, racine **kwargs)
    
"""


import time as t
import tkinter as tk

class Chrono(tk.Label):
    """Dérive de tk.Label pour former un chronomètre qui une fois lancé continue
seul à tourner.

 - __init__(self, racine, **kwargs)         -> (None),
 - formate_temps(self)                      -> (str),
 - tourne_chrono(self)                      -> (None),
 - lance_chrono(self)                       -> (None),
 - stop_chrono(self)                        -> (None)
"""

    def __init__(self, racine, **kwargs) -> (None):
        tk.Label.__init__(self, racine, kwargs)

        # Le temps écoulé depuis le lancement du chronomètre
        self.temps_ecoule = 0
        # Détermine l'état du chronomètre
        self.chrono_actif = False

        # Initialise l'affichage du temps écoulé
        self.__setitem__('text', '00:00:00')

    def formate_temps(self) -> (str):

        temp = t.strptime(str(self.temps_ecoule), '%S')
        
        return t.strftime('%H:%M:%S', temp)
        
    def tourne_chrono(self) -> (None):
        """Fonction récursive (via appel à after) faisant tourner le chronomètre
chaque seconde à partir de son lancement, si il doit toujours être actif."""

        if self.chrono_actif:

            # Mise à jour de l'affichage du temps écoulé
            self.__setitem__('text', self.formate_temps())
            # Ajout d'une seconde
            self.temps_ecoule += 1
            # Attente d'une seconde avant l'appel récursif
            self.after(1000, self.tourne_chrono)

    def stop_chrono(self) -> (None):
        """Stoppe le chrono s'il est lancé, sinon ne fait rien."""
        self.chrono_actif = False

    def lance_chrono(self) -> (None):
        """Lance le chrono s'il n'est pas déjà actif, sinon ne fait rien."""

        # Vérifie l'état du chronomètre
        if not self.chrono_actif:
            # Remise à zéro des paramètres
            self.temps_ecoule = 0
            self.chrono_actif = True

            # Lancement du chronomètre
            self.tourne_chrono()


# Code exécuté lors de tests
if __name__ == '__main__':

    fen = tk.Tk()
    ch = Chrono(fen)
    bt1 = tk.Button(fen, text='on', command=ch.lance_chrono)
    bt2 = tk.Button(fen, text='off', command=ch.stop_chrono)
    
    bt1.pack()
    bt2.pack()
    ch.pack()
    fen.mainloop()
