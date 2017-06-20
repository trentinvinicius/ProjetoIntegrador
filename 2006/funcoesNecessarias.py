'''
Created on Jun 9, 2017

@author: vinicius
'''

import numpy as np
from math import cos, sin

pose = np.array((0, 0, 0))

d, e = 9,9          #diferenças dos encoders das rodas em metros
sentido
d_old = d_new
d_new = getEncoder(d)
e_old = e_new
e_new = getEncdoer(e)
if sentido
    d = d_new - d_old
else
    
e = e_old - e_new

3900 old
0100 new
encoder = np.array([d,e])
matriz1 = np.array([[R/2.0, R/2.0],[0, 0],[R/(2*l), -R/(2*l)]])
matrizRotacao = np.array([[cos(pose[2]), -sin(posicoes[2]), 0],[sin(posicoes[2]), cos(posicoes[2]),0],[0,0,1]])
velocidades = matriz1.dot(encoder)
incrementos = matrizRotacao.dot(velocidades)
posicoes += incrementos*tempo