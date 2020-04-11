import cv2
import operator
import numpy as np
from matplotlib import pyplot as plt


def path_to_img(path):
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

def convert_when_colour(colour, img):
    """Dynamically converts an image to colour if the input colour is a tuple and the image is grayscale."""
    if len(colour) == 3:
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif img.shape[2] == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img

def traitement_image(img):
    res = cv2.GaussianBlur(img.copy(), (9, 9), 0)
    res = cv2.adaptiveThreshold(res, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    res = cv2.bitwise_not(res, res)
    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
    res = cv2.dilate(res, kernel)
    return res

def trouve_coins_points(img):
    contours, h = cv2.findContours(img.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours[0]

def point_segment(P1,P2,P):
    return (P2[0]-P1[0])*(P[1]-P1[1])-(P2[1]-P1[1])*(P[0]-P1[0])>0

def enveloppe_convexe(tab):
    def array_to_list(tab):
        res = []
        for i in tab:
            res.append([i[0][0],i[0][1]])
        return res
    def cle(P):
        return P[0]
    points = array_to_list(tab)
    points.sort(key=cle)
    N=len(points)
    enveloppe = [points[0],points[1]]
    for i in range(2,N):
        enveloppe.append(points[i])
        valide = False
        while not(valide) and len(enveloppe)>2:
            P3 = enveloppe.pop()
            P2 = enveloppe.pop()
            P1 = enveloppe.pop()
            if point_segment(P1,P2,P3):
                enveloppe.append(P1)
                enveloppe.append(P3)
            else:
                enveloppe.append(P1)
                enveloppe.append(P2)
                enveloppe.append(P3)
                valide = True
    enveloppe.append(points[N-2])
    for i in range(N-3,-1,-1):
        enveloppe.append(points[i])
        valide = False
        while not(valide) and len(enveloppe)>2:
            P3 = enveloppe.pop()
            P2 = enveloppe.pop()
            P1 = enveloppe.pop()
            if point_segment(P1,P2,P3):
                enveloppe.append(P1)
                enveloppe.append(P3)
            else:
                enveloppe.append(P1)
                enveloppe.append(P2)
                enveloppe.append(P3)
                valide = True
    return enveloppe


def show_image(img):
    """Shows an image until any key is pressed"""
    cv2.imshow('image', img)  # Display the image
    cv2.waitKey(0)  # Wait for any key to be pressed (with the image window active)
    cv2.destroyAllWindows()  # Close all windows

img = path_to_img('exemple_hidato\exemple1.jpg')
img = traitement_image(img)

#show_image(traitement_image(img))

print(enveloppe_convexe(trouve_coins_points(img)))

points = trouve_coins_points(img)
env=enveloppe_convexe(points)
plt.figure()
plt.axis([0,1000,0,1000])
for i in range(1,len(env)):
    P2 = env[i]
    P1 = env[i-1]
    plt.plot([P1[0],P2[0]],[P1[1],P2[1]],"k-")
plt.show()