# Fichier de rapport du travail d'**Alexis**

_______________________________________________________________________________

## 09/02/2016:

Création de `terrain.py` et mise en place du fichier `rapport-alexis.md` ainsi que du `README.md`.

_______________________________________________________________________________

## 10/02/2016:

#### 1) MàJ de terrain.py:

Fonction `place_nombre_mines()` créée, elle permet de modifier `self.terrain` afin de le retourner en ayant placé dans chaque case le nombre de mines adjacentes.

**Problèmes rencontrés:**

Au départ, l'utilisation de ce type de code:
```python
try:
    if self.terrain[y-1][x-1]:
        self.terrain[y][x] += 1
except IndexError:
    pass
```
entrainait des erreurs d'index mal placés : lorsque y-1 et/ou x-1 devenaient égaux à -1, on pouvait tomber sur une mine hors champ ou compter une deuxième fois une mine qui aurait été comptée par un autre test.

J'ai ensuite testé:
```python
try:
    if self.terrain[abs(y-1)][abs(x-1)]:
        self.terrain[y][x] += 1
except IndexError:
    pass
```
Mais dans ce cas là, on comptait environ deux fois chaque mine présente autour des cases placées sur les lignes/colonnes extérieures.

J'ai donc ensuite utilisé cela comme solution qui rendrait le code à la fois compact, lisible et fonctionnel:
```python
# Si y-1 ou x-1 = -1, on risque d'accéder au mauvais élément de
# self.terrain lors de la vérification de l'entourage de la case
# donc on le place volontairement en dehors des possibilités
# d'accès afin de lever une erreur et d'ajouter un 0 au lieu
# d'un potentiel 9 lors de la vérification
y_moins = y - 1 if y - 1 >= 0 else self.hauteur + 1
x_moins = x - 1 if x - 1 >= 0 else self.largeur + 1

entourage = [] # L'entourage de la case vérifiée

# Si la case n'est pas une mine, on procède à la vérification
# Pour cela, on vérifie les 8 cases l'entourant et on ajoute
# leur contenu à 'entourage' si elles sont accessibles
# (pas d'IndexError), sinon 0 (pas une mine)
if self.terrain[y][x] < 9:                    

    try: entourage.append(self.terrain[y_moins][x_moins])
    except IndexError: entourage.append(0)

    try: entourage.append(self.terrain[y_moins][x])
    except IndexError: entourage.append(0)

    try: entourage.append(self.terrain[y_moins][x+1])
    except IndexError: entourage.append(0)

    try: entourage.append(self.terrain[y][x+1])
    except IndexError: entourage.append(0)

    try: entourage.append(self.terrain[y+1][x+1])
    except IndexError: entourage.append(0)

    try: entourage.append(self.terrain[y+1][x])
    except IndexError: entourage.append(0)

    try: entourage.append(self.terrain[y+1][x_moins])
    except IndexError: entourage.append(0)

    try: entourage.append(self.terrain[y][x_moins])
    except IndexError: entourage.append(0)

    # En comptant le nombre de 9 dans l'entourage, on obtient le
    # nombre de mines. On passe cette valeur à la case vérifiée.
    self.terrain[y][x] = entourage.count(9)
```

#### 2) MàJ de terrain.py:

Correction d’une cause possible de boucle infinie dans la fonction `Terrain.place_mine()` lorsque trop de mines étaient demandées par rapport à la taille du terrain.

**L'erreur:**
```python
# Tant que l'on a pas placé toutes les mines demandées
while mines < nombre_mines:
```
Ce code pose un risque potentiel d'erreur car il était possible jusque là de demander un nombre de mines supérieur à la taille du terrain et donc de créer une boucle infinie lors de la génération du terrain.

**La correction:**
```python
# Si l'on demande trop de mines, on indique que c'est impossible
if nombre_mines > self.largeur * self.hauteur: raise ValueError
```
Si le nombre de mines demandées est trop grand pour le terrain, on lève une erreur pour l'indiquer.

_______________________________________________________________________________

## 14/02/2016:

#### 1) Création de constantes.py:

Création du fichier `constantes.py` qui contient les constantes représentant les différents états possibles d'une case.

#### 2) MàJ de terrain.py:

+ Ajout d’une fonction pour placer un drapeau
+ Ajout d’une fonction pour supprimer un drapeau
+ Ajout d’une fonction qui retourne l’entourage d’une case donnée
+ Prise en compte des constantes définies dans `constantes.py`
+ Ajout d'une variable qui sauvegarde le terrain miné avec ses cases inconnues
+ Ajout d'une variable qui sauvegarde le terrain complet (miné avec entourage calculé) 
+ Affichage du terrain remanié

#### 3) MàJ de actions_user.py:

+ Mise à jour de la documentation/ des commentaires.

_______________________________________________________________________________

## 18-19/02/2016

#### 1) MàJ de constantes.py, ajout des ressources, premiière version de l'interface

Ajout des constantes suivantes dans `constantes.py`:
+ `NOM_APP`: le nom de l'application (son titre),
+ `LARGEUR_MIN`: la largeur minimale de la fenêtre de l'application, en pixel,
+ `HAUTEUR_MIN`: la hauteur minimale de la fenêtre de l'application, en pixel,
+ `MIN_CASES`: le nombre minimal de cases sur le plateau, longueur comme largeur,
+ `MAX_CASES`: le nombre maximal de cases sur le plateau, longueur comme largeur.

Ajout des ressources (images uniquement pour le moment) qui seront affichées sur le plateau:
+ Création de 5 dossiers, seuls les dossiers `15`, `30`,`45` et `60` sont utilisés lors du déroulement du jeu, le dossier `original` sert à refaire les images en cas de besoin,
+ Ajout des images suivantes: `base.gif`, `drapeau.gif`, `mine.gif` et `mine_explose.gif`.

Ajout du fichier `interface.py`:
+ Ajout de la classe `Interface` qui contient les fonctions gérant l'interface. Pour le moment elle permet de:
    + Générer un plateau uniforme de taille 5x5 jusqu'à 30x30,
    + Choisir la taille de ce plateau entre ces deux bornes,
    + Régler le nombre de mines via une échelle (même s'il n'a aucune influence pour le moment) qui est mise à jour à chaque changement de la taille du plateau,
    + Regénérer un nouveau plateau grâce à un bouton.

La documentation intégrale a été réalisée.

#### 2) MàJ des ressources:

+ Ajout des images des cases `case_1.gif` à `case_8.gif`,
+ Coloration des images des cases `case_1.gif` à `case_8.gif` pour mieux représenter le danger autour d'elles.

Toutes les tailles ont été mise à jour.
