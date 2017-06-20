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
        while(self.mapa[x,y]):
            x = randint(limInfX, limSupX)
            y = randint(limInfY, limSupY)
            theta = randint(limInfTheta, limSupTheta)
        #self.particles.append((x, y, theta))
        return (x, y, theta)
    
    def measurementUpdate(self, z, x, y, theta):
        try:
            xS, yS, thetaS = self.getSensorPosition(x, y, theta, 0)
            zReal = self.rayCasting[xS, yS, thetaS]
            return RangeFinderModel([(z,zReal)]).calcularProbabilidade()
        except:
            return 0
    
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
        return pSO[0], pSO[1], theta + angPescoco
     #   pass
    #   angPescoco o angulo do servo motor da cabeca em relacao ao centro do robo
       
#angulo de leitura do sensor = theta + angPescoco (horario +, anti-horario - ?)
    def motionUpdate(self, u, X):
        i = 0;
        while True:
            Xn = sampleMotionModelOdometry(u, X)
            if (self.mapa[Xn[0],Xn[1]] == 0):
                return Xn
            i += 1
            if (i == 10):
                return 0 #ver como fazer caso a particula caia fora 
    
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
    

if __name__ == '__main__':
    p = ParticleFilter()
    for i in range(10):
        p.newRandomParticle()
    z = 150
    s = 0
    '''normalizar o peso'''
    for x, y, theta in p.particles:
        print p.rayCasting[x,y,theta], p.measurementUpdate(z, x, y, theta)
        s = s + p.measurementUpdate(z, x, y, theta)
    print "SOma ", s
    
    a = (0, 0, 0)
    b = (10, 5, pi/6)
    c = (1, 1, pi)
    u = (a,b)
    print p.motionUpdate(u, c)
def move(self, x2, y2, theta2):
    pass
            
        