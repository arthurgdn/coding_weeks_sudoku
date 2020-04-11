En ce qui concerne la résolution d'une grille de sudoku, nous avons testé deux méthodes :

    - une résolution assez brutale, qui consiste à procéder de manière récursive en faisant de nombreuses hypothèses sur les valeurs des différentes cases

    - une résolution basée sur le raisonnement humain utilisé pour résoudre un sudoku (malgré tout récursive)



## résolution brutale
Le principe est simple : on sélectionne la première case vide (en haut à gauche) et on y affecte une valeur qui ne contredise pas les valeurs déjà existantes dans la ligne, la colonne et le carré; on repète ensuite l'opération sur la case suivante.
On effectue ce processus récursif jusqu'à obtenir la grille résolue


## résolution 'humaine'
Une sous fonction intitulée resolution_naive utilise le raisonnement humain de résolution d'un sudoku et ne fait aucune hypothèse sur la valeur d'une case. Elle garde en mémoire les différentes possibilités de chaque case (sous forme de liste), et les met à jour dès qu'une case ne possede plus qu'une possibilité.
Cette fonction permet de résoudre des sudoku de difficultés facile à moyen, mais est dans l'incapacité de résoudre des grilles difficiles.
Pour permettre la résolution de toutes les grilles, il a fallu implementer cette fonction dans une fonction récursive, qui fait une supposition sur une case, puis éxécute la résolution naive, et recommence si nécessaire.




### comparaison du temps de résolution
Dans le dossier 'calcul_temps_resolution', se trouve un fichier 'difference_temps_resolution.py' qui permet, lors de l'éxécution, d'afficher un graphique représentant l'évolution du temps de résolution en fonction de la difficulté de la grille.
(La difficulté est simulée par le nombre de case remplie initialement avant la résolution).
Ce graphique est présent en capture d'écran dans le dossier 'calcul_temps_résolution'