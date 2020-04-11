import tensorflow as tf
import cv2
from grid_extractor import *
import pickle


def convert(ligne):
    """
    converti une liste d'images du format "flatten" en format matrice classique
    """
    ligne = np.array(ligne)
    grid = np.zeros((28,28))
    for i in range(28):
        for j in range(28):
            grid[i][j] = ligne[i*28+j]
    return grid


"""
Importation du dataset pour l'entrainement du réseau de neuronnes
"""
pickle_in = open("digit-basic","rb")
dataset = pickle.load(pickle_in)


def index_max(ligne):
    """
    renvoi l'indice du plus grand élément de la liste
    """
    i = 0
    for k in range(len(ligne)):
        if ligne[k] > ligne[i]:
            i = k
    return i

(x_train, y_train), (x_test, y_test) = (dataset.train.images,dataset.train.labels) ,(dataset.test.images,dataset.train.labels)
x_train, x_test = x_train, x_test

x_train = np.array([ convert(x) for x in x_train])
y_train = np.array([index_max(x) for x in y_train])
x_test = np.array([ convert(x) for x in x_test])
y_test = np.array([index_max(x) for x in y_test])

"""
Initialisation de notre réseau de neuronnes
"""

model = tf.keras.models.Sequential([
tf.keras.layers.Flatten(input_shape=(28, 28)),
tf.keras.layers.Dense(128, activation='relu'),
tf.keras.layers.Dropout(0.2),
tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])

def train():
    """
    entrainement du réseau de neuronnes
    """
    model.fit(x_train, y_train, epochs=5)


train()


model.save('model2.h5')


