'''
Created on Apr 19, 2017

@author: vinicius
'''

import numpy as np
from random import uniform, random
from datetime import datetime

def lowVarianceSampler(X, W):
    tamanho = len(X)
    Xn = []
    r = uniform(0,tamanho**(-1))
    c = W[0]
    i = 0
    for m in range (tamanho):       
        u = r + (m)*(tamanho**(-1))
        while u > c:
            i += 1
            c += W[i]
        Xn.append(X[i])
    return Xn
        
            
    
X = [i for i in range(10000)]
w = [random() for i in range(10000)]
a = sum(w)
W = [b/a for b in w]
print sum(W)

print 'X: ', X
print 'W: ', W
inicio = datetime.now()
inicio.strftime("%H:%M:%S.%f")
lowVarianceSampler(X, W)
fim = datetime.now()
fim.strftime("%H:%M:%S.%f")
print "INICIO: ", inicio
print "FIM: ", fim
print fim - inicio
