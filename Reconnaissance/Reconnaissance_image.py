import cv2
import operator
import numpy as np
from matplotlib import pyplot as plt

def affiche_image(image):
    """Affiche une image donnée jusqu'à ce qu'une touche soit entrée"""
    cv2.imshow('image', image) #Affiche l'image
    cv2.waitKey(0) #Attend qu'une touche soit appuyée (l'image est encore visible)
    cv2.destroyAllWindows() #Ferme toutes les fenêtres

def affiche_chiffres(chiffres, couleur = 255):
    """Affiche une liste de 81 chiffres sous le format d'une grille"""
    lignes =[]
    bordures = [cv2.copyMakeBorder(img.copy(),1,1,1,1, cv2.BORDER_CONSTANT, None, couleur) for img in chiffres]
    for i in range(9):
        ligne = np.concatenate(bordures[i*9 : ((i+1)*9)], axis = 1)
        lignes.append(ligne)
    affiche_image(np.concatenate(lignes))





def pre_traitement(image,dilatation = True):
    """On utilise un flou gaussien, un seuil adaptif et une dilatation
     pour expliciter au mieux les informations de l'image"""
    #On effectue un flou gaussien
    res = cv2.GaussianBlur(image.copy(),(9,9),0)

    #On utilise un seuil adaptatif pour contraster l'image, ce seuil dépends des 11 pixels les plus proches
    res = cv2.adaptiveThreshold(res, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    #On inverse les couleurs pour appliquer la dilatation
    res = cv2.bitwise_not(res,res)

    #On dilate l'image
    if dilatation:
        kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
        res = cv2.dilate(res, kernel)
    return res

def trouve_coins_polygone_max(img):
    """Trouve les 4 coins du contour le plus large de l'image, donc ici les 4 coins de la grille"""
    contours , _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Trouve les contours
    contours = sorted(contours, key = cv2.contourArea, reverse = True) #On trie les contours par aires décroissante
    polygone = contours[0] #On récupère le polygone le plus spacieux

    #Pour trouver les coordonnées des coins, on peut procéder comme suit :
    #Coin en bas à droite (x,y) on maximie x+y
    #Coin en haut à gauche (x,y) on minimise x+y
    #Coin en bas à gauche (x,y) on minimise x-y
    #Coin en haut à gauche (x,y) on maximise x+y

    bas_droit , _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygone]), key=operator.itemgetter(1))
    haut_gauche , _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygone]), key=operator.itemgetter(1))
    bas_gauche , _ = min(enumerate([pt[0][0] - pt[0][1] for pt in polygone]), key=operator.itemgetter(1))
    haut_droit , _ = max(enumerate([pt[0][0] - pt[0][1] for pt in polygone]), key=operator.itemgetter(1))

    #On a utilisé key = operator.itemgetter pour retrouver les indices correspondants

    return [polygone[haut_gauche][0], polygone[haut_droit][0], polygone[bas_droit][0], polygone[bas_gauche][0]]

def distance_entre(p1,p2):
    """Retourne la distance entre les points p1 et p2"""
    a = p2[0] - p1[0]
    b = p2[1] - p1[1]
    return np.sqrt((a**2) + (b**2))

def redimensionne(image, rect_coord):
    """Redimensionne une image rectangulaire en une image carrée de taille similaire"""
    #On décrit le rectangle par ses coins
    haut_gauche, haut_droit, bas_droit, bas_gauche = rect_coord[0], rect_coord[1], rect_coord[2], rect_coord[3]

    rect = np.array([haut_gauche, haut_droit, bas_droit, bas_gauche], dtype='float32') #on force le typage pour les fonctions qui suivents

    #On sélectionne le coté le plus long
    cote = max([distance_entre(bas_droit, haut_droit), distance_entre(haut_gauche, bas_gauche), distance_entre(bas_droit, bas_gauche), distance_entre(haut_gauche, haut_droit)])

    #On donne les coordonnées du carré
    carre = np.array([[0,0], [cote-1,0], [cote-1, cote-1], [0, cote-1]], dtype='float32')

    #On trouve le rapport de déformation de l'image
    r = cv2.getPerspectiveTransform(rect,carre)

    #On effectue la transformation
    return cv2.warpPerspective(image, r, (int(cote), int(cote)))

def creation_grille(image):
    """Crée une grille de 81 cases à partir d'une image carrée (renvoie les coordonnées)"""
    grille= []
    cote = image.shape[:1]
    cote = cote[0]/9
    #On échange les rôles de i et j pour ranger les rectangles ligne par ligne
    for j in range(9):
        for i in range(9):
            p1 = (i * cote, j * cote) #Coin haut gauche
            p2 = ((i+1) * cote, (j+1) * cote) #Coin bas droit
            grille.append((p1,p2))
    return grille

def coupe_rect(img,rect):
    """Coupe un rectangle dans l'image à partir du coin haut gauche et du coin bas droit"""
    return img[int(rect[0][1]):int(rect[1][1]), int(rect[0][0]):int(rect[1][0])]

def echelonne_centre(img, taille, marge = 0, fond = 0):
    """echelonne et centre une image sur un nouveau fond carré"""
    h,l = img.shape[:2]

    def centrage(longueur):
        if longueur % 2 == 0:
            cote1 = int((taille-longueur)/2)
            cote2 = cote1
        else:
            cote1 = int((taille-longueur)/2)
            cote2 = cote1 + 1
        return cote1, cote2

    def echelonne(r,x):
        return int(r*x)

    if h > l :
        dessus = int(marge/2)
        dessous = dessus
        ratio = taille/h
        h,l = echelonne(ratio,h), echelonne(ratio,l)
        gauche, droite = centrage(l)
    else:
        gauche = int(marge/2)
        droite = gauche
        ratio = taille/l
        h,l = echelonne(ratio,h), echelonne(ratio,l)
        dessus, dessous = centrage(h)
    
    img = cv2.resize(img, (l,h))
    img = cv2.copyMakeBorder(img, dessus, dessous, gauche, droite, cv2.BORDER_CONSTANT, None, fond)
    return cv2.resize(img, (taille, taille))

def trouve_plus_gros_bloc(inp_img, scan_haut_gauche=None, scan_bas_droit=None):
    """ Trouve la structure la plus grosse dans l'image, la colorie en blanc et colorie le reste en noir"""
    img = inp_img.copy()
    hauteur, largeur = img.shape[:2]

    aire_max = 0
    seed_point = (None,None)

    if scan_haut_gauche==None:
        scan_haut_gauche=[0,0]

    if scan_bas_droit==None:
        scan_bas_droit=[largeur, hauteur]

    #On boucle à travers l'image
    for x in range(scan_haut_gauche[0], scan_bas_droit[0]):
        for y in range(scan_haut_gauche[1], scan_bas_droit[1]):
            if img.item(y,x) == 255 and x < largeur and y < hauteur:
                aire = cv2.floodFill(img, None, (x, y), 64)
                if aire[0] > aire_max:
                    aire_max = aire[0]
                    seed_point = (x,y)
    
    #Coloriage en gris
    for x in range(largeur):
    		for y in range(hauteur):
			    if img.item(y, x) == 255 and x < largeur and y < hauteur:
				    cv2.floodFill(img, None, (x, y), 64)

    masque = np.zeros((hauteur + 2, largeur + 2), np.uint8) #Masque qui est 2 pixel plus grand

    #On trouve le plus gros bloc
    if all([p is not None for p in seed_point]):
        cv2.floodFill(img, masque, seed_point, 255)
    
    dessus, dessous, gauche, droite = hauteur, 0, largeur, 0
    
    for x in range(largeur):
        for y in range(hauteur):
            if img.item(y,x) == 64:
                cv2.floodFill(img, masque, (x, y), 0)
            
            if img.item(y,x) == 255:
                dessus = y if y < dessus else dessus
                dessous = y if y > dessous else dessous
                gauche = x if x < gauche else gauche
                droite = x if x > droite else droite

    boite = [[gauche,dessus], [droite, dessous]]
    return img,np.array(boite, dtype='float32'), seed_point

def extraction_chiffre(img,rect,taille):
    """Exrait un chiffre  (si il y en a un) d'une grille de Sudoku"""
    chiffre = coupe_rect(img,rect) #On extrait l'image de la case
    h,l = chiffre.shape[:2]
    marge = int(np.mean([h,l])/2.5)
    _, boite, seed, = trouve_plus_gros_bloc(chiffre, [marge, marge], [l-marge, h-marge])
    chiffre = coupe_rect(chiffre, boite)

    l = boite[1][0] - boite[0][0]
    h = boite[1][1] - boite[0][1]

    if l > 0 and h > 0 and (l*h) > 100 and len(chiffre) > 0:
        return echelonne_centre(chiffre, taille, 4)
    else:
        return np.zeros((taille,taille), np.uint8)

def obtention_chiffres(img,carres,taille):
    """Extrait chaque chiffre de leur case pour construire un tableau"""
    chiffres=[]
    img = pre_traitement(img.copy(),dilatation=False)
    for carre in carres:
        chiffres.append(extraction_chiffre(img,carre,taille))
    return chiffres

def contraste_max(chiffres):
    """Prend chaque élément du tableau donné par obtention_chiffres et remplace les pixels exclusivement par du noir ou du blanc"""
    for i in range(len(chiffres)):
        for j in range(len(chiffres[0])):
            for k in range(len(chiffres[0][0])):
                if chiffres[i][j][k] > 50:
                    chiffres[i][j][k] = 255
                else:
                    chiffres[i][j][k] = 0
    return chiffres

def grille_extraite(path):
    original = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    traitee = pre_traitement(original)
    coins = trouve_coins_polygone_max(traitee)
    rognee = redimensionne(original,coins)
    carres = creation_grille(rognee)
    chiffres = obtention_chiffres(rognee, carres, 28) #28 pour avoir un bonne taille pour la reconnaissance de chiffres
    chiffres = contraste_max(chiffres)
    return chiffres

def is_empty(case):
	rate = 0
	total = 0
	for i in case:
		for j in i:
			if j  > 200: #Case blanche
				rate = rate + 1
			total = total + 1
	return rate/total < 0.01

