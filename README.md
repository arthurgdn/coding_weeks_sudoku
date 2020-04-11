Sudoku : photographiez/resolvez

____________________________________________________________________________________________________________________________________________________________________________________


Dans le cadre de ce projet de coding weeks, nous avons pour but de réaliser un solveur de grilles de Sudoku. Ce solveur devra :
    
    - être capable de reconstruire numériquement une grille de sudoku à partir d'une photographie
    - résoudre la grille de sudoku et afficher celle-ci
    
Pour effectuer cette tâche, nous allons diviser le travail en trois parties : 
    
    1) L'interface graphique
    
    2) La résolution
    
    3) La reconnaissance
    
1) Cette partie (interface graphique) consiste en l'interface utilisateur du produit. Elle devra permettre à l'utilisateur de donner une photo de grille au programme pour que 
celle-ci soit traitée.En outre, l'interface graphique doit permettre d'afficher la grille et d'intéragir avec elle (changer des numéros par exemple).

2) Cette parte (résolution) comprend l'algorithme de résolution du sudoku. La grille de sudoku, représentée sous forme de liste de listes sera traitée par un algorithme pour
fournir à l'utilisateur une grille résolue affichée par l'interface graphique.

3) Cette partie (reconnaissance) consiste en la transformation d'une photographie de grille de sudoku en données numériques, traitables par les différents algorithmes et 
programmes cités plus-haut. Le but de cette partie est donc de construire une grille à partir de la photographie, en reconnaissant les cases vides et les nombres.

____________________________________________________________________________________________________________________________________________________________________________________
Modules utilisés :

- numpy
- openCV
- matplotlib
- operator
- random
- tkinter
- functools
- Pypi
____________________________________________________________________________________________________________________________________________________________________________________


Pour utiliser le programme, 

- Exécutez le fichier sudoku.py.

- Sélectionner "Saisir la grille" si vous voulez la rentrer manuellement, "Scanner la grille" si vous voulez résoudre le sudoku à partir d'une photo, "Générer la grille" si vous
voulez générer une grille. Si vous avez chosi de scanner une grille, sélectionnez si elle est écrite de facon manuscrite ou avec un ordinateur puis sélectionnez la.

- Vérifiez la qualité de la grille.

- Choisissez entre "Jouer" pour résoudre vous même la grille ou bien "Résoudre" pour compléter la grille.

____________________________________________________________________________________________________________________________________________________________________________________

Fonctionnalités suplémentaires : 

- Générer une grille selon trois niveaux de difficulté
- Donner des indices
- Faire des hypothèses dans des cases
- Jouer et résoudre le jeu "Hidato"
- 2 modèles de reconnaissance d'image pour plus de précision

____________________________________________________________________________________________________________________________________________________________________________________
Etudiants:

- Arthur Guédon
- Alexis Richard
- Thomas Pouplin
- Charles Guillard
- Lucas Sor
____________________________________________________________________________________________________________________________________________________________________________________

Ressources :

Traitement d'image : https://medium.com/@neshpatel/solving-sudoku-part-ii-9a7019d196a2 / https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html
Réseau de neuronnes : https://www.tensorflow.org/tutorials/quickstart/beginner
