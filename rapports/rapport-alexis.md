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

+ Ajout d’une fonction pour placer un drapeau,
+ Ajout d’une fonction pour supprimer un drapeau,
+ Ajout d’une fonction qui retourne l’entourage d’une case donnée,
+ Prise en compte des constantes définies dans `constantes.py`,
+ Ajout d'une variable qui sauvegarde le terrain miné avec ses cases inconnues,
+ Ajout d'une variable qui sauvegarde le terrain complet (miné avec entourage calculé),
+ Affichage du terrain remanié.

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

Toutes les tailles ont été mises à jour.

#### 3) Interface, v2

Mise à jour de l'interface qui est donc maintenant entièrement fonctionnelle pour ce qui est de la base du jeu. Il est désormais possible de jouer une partie sans provoquer de bug (mais toucher une mine ne fera pas perdre non plus)

**Problèmes rencontrés**:

+ La construction de fonctions pour mettre à jour les cases lors de clics a été difficile. Il a fallu faire face à un problème de référence dans `terrain.py`, où la variable `self.terrain_complet` était créée par simple copie, une modification de l'une entrainant une modification de l'autre, annulant tout l'intérêt de sauvegarde. L'utilisation de `copy.deepcopy` a permis de régler le problème.
+ Le stockage des cases lors de leur création a aussi été compliqué du fait qu'il est venu lorsque j'ai vu que la méthode `widget` existait pour les évènements.
+ Il a fallu créer une variable `self.pos_vues` dans `terrain.py` dans la classe `Terrain` pour retenir les cases découvertes et y empêcher le placement de drapeau.
+ Se rendre compte de l'inutilité de la constante `INCONNU` et de la variable `self.terrain_mine` a été long.
+ Se rappeler de l'existence de `actions_user.py` aussi.

**Code des deux fonctions ajoutées**:
```python
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
    # Si c'est une mine on affiche une mine (le fait d'avoir perdu n'est pas
    # encore pris en compte)
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

    # S'il y a déjà un drapeau, on le supprime et on remplace par l'ancienne
    # valeur
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
```
