# -*- coding: utf-8 -*-

""" -- chronometre.py

CLASSE

 - class Chrono(self, racine **kwargs)                          <- (tk.Label).

FONCTION

 - formate_temps(temps: int)                                    -> (str).
"""

import tkinter as tk


class Chrono(tk.Label):
    """Dérive de tk.Label pour former un chronomètre qui une fois lancé,
 continue de tourner en se mettant à jour toutes les secondes.

 - __init__(self, racine, **kwargs)         -> (None),
 - tourne_chrono(self)                      -> (None),
 - lance_chrono(self)                       -> (None),
 - stop_chrono(self)                        -> (None)
"""

    def __init__(self, racine, **kwargs) -> (None):
        """Initialise le chronomètre.

Arguments:
 - racine           - tk.Tk() / tk.Canvas() / tk.Frame() - zone d'affichage
 - **kwargs         - divers arguments ajoutables à tk.Label.__init__
"""
        # Chrono est donc un objet tk.Label avec toutes les méthodes associées
        tk.Label.__init__(self, racine, kwargs)
        # Le temps écoulé depuis le lancement du chronomètre
        self.temps_ecoule = 0
        # Détermine l'état du chronomètre
        self.chrono_actif = False
        # L'ID utilisée pour le self.after()
        self._after = None
        # Initialise l'affichage du temps écoulé (possible car on dérive d'un
        # tk.Label)
        self.__setitem__('text', '0h 0min 0s')

    def tourne_chrono(self) -> (None):
        """Fonction récursive (via appel à after) faisant tourner le
chronomètre chaque seconde à partir de son lancement, si il doit toujours être
actif."""

        if self.chrono_actif:
            # Mise à jour de l'affichage du temps écoulé
            self.__setitem__('text', formate_temps(self.temps_ecoule))
            # Ajout d'une seconde
            self.temps_ecoule += 1
            # Attente d'une seconde avant l'appel récursif
            self._after = self.after(1000, self.tourne_chrono)

    def stop_chrono(self) -> (None):
        """Stoppe le chrono s'il est lancé, sinon ne fait rien."""
        self.chrono_actif = False
        # On utilise l'ID du self.after pour l'arr^ter au besoin
        if self._after is not None:
            self.after_cancel(self._after)
            self._after = None

    def lance_chrono(self) -> (None):
        """Lance le chrono s'il n'est pas déjà actif, sinon ne fait rien."""

        # Vérifie l'état du chronomètre
        if not self.chrono_actif:
            # Remise à zéro des paramètres
            self.temps_ecoule = 0
            self.chrono_actif = True
            # Lancement du chronomètre
            self.tourne_chrono()


def formate_temps(temps: int) -> (str):
    """Prends un temps en seconde en entrée, le retourne sous la forme
heures:minutes:secondes."""

    heures = temps // 3600
    minutes = (temps - heures * 3600) // 60
    secondes = temps - (heures * 3600 + minutes * 60)

    return "%sh %smin %ss" % (heures, minutes, secondes)


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
