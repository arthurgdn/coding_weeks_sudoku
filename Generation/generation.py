from random import *
from Resolution.résolution import *
import numpy as np
from tkinter import *


def grid_full():
    """
    renvoie une grille de sudoku remplie
    """
    grid = np.zeros((9,9))
    count = 0
    while count < 15: #ajoute 15 valeur de manière aléatoire en respectant les contraintes du sudoku à une grille vide
        value = randint(1,9)
        x = randint(0,8)
        y = randint(0,8)
        if ligne(grid,x,value) and colonne(grid,y,value) and carré(grid,x,y,value) and grid[x][y]==0:            
            grid[x][y] = value
            count += 1
    grid = resolve_random(grid)
  
    return grid



def unicité(grid_ref,grid):
    """
    teste l'unicité d'une grille
    """
    for i in range(5): #on test plusieurs résolutions aléatoires et on compare par rapport à la grid full

        if False in (grid_ref == resolve_random(grid)):
            return False
    return True


def remove_value(grid,v,p_bar):
    """
    enlève des valeurs de la grille grid jusqu'à qu'il n'en reste plus que un nombre v et met à jour la barre de progression p_bar
    """
    def progress(p_bar,currentValue):
        """
        met à jour la barre de progression
        """
        p_bar["value"]=currentValue
    
    grid2 = np.copy(grid)
    count = 81
    count2 = 0
    while count > v:
        count2 += 1
        if count2 > 500:
            return (False,grid)
        
        p_bar.after(500, progress(p_bar,81-count)) #mise à jour de la barre de progression
        p_bar.update() 
        x = randint(0,8)
        y = randint(0,8)
        
        if grid2[x][y] != 0:
                     
            grid2[x][y] = 0
            if unicité(grid,grid2):
                count -= 1
            else:
                grid2[x][y] = grid[x][y]
    return (True,grid2)


def generation(diff,p_bar):
    """
    génère une grille de difficulté diff
    """
    if diff == "Facile":
        v = 32
        p_bar["maximum"] = 81-32
    elif diff == "Moyen":
        v = 27
        p_bar["maximum"] = 81-27
    else:
        v = 23
        p_bar["maximum"] = 81-23

    s = False
    while not s:
        grid = grid_full()
        print('ok')
        s,grid = remove_value(grid,v,p_bar)

    return grid

