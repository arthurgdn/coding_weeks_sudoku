import numpy as np
from random import randint


def ligne(grid,i,k,t=-1):
    """
    vérifie les contraintes liées aux chiffres sur la même ligne
    """
    n = len(grid)
    for j in range(n):
        if grid[i][j] == k and j != t:
            return False
    return True

def colonne(grid,i,k,t = -1):
    """
    vérifie les contraintes liées aux chiffres sur la même colonne
    """
    n = len(grid)
    for j in range(n):
        if grid[j][i] == k and j != t:
            return False
    return True

def carré(grid,i,j,k):
    """
    vérifie les contraintes liées aux chiffres sur le même carré
    """
    n = len(grid)
    x0 = i - (i % 3)
    y0 = j - (j % 3)
    for x in range(3):
        for y in range(3):
            if grid[x0+x][y0+y] == k and (x0 + x) != i and (y0 + y) != j:
                return False
    return True

def suivant(i,j):
    """
    renvoie les coordonnées de la prochaine case à traiter dans la grille. (l'ordre est de gauche à droite, de haut en bas)
    """
    if j ==8:
        if i == 8:
            return (8,8)
        else:        
            return (i+1,0)
    else:
        return (i,j+1)


def next_case(grid,i,j):    
    """
    fonction récursive qui teste par ordre croissant les valeurs dans chaque case et revient en arrière dans le cas d'une incompatibilité
    """
    grid2 = np.copy(grid)
    if (grid[i][j] != 0):
        if i == j == 8:
            return (True,grid)
        else:
            i1,j1 = suivant(i,j)
            return next_case(grid,i1,j1)
    else:
        value = 1
        i1,j1 = suivant(i,j)
        s = False       
        while (not s) and value <= 9:            
            if ligne(grid,i,value) and colonne(grid,j,value) and carré(grid,i,j,value):
                grid2 = np.copy(grid)
                grid2[i][j] = value
                s,grid_f = next_case(grid2,i1,j1)               
                if not s:
                    value +=1
            else:
                value += 1        
        if value <= 9 :
            return (True,grid_f)
        else:
            return (False,grid2)



def next_case_random(grid,i,j):  
    """
    fonction récursive qui teste de manière aléatoire les valeurs dans chaque case et revient en arrière dans le cas d'une incompatibilité
    """  
    n = len(grid)
    grid2 = np.copy(grid)
    if (grid[i][j] != 0):
        if i == j == 8:
            return (True,grid)
        else:
            i1,j1 = suivant(i,j)
            return next_case(grid,i1,j1)
    else:
        i1,j1 = suivant(i,j)
        s = False  
        l_value = [1,2,3,4,5,6,7,8,9]     
        value = randint(0,8)
        while (not s) and l_value != []:            
            if ligne(grid,i,l_value[value]) and colonne(grid,j,l_value[value]) and carré(grid,i,j,l_value[value]):
                grid2 = np.copy(grid)
                grid2[i][j] = l_value[value]
                s,grid_f = next_case(grid2,i1,j1)               
                if not s:
                    del l_value[value]
                    value = randint(0,(len(l_value)-1))
            else:
                del l_value[value]
                value = randint(0,(len(l_value)-1))        
        if l_value != []:
            return (True,grid_f)
        else:
            return (False,grid2)


def resolve(grid):
    """ 
    résolution du sudoku
    """
    return next_case(grid,0,0)[1]


def resolve_random(grid):
    """
    résolution du sudoku avec une part d'aléatoire
    """
    return next_case_random(grid,0,0)[1]

def transform_grid(grid):
    """
    convertie le format de la grille, la representation des cases vides passe de '' à 0
    """
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j]=='':
                grid[i][j]=0
            else: grid[i][j] = grid[i][j]
    return grid


def empty_count(grid):
    """
    compte le nombre de case vide d'une grille
    """
    n = len(grid)
    count = 0
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                count += 1
    return count

def verif(grid):
    """
    vérifie si la grille donnée est résolue ou non
    """
    if not empty_count(grid) == 0:
        return False
    else:
        
        s = True
        for i in range(9):
            for j in range(9):
                print(i,j)
                print(s)
                s = s and ligne(grid,i,grid[i][j],j) and colonne(grid,j,grid[i][j],i) and carré(grid,i,j,grid[i][j])
        return s







ex  = [[9,5,0,0,0,0,0,4,8],[0,0,0,0,1,0,0,0,0],[0,6,3,2,0,4,9,1,0],[0,2,5,0,0,0,7,8,0],[3,8,0,5,0,9,0,2,4],[0,9,4,0,0,0,3,6,0],[0,4,9,7,0,3,8,5,0],[0,0,0,0,6,0,0,0,0],[2,1,0,0,0,0,0,7,3]]


ex2 =  [[0,6,0,8,9,3,0,4,0],[2,0,0,0,0,0,0,0,6],[0,0,3,2,0,1,7,0,0],[7,0,0,0,5,0,0,0,8],[3,0,8,1,7,6,5,0,4],[9,0,0,0,3,0,0,0,1],[0,0,5,6,0,9,4,0,0],[6,0,0,0,0,0,0,0,5],[0,9,0,5,2,7,0,1,0]]
sudoku=[['' ,[6],'' ,[8],[9],[3],'' ,[4],'' ],
        [[2],'' ,'' ,'' ,'' ,'' ,'' ,'' ,[6]],
        ['' ,'' ,[3],[2],'' ,[1],[7],'' ,'' ],
        [[7],'' ,'' ,'' ,[5],'' ,'' ,'' ,[8]],
        [[3],'' ,[8],[1],[7],[6],[5],'' ,[4]],
        [[9],'' ,'' ,'' ,[3],'' ,'' ,'' ,[1]],
        ['' ,'' ,[5],[6],'' ,[9],[4],'' ,'' ],
        [[6],'' ,'' ,'' ,'' ,'' ,'' ,'' ,[5]],
        ['' ,[9],'' ,[5],[2],[7],'' ,[1],'' ]]

sudoku2=[['','' ,'' ,'' ,[3],'' ,'' ,'' ,'' ],
        ['' ,'' ,[4],[8],'' ,[7],[6],'' ,'' ],
        [[3],[1],'' ,'' ,[5],'' ,'' ,[2],[7]],
        ['' ,[6],'' ,'' ,'' ,'' ,'' ,[1],'' ],
        ['' ,[7],[1],[9],'' ,[8],[2],[6],'' ],
        ['' ,[2],'' ,'' ,'' ,'' ,'' ,[9],'' ],
        [[1],[4],'' ,'' ,[8],'' ,'' ,[7],[9]],
        ['' ,'' ,[8],[5],'' ,[2],[3],'' ,'' ],
        ['' ,'' ,'' ,'' ,[9],'' ,'' ,'' ,'' ]]


sudoku3=[['' ,'' ,'' ,'' ,[8],'' ,'' ,'' ,'' ],
         [[8],'' ,'' ,'' ,[9],'' ,'' ,'' ,[3]],
         ['' ,'' ,[5],[2],[7],[3],[6],'' ,'' ],
         ['' ,[4],[1],'' ,'' ,'' ,[3],[7],'' ],
         [[7],'' ,'' ,'' ,'' ,'' ,'' ,'' ,[6]],
         ['' ,[6],[2],'' ,'' ,'' ,[8],[5],'' ],
         ['' ,'' ,[9],[8],[1],[7],[2],'' ,'' ],
         [[4],'' ,'' ,'' ,[5],'' ,'' ,'' ,[7]],
         ['' ,'' ,'' ,'' ,[2],'' ,'' ,'' ,'' ]]
#print(resolve(ex2))
#print(resolve_random(transform_grid(sudoku)))
#print(resolve(transform_grid(sudoku2)))
#print(resolve(transform_grid(sudoku3)))



        

