import numpy as np
import sys
from movements import Movements
import sensor 
from time import sleep

leituras = []
move = Movements()

while True:
    dados = raw_input("Informe as coordenadas x, y, theta ou digite 'fim' para encerrar: ")
    print dados
    if dados == 'fim':
        np.save('leituras.npy', leituras)
        print leituras
        sys.exit()
        
    try:
#        x, y, theta = dados.split(', ')
#        print x, y, theta
        x, y, theta = 0, 0, 0
        for i in range(8):
            ang = 20*i
            #print 'a'
            move.setAngle(8,ang)
            #print 'b'
            for j in range(5):
                valor = sensor.distance()
                print valor
                leituras.append((int(x), int(y), int(theta), ang, valor))
                sleep(0.05)
    except:
        print "Dados invalidos"
    

