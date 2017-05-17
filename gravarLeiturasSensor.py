'''
Created on Apr 17, 2017

@author: vinicius


Esse arquivo serve para realizar leituras em determinadas posicoes
e gerar um arquivo com a posicao e a leitura para serem usados na obtencao
dos parametros intrinsicos de leitura
'''

import numpy as np
import sys
sys.path.insert(0, '/home/vinicius/Dropbox/PROJETO')
#from movements import Movements

leituras = []

while True:
    dados = raw_input("Informe as coordenadas x, y, theta ou digite 'fim' para encerrar: ")
    
    if dados == 'fim':
        np.save('leituras.npy', leituras)
        print leituras
        sys.exit()
        
    try:
        x, y, theta = dados.split(', ')
        for i in range(5):
            #setAngle(i)
            for j in range(5):
                #valor = readSensor()
                leituras.append((int(x), int(y), int(theta), i, j))
    except:
        print "Dados invalidos"
    
        
