'''
Created on Apr 9, 2017

@author: vinicius
'''
from random import randint
import numpy as np
from rangeFinderModel import RangeFinderModel
from parametros import Parametros
from math import cos, sin, pi
from random import uniform
from motionModel import sampleMotionModelOdometry

class ParticleFilter(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.particles = []
        self.loadMapa()
        self.loadRayCasting()
        
    def loadMapa(self):
        self.mapa = np.load('mapaDilatado.npy','readonly')
        self.largura, self.altura = self.mapa.shape
        
    def loadRayCasting(self):
        self.rayCasting = np.load('rayCasting.npy','readonly')
        
    def newRandomParticle(self, limInfX = 0, limSupX = None, limInfY = 0, limSupY = None, limInfTheta = 0, limSupTheta = 359):
        if limSupX == None:
            limSupX = self.largura - 1
        if limSupY == None:
            limSupY = self.altura - 1
            
        x = randint(limInfX, limSupX)
        y = randint(limInfY, limSupY)
        theta = randint(limInfTheta, limSupTheta)
        while(self.mapa[x,y]==0.0):
            x = randint(limInfX, limSupX)
            y = randint(limInfY, limSupY)
            theta = randint(limInfTheta, limSupTheta)
        #self.particles.append((x, y, theta))
        return (x, y, theta)
    
    def measurementUpdate(self, z, X):
        W = []
        for particle in X:
            if (particle == (0,0,0)):
                W.append(0)
                continue
            x, y, theta = particle
            zReal = []
            for ang in range(-30,40,10):
                try:
                    xS, yS, thetaS = self.getSensorPosition(x, y, theta, ang)
                    zReal.append(self.rayCasting[xS, yS, thetaS])
                    #print "Posicao e medida  ",xS, yS, thetaS, zReal                    
                except:
                    W.append(0)
                    break
            #print "MEDIDAS: ", z, zReal
            w = RangeFinderModel(z,zReal).calcularProbabilidade()  
            #print "PROB: ", w             
            W.append(float(w))
        return W
    
    def getSensorPosition(self, x, y, theta, angPescoco):
        thetaRad = float(theta)*pi/180
        angPescocoRad = float(angPescoco)*pi/180
        R = np.array([[cos(thetaRad), sin(thetaRad), x], \
                      [-sin(thetaRad), cos(thetaRad), y],\
                       [0, 0, 1]])
        pSR = np.array([(cos(angPescocoRad)*(Parametros.XSENSOR) + sin(angPescocoRad)*(Parametros.YSENSOR)), \
                        (-sin(angPescocoRad)*(Parametros.XSENSOR) + cos(angPescocoRad)*(Parametros.YSENSOR)), \
                        1])
        pSO = R.dot(pSR)
        return pSO[0], pSO[1], ((theta + angPescoco)%360)
     #   pass
    #   angPescoco o angulo do servo motor da cabeca em relacao ao centro do robo
       
#angulo de leitura do sensor = theta + angPescoco (horario +, anti-horario - ?)
    def motionUpdate(self, u, X):
        Xn = []
        for particle in X:
            i = 0;
            while True:
                try:
                    xn = sampleMotionModelOdometry(u, particle)
                    if (self.mapa[xn[0],xn[1]] == 1):
                        Xn.append(xn)
                        continue
                except:
                    pass
                i += 1
                if (i == 10):
                    #Xn.append(self.newRandomParticle())
                    Xn.append((0,0,0)) #ver como fazer caso a particula caia fora
                    break 
       
        return Xn
        
    def lowVarianceSampler(self, X, W):
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
    
    def estimativa(self, X, W):
        tamanho = len(X)
        x_estimado, y_estimado, theta_estimado, soma = 0, 0, 0, 0
        for i in range(tamanho):
            x, y, theta = X[i]
            soma += W[i]
            x_estimado     += x * W[i]
            y_estimado     += y * W[i]
            theta_estimado += float(theta) * W[i]
            print float(theta)
            
        if (soma==0):
            return -1
        
        x_estimado     /= soma
        y_estimado     /= soma
        theta_estimado /= soma
        #print theta_estimado
        return (round(x_estimado,2), round(y_estimado,2), round((theta_estimado %360),2))
            
    

if __name__ == '__main__':
    p = ParticleFilter()
    for i in range(10):
        p.newRandomParticle()
    z = 150
    s = 0
    '''normalizar o peso'''
    pa = []
    
    pa.append(p.newRandomParticle())
    print pa
    for e in pa:
        x, y, theta = e
        print p.rayCasting[x,y,theta]
        
    print "SOma ", s
    #print  p.measurementUpdate(z, pa)
    a = (0, 0, 0)
    b = (10, 5, pi/6)
    c = (1, 1, pi)
    u = (a,b)
    #print p.motionUpdate(u, c)
def move(self, x2, y2, theta2):
    pass
            
        