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

#### 1) Création de constantes.py

Création du fichier `constantes.py` qui contient les constantes représentant les différents états possibles d'une case.

#### 2) MàJ de terrain.py:

+ Ajout d’une fonction pour placer un drapeau
+ Ajout d’une fonction pour supprimer un drapeau
+ Ajout d’une fonction qui retourne l’entourage d’une case donnée
+ Prise en compte des constantes définies dans `constantes.py`
+ Ajout d'une variable qui sauvegarde le terrain miné avec ses cases inconnues
+ Ajout d'une variable qui sauvegarde le terrain complet (miné avec entourage calculé) 
= Affichage du terrain remanié
