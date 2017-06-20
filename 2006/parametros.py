'''
Created on Apr 1, 2017

@author: vinicius
'''
from enum import Enum

class Parametros(object):
    '''
    Parametros intrinsicos dos modelos de medida e de movimento
    '''
    
    ALCANCE_MAXIMO = 645        # maximo alcance do sensor sonar
    ALCANCE_MINIMO = 20         # distancia minima informada pelo sonar
    DESVIO_HIT = 10
    LAMBDA_SHORT = 0.01
    ZHIT = 0.88
    ZSHORT = 0.01
    ZMAX = 0.01
    ZRAND = 0.1
    
    XSENSOR = 0                 # coordenada x da posicao do sensor em relacao ao centro do robo
    YSENSOR = 0                 # coordenada y da posicao do sensor em relacao ao centro do robo
    
    ALPHA1 = 0.05             # erro de rotacao devido ao movimento de rotacao
    ALPHA2 = 0.05             # erro de rotacao devido ao movimento de translacao
    ALPHA3 = 0.01            # erro de translacao devido ao movimento de translacao
    ALPHA4 = 0.01               # erro de translacao devido ao movimento de rotacao
    
    DIMENSOES = (400, 400)      # dimensoes do mapa
    
    


