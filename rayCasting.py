'''
Created on Mar 30, 2017

@author: vinicius
'''

import numpy as np
from time import gmtime, strftime
from parametros import Parametros

"""Load Map"""
mapa = np.load('mapa.npy','readonly')
largura, altura = mapa.shape
"""        """
rayCasting = np.zeros((largura,altura,360))
maxRange = (Parametros.ALCANCE_MAXIMO).value

def distancia(origem, angulo, mapa):
    dx = np.cos(angulo)
    dy = np.sin(angulo)
    x0, y0 = origem
    for d in np.arange(0, maxRange):
        x = int(x0 + dx*d)
        y = int(y0 + dy*d)
        if 0 <= x < largura and \
           0 <= y < altura:
               if mapa[x,y] == 1.0:
                   return d
    return -1

inicio = strftime("%Y-%m-%d %H:%M:%S", gmtime())
 
for i in range(largura):
            for j in range(altura):
                if (mapa[i,j]==0):
                    for ang in range(360):
                        dist = distancia((i,j), float(ang)*np.pi/180, mapa)
                        rayCasting[i,j,ang] = float(dist)
                        print i, j, ang

np.save("rayCasting",rayCasting)

fim = strftime("%Y-%m-%d %H:%M:%S", gmtime())

print "DONE"
print "Inicio: ", inicio
print "Final: ", fim