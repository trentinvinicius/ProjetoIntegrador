#!-*- conding: utf8 -*-
'''
Created on Apr 21, 2017

@author: vinicius
'''
'''
o encoder comeca com 0, 0, 0
e vai integrando
cada vez que eh chamado ele retorna o ultimo valor chamado e o valor atual
atualizando o ultimo valor chamado com o valor atual
'''
from parametros import Parametros
from math import cos, sin, atan2, pi, sqrt
from funcoesProbabilidade import sample

def sampleMotionModelOdometry(u, X):
    '''
    Gera uma amostra de p(x(t)\u, x(t-1)), dado u e x
    Sendo:
    u = (Xa, Xb) = estimativa realizada atraves do incremento dos encoders das rodas
                   com:
                   Xa = estimativa anterior
                   Xb = estimativa atual
    x = hipotese no tempo t-1
    '''
    Xa, Xb = u
    xa, ya, thetaa = Xa
    xb, yb, thetab = Xb
    
    x, y, theta = X
    #print "GRAUS ", theta, thetaa, thetab
    theta = theta*pi*(180**-1)
    thetaa = thetaa*pi*(180**-1)
    thetab = thetab*pi*(180**-1)
    
    #print "RAD ", theta, thetaa, thetab
    
    dRot1 = atan2(yb - ya, xb - xa) - thetaa
    dTrans = sqrt((xa - xb)**2 + (ya - yb)**2)
    dRot2 = thetab - thetaa - dRot1
    
    dRot1N = dRot1 + sample((Parametros.ALPHA1) * abs(dRot1) + (Parametros.ALPHA2) * dTrans)
    dTransN = dTrans + sample((Parametros.ALPHA3) * dTrans + (Parametros.ALPHA4) * (abs(dRot1) + abs(dRot2)))
    dRot2N = dRot2 + sample((Parametros.ALPHA1) * abs(dRot2) + (Parametros.ALPHA2) * dTrans)
    
    xn = x + dTransN * cos(theta + dRot1N)
    yn = y + dTransN * sin(theta + dRot1N)
    thetan = (theta + dRot1N + dRot2N) % (2*pi)
    
    Xn = (int(round(xn)), int(round(yn)), int(round(thetan*180*(pi**-1))))
    
    return Xn


'''
a = (0, 0, 0)
b = (10, 5, 5*pi/3)
c = (1, 1, 0)
u = (a,b)
for i in range(10):
    print sampleMotionModelOdometry(u, c)
'''