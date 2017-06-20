'''
Created on Apr 19, 2017

@author: vinicius
'''

import numpy as np
from random import uniform, random
from datetime import datetime

def lowVarianceSampler(X, W, t):
    tamanho = t #len(X)
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
        
            
    
X = [i for i in range(5)]
w = [random() for i in range(5)]
a = sum(w)
W = [b/a for b in w]
#print sum(W)

print 'X: ', X
print 'W: ', W
inicio = datetime.now()
inicio.strftime("%H:%M:%S.%f")
X2 = lowVarianceSampler(X, W, len(X))
print 'X2: ', X2
X3 = lowVarianceSampler(X, W, len(X)-2)
print 'X3: ', X3
'''
fim = datetime.now()
fim.strftime("%H:%M:%S.%f")
print "INICIO: ", inicio
print "FIM: ", fim
print fim - inicio
'''