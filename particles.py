'''
Created on May 21, 2017

@author: vinicius
'''
from parametros import Parametros
from random import randint, uniform, random
import numpy as np
from math import pi, atan2, cos, sin, sqrt, trunc
import funcoesProbabilidade
import copy


class Particle(object):
    '''
    classdocs
    
    '''


    def __init__(self, N):
        '''
        Constructor
        '''
        self.dimensaoX, self.dimensaoY = Parametros.DIMENSOES
        self.x = randint(0, self.dimensaoX-1)
        self.y = randint(0, self.dimensaoY-1)
        self.theta = randint(0, 360)
        self.w = 1.0/N
        
    def setParticle(self, x, y, theta, w):
        self.x = x
        self.y = y
        self.theta = theta
        self.w = w
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s peso=%s]' % (str(self.x), str(self.y), 
                                                str(self.theta), str(self.w))
    
class ParticleFilter(object):
    
    def __init__(self, N):
        self.N = N
        self.loadMapa()
        self.loadRayCasting()
        self.X = []
        
        for i in range(self.N):
            p = Particle(self.N)
            while(self.mapa[p.x,p.y] == 0.0):
                p = Particle(self.N)
            self.X.append(p)
        
    
    def loadMapa(self):
        self.mapa = np.load('mapaDilatado.npy','readonly')
        self.largura, self.altura = self.mapa.shape
        
    def loadRayCasting(self):
        self.rayCasting = np.load('rayCasting.npy','readonly')
    
    def findU(self, posicoesEncoder):
        Xa, Xb = posicoesEncoder
        xa, ya, thetaa = Xa
        xb, yb, thetab = Xb
        thetaa = thetaa*pi*(180**-1)
        thetab = thetab*pi*(180**-1)
        dRot1 = atan2(yb - ya, xb - xa) - thetaa
        dTrans = sqrt((xa - xb)**2 + (ya - yb)**2)
        dRot2 = thetab - thetaa - dRot1
        return (dRot1, dTrans, dRot2)
    
    def move(self, p, u):
        i = 0;
        while True:
            i += 1                
            try:
                pn = self.sampleMotionModel(p, u)
                if (self.mapa[trunc(pn.x), trunc(pn.y)] == 1.0):
                        p = pn                        
                        break
            except:
                pass                                
            if (i == 10):
                p.x = 0.0
                p.y = 0.0
                p.theta = 0.0
                break        
    
    def sampleMotionModel(self, p, u):
        dRot1, dTrans, dRot2 = u
        dRot1N = dRot1 + funcoesProbabilidade.sample((Parametros.ALPHA1) * abs(dRot1) + (Parametros.ALPHA2) * dTrans)
        dTransN = dTrans + funcoesProbabilidade.sample((Parametros.ALPHA3) * dTrans + (Parametros.ALPHA4) * (abs(dRot1) + abs(dRot2)))
        dRot2N = dRot2 + funcoesProbabilidade.sample((Parametros.ALPHA1) * abs(dRot2) + (Parametros.ALPHA2) * dTrans)
    
        p.x += dTransN * cos(p.theta + dRot1N)
        p.y += dTransN * sin(p.theta + dRot1N)
        #print p.theta, dRot1N, dRot2N
        p.theta = (p.theta*pi*180**-1 + dRot1N + dRot2N) % (2*pi)
        p.theta = int(p.theta*180*pi**-1)
    
        return p
    
    def sense(self, p, leituraSensor):
        Z, angPescoco = leituraSensor
        if (p.x == 0.0):
            p.w = 0.0
        else:
            try:
                xS, yS, thetaS = self.getSensorPosition(p, angPescoco)
                zReal = self.rayCasting[trunc(xS), trunc(yS), trunc(thetaS)]               
                p.w *= self.calcularProbabilidade(Z, zReal)
            except:
                p.w = 0.0
        #return p
                
    def getSensorPosition(self, p, angPescoco):
        thetaRad = float(p.theta)*pi/180
        angPescocoRad = float(angPescoco)*pi/180
        R = np.array([[cos(thetaRad), sin(thetaRad), p.x], \
                      [-sin(thetaRad), cos(thetaRad), p.y],\
                       [0, 0, 1]])
        pSR = np.array([(cos(angPescocoRad)*(Parametros.XSENSOR) + sin(angPescocoRad)*(Parametros.YSENSOR)), \
                        (-sin(angPescocoRad)*(Parametros.XSENSOR) + cos(angPescocoRad)*(Parametros.YSENSOR)), \
                        1])
        pSO = R.dot(pSR)
        return pSO[0], pSO[1], ((p.theta + angPescoco)%360)
    
    def calcularProbabilidade(self, Z, zReal):
        prob = (Parametros.ZHIT) * funcoesProbabilidade.pHit(Z, zReal) + \
            (Parametros.ZSHORT) * funcoesProbabilidade.pShort(Z, zReal) + \
            (Parametros.ZMAX) * funcoesProbabilidade.pMax(Z) + \
            (Parametros.ZRAND) * funcoesProbabilidade.pRand(Z)      
        return prob 
    
    def resample(self):
        tamanho = self.N        
        Xn = []
        r = uniform(0,tamanho**(-1))
        c = self.X[0].w
        i = 0
        for m in range (tamanho):       
            u = r + (m)*(tamanho**(-1))
            while u > c:
                i += 1
                c += self.X[i].w
            self.X[i].w = 1.0/self.N
            #print self.X[i]
            Xn.append(self.X[i])
        '''return Xn
        for i in range(2):
            pn = Particle(self.N)
            pn.setParticle(1,2,3)
            Xn.append(pn)'''
        #print self.X
        #print Xn
        self.X = copy.deepcopy(Xn)
        #print self.X
        
    def estimativa(self):
        tamanho = self.N
        x_estimado, y_estimado, theta_estimado, soma = 0, 0, 0, 0
        for p in self.X:
            soma += p.w
            x_estimado     += p.x * p.w
            y_estimado     += p.y * p.w
            theta_estimado += float(p.theta) * p.w
            #print float(p.theta)
            
        if (soma==0):
            return -1
        
        x_estimado     /= soma
        y_estimado     /= soma
        theta_estimado /= soma
        #print theta_estimado
        return (round(x_estimado,2), round(y_estimado,2), round((theta_estimado %360),2))
              
    

    