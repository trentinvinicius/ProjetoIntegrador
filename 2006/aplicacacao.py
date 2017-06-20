'''
Created on May 24, 2017

@author: vinicius
'''
from particles import ParticleFilter
from math import pi

numParticles = 10

pf = ParticleFilter(numParticles)
print pf.X

while True:
    posicoesEncoder = ((0,0,0),(0,0,90))
    leituraSensor = (260, 30)
    u = pf.findU(posicoesEncoder)
    print u
    soma = 0
    for p in pf.X:
        #print p
        pf.move(p, u)
        #print p
        pf.sense(p, leituraSensor)
        soma += p.w
        #print p.w
    '''for i in range(numParticles):
        pf.move(pf.X[i],u)
        pf.sense(pf.X[i],leituraSensor)'''
        
    print pf.X
    #for i in range(numParticles):
    normalizador = soma**-1
    for p in pf.X:
        p.w = p.w*normalizador
        #print p.w
    
    print soma
    break
    
        
        