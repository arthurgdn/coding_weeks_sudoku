import tensorflow as tf
import cv2
from Reconnaissance.Reconnaissance_image import *
import operator

def maximum(array):
    """
    renvoie l'index du maximum d'une liste 
    """
    return max(enumerate([i for i in array]), key=operator.itemgetter(1))[0]



def photo_to_grid(path,model):
    """
    transforme une photo en grille sous forme de matrice
    """
    
    digit = grille_extraite(path)
    
    
    if model == 'ordi': 
        model = tf.keras.models.load_model('Reconnaissance/model2.h5') #chargement du modèle "chiffre écrit à l'ordinateur"
        digit_reshape  = np.float64(np.array([x.reshape(1,28,28) for x in digit]))  
    else:
        model = tf.keras.models.load_model('Reconnaissance/model_mnist.h5') #chargement du modèle "chiffre écrit à la main"
        digit_reshape  = np.float64(np.array([x.reshape(1,28,28,1) for x in digit]))
    
    grid = np.full((9,9), "")


    for i in range(len(digit)):
        if is_empty(digit[i]):
            grid[i//9][i%9] = ""
        else:
            chiffre = (model.predict(digit_reshape[i]))
            chiffre = maximum(chiffre[0])
            if chiffre == 0:
                chiffre =1
            grid[i//9][i%9] =  str(chiffre)
    return grid
