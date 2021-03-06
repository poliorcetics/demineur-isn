# Fichier de rapport du travail d'Alexis

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

#### 1) MàJ de constantes.py, ajout des ressources, première version de l'interface

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

#### 4) Corrections

+ Du fait de l'ajout de l'interface, il n'est plus possible de demander le placement de plus de mines que possibles, on peut donc retirer le test correspondant dans le fichier `terrain.py`
+ Passage de l'ensemble des fichiers `*.py` en mode `PEP-8 compliant`. (Oui c'est pour le fun)

_______________________________________________________________________________

## 20/02/2016

#### 1) Passage en impératif

Recodage de l'ensemble du projet pour tout passer en `programmation impérative`. Utilisation de `variables globales` avec des `fonctions` en lieu et place de `classes`.

**Pourquoi ?**:

L'usage des `classes` était difficile et mal pensé, notre niveau pas assez élevé pour permettre de corriger cela rapidement et de plus l'usage de `POO` ici n'était pas nécessaire.

**Ce qui a été fait**:

J'ai supprimé les classes `Terrain` et `Interface` et les aient remplacées par des `variables globales` et des `fonctions` codées plus intelligemment et plus clairement. Le format de la documentation a également été revu, elle est donc maintenant (normalement) **très très très claire** et je l'espère complète (ce sera corrigé si ce n'est pas le cas).

J'ai aussi commencé à lier l'interface / le générateur de terrain avec les actions de du joueur, via le fichier `actions_joueur.py`. (Ceci était nécessaire pour arriver au même endroit que là où nous en étions en version `POO`.)

**Problèmes recontrées**:

À côté de toute la réflexion à faire pour réécrire le code, j'ai rencontré un `bug` bien étrange (et connu du net, stackoverflow a plus d'une quinzaine de sujet dessus).

Ce code là:
```python
cases_img = {
    0:        tk.PhotoImage(file='%scase_0.gif' % chemin),
    1:        tk.PhotoImage(file='%scase_1.gif' % chemin),
    2:        tk.PhotoImage(file='%scase_2.gif' % chemin),
    3:        tk.PhotoImage(file='%scase_3.gif' % chemin),
    4:        tk.PhotoImage(file='%scase_4.gif' % chemin),
    5:        tk.PhotoImage(file='%scase_5.gif' % chemin),
    6:        tk.PhotoImage(file='%scase_6.gif' % chemin),
    7:        tk.PhotoImage(file='%scase_7.gif' % chemin),
    8:        tk.PhotoImage(file='%scase_8.gif' % chemin),
    BASE:     tk.PhotoImage(file='%sbase.gif' % chemin),
    DRAPEAU:  tk.PhotoImage(file='%sdrapeau.gif' % chemin),
    MINE:     tk.PhotoImage(file='%smine.gif' % chemin),
    PERDU:    tk.PhotoImage(file='%sperdu.gif' % chemin)
}
```
ne fonctionnera jamais car les images sont supprimées par le `Garbage Collector` (il ne détecte pas de parent), malgré le fait qu'elles soient référencées dans un dictionnaire. La correction est assez simple, il suffit de rajouter un parent:
```python
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
```

**Fin de la réécriture**:

Tout est de nouveau fonctionnel mais cette fois sans `POO`. Pour obtenir la même fenêtre avec les mêmes options qu'auparavant (placement/suppression de drapeau, découverte des cases, etc...) il faut lancer le fichier `actions_joueur.py` et non plus le fichier `interface.py`.

_______________________________________________________________________________

## 01/03/2016

#### 1) Propagation de la révélation des cases

Codage de la fonction suivante:
```python
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
```
Cette fonction permet de propager la révélation des cases si nécessaire. Elle fonctionne récursivement.

**Problèmes rencontrés**:

J'ai rencontré deux problèmes principaux lors du codage de cette fonction.

 1. **Problème de référencement des cases**: La création de la variable `cases_pos` a été imposée car la méthode en sens inverse posait un problème lors de la récursion pour le référencement des cases et donc les modifications d'images nécessaires.
 2. **Problème de récursion**: La première version impliquait un grand nombre de boucles inutiles et posait son `return` trop tard, amenant une erreur de récursion trop importante car elle ne vérifiait pas assez tôt si la case avait été vue auparavant, causant une boucle infinie en repassant sans arrêt sur les mêmes cases.

 L'implémentation de cette fonction a permis une grande simplification de la fonction `event_case(c: tk.Event) -> (None)` il suffit maintenant d'appeler la fonction `maj_revele_case(x: int, y: int) -> (None)` si la case n'est pas un drapeau pour gérer tout les cas actuels.

_______________________________________________________________________________

## 10/03/2016

##### 1) Gestion des différents clics selon les OS.

Nous avons trouvé que sous Windows, le clic-droit semble être `<Button-3` tandis que sous OS X (et probablement tous les systèmes Unix), il s'agit de `<Button-2>`. Nous avons donc ajouté une gestion du clic-droit en fonction de l'OS dans le fichier `interface.py`, dans la fonction générant une case (`label_case(racine: tk.Canvas, x: int, y: int) -> (tk.Label)`):

```python
# Pour Mac/Linux/Autres unix
if name == 'posix':
    case.bind('<Button-2>', event_drapeau)
# Pour Windows
else:
    case.bind('<Button-3>', event_drapeau)
```
