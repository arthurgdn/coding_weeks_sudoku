import sys
sys.path.append('../Resolution')                #permet les import provenant d'autres dossiers
from resolution_optimisée import *
from résolution_sous_optimal import *
sys.path.append('..')
from generation import *
from base_de_grilles import *
import random
from time import time
import numpy as np
import matplotlib.pyplot as plt

#pour rappel : 
#    - la fonction resolve correspond à un résolution récursives assez brutales avec hypothèse systématique sur la valeur des cases
#    - la fonction resolution correspond à une résolution basée sur la méthode humaine de résolution de sudoku


# Le but de se fichier est de tracer un graphique représentant l'évolution du temps de résolution 
# en fonction du nombre de cases remplies avant la résolution (pour les deux fonctions)




def grille_aleatoire(nb_cases_non_vides):
    """renvoie une grille générée aléatoirement avec nb_cases_non_vides"""
    choix_aleatoire = randint(0,len(liste_grilles)-1)
    grille = liste_grilles[choix_aleatoire]             #on utilise le fichier base_de_grilles.py
    nb_cases_vides = 81 - nb_cases_non_vides            #qui contient des grilles valides déja enregistrées
    compteur=0
    while compteur < nb_cases_vides:
        i = randint(0,8)
        j = randint(0,8)
        if grille[i][j] != 0:
            grille[i][j]=0
            compteur+=1
    return(grille)

def temps_necessaire(nb_cases_non_vides):
    """renvoie le temps necessaire à la résolution d'une grille aleatoire avec nb cases non vide par les deux méthodes de résolution"""
    temps_fct_resolve=[]          
    temps_fct_resolution=[]       
    grille = grille_aleatoire(nb_cases_non_vides)       
    
    temps_initial_1=time()                                  #utilisation du module time
    resolve(grille)                                         #pour connaitre le temps necessaire à la résolution
    temps_final_1=time()
    temps_fct_resolve = temps_final_1 - temps_initial_1

    grille=int_to_string(grille)            #changement de format necessaire pour utiliser la fonction résolution
    temps_initial_2=time()
    resolution(grille)
    temps_final_2=time()
    temps_fct_resolution = temps_final_2 - temps_initial_2
    return((temps_fct_resolve,temps_fct_resolution))

######### enregistrment de nombreux calculs ##########
# les calculs sont longs pour calculer les temps, on enregistre donc les temps dans deux dictionnaires stockés dans le fichier temps.txt
def dic_temps_vide():
    dic={}
    for i in range(23,81):
        dic[i]=[]
    return(dic)

def remplissage(nb_essais,nb_cases_non_vides):
    """remplie les dictionnaires present dans le fichier temps.txt avec les temps de résolution des deux fonctions pour une grille avec nb_cases_non_vides"""
    with open('temps.txt','r') as fichier:
        dic_temps_resolve = eval(fichier.readline())            #.readline() renvoie une chaine de caractère contenant le dictionnaire
        dic_temps_resolution = eval(fichier.readline())
    for i in range(nb_essais):
        (temps_resolve,temps_resolution)=temps_necessaire(nb_cases_non_vides)
        dic_temps_resolve[nb_cases_non_vides].append(temps_resolve)
        dic_temps_resolution[nb_cases_non_vides].append(temps_resolution)
    with open('temps.txt','w') as fichier : 
        fichier.write(str(dic_temps_resolve))
        fichier.write('\n')
        fichier.write(str(dic_temps_resolution))

def remplissage_plage(debut,fin):
    """rempli le dictionnaire du fichier temps.txt dans la plage [debut,fin] (fin compris)"""
    for nb_cases_non_vides in range(fin, debut-1, -1):
        remplissage(1,nb_cases_non_vides)
        print(nb_cases_non_vides)

#remplissage_plage(23,80)


############## affichage sous forme de graphique ##############
def graphique():
    liste_nb_cases_non_vides=[]
    liste_temps_resolve=[]
    liste_temps_resolution=[]
    with open('temps.txt','r') as fichier:
        dic_temps_resolve = eval(fichier.readline())            
        dic_temps_resolution = eval(fichier.readline())
    for k in range(23,81):
        for temps in dic_temps_resolve[k]:
            liste_nb_cases_non_vides.append(k)          #création de listes utilisable pour faire un nuage de points avec plt.scatter
            liste_temps_resolve.append(temps)
        for temps in dic_temps_resolution[k]:
            liste_temps_resolution.append(temps)
    plt.subplot(2,1,1)
    plt.scatter(liste_nb_cases_non_vides, liste_temps_resolve, label = "résolution brutale", s=2)
    plt.scatter(liste_nb_cases_non_vides, liste_temps_resolution, label = "résolution 'humaine'", s=2)
    plt.ylabel('temps (en s)')
    plt.axis([23,80,0,1])
    plt.legend()

    plt.subplot(2,1,2)
    plt.scatter(liste_nb_cases_non_vides, liste_temps_resolve, label = "résolution brutale", s=2)
    plt.scatter(liste_nb_cases_non_vides, liste_temps_resolution, label = "résolution 'humaine'", s=2)
    plt.xlabel('nombre de cases remplies avant la resolution')
    plt.ylabel('temps (en s)')
    plt.axis([23,80,0,0.01])

    plt.show()

graphique()



