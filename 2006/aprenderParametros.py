'''
Created on Mar 31, 2017

@author: vinicius
'''

import numpy as np
import sys
import funcoesProbabilidade
from math import sqrt

class AprenderParametros(object):
    '''
    classdocs
    '''


    def __init__(self, rayFile, dadosFile, parametrosFile):
        '''
        Constructor
        '''
        self.rayFile = rayFile
        self.dadosFile = dadosFile
        self.parametrosFile = parametrosFile
        self.loadRayCasting()
        self.loadDados()
        self.loadParametros()
        
    def loadRayCasting(self):
        self.rayCasting = np.load(self.rayFile,'readonly')
        
    def loadDados(self):
        self.dados = np.load(self.dadosFile,'readonly')
    
    def loadParametros(self): 
        file = open(self.parametrosFile,'r')
        parametros = []
        for linha in file.readlines():
            parametros.append(linha.split(": ")[1])
        file.close()
        self.alcanceMax = int(parametros[0])
        self.desvioHit = int(parametros[1])
        self.lambdaShort = int(parametros[2])
    
    def aprenderParametrosIntrinsicos(self):
        eHit = []
        eShort = []
        eMax = []
        eRand = []
        Z = []
        ZReal = []
        Zaux = 0
        for i,d in enumerate(self.dados):
            x, y, theta, z = d
            zReal = self.rayCasting(x,y,theta)
            Z[i] = z
            ZReal[i] = zReal
            '''acredito que esteja certo'''
            Zaux += z**2
            
            phit = funcoesProbabilidade.pHit(z, zReal, self.desvioHit, self.alcanceMax)
            pshort = funcoesProbabilidade.pShort(z, zReal, self.lambdaShort)
            pmax = funcoesProbabilidade.pMax(z, self.alcanceMax)
            prand = funcoesProbabilidade.pRand(z, self.alcanceMax)
            
            n = (phit + pshort + pmax + prand)**-1
            
            eHit[i] = n*phit
            eShort[i] = n*pshort
            eMax[i] = n*pmax
            eRand[i] = n*prand
            
        aux = sqrt(Zaux)**-1    # Verificar isso
        self.zHit    =   aux * sum(eHit)
        self.zShort  =   aux * sum(eShort)
        self.zMax    =   aux * sum(eMax)
        self.zRand   =   aux * sum(eRand)
        self.novoDesvioHit = sqrt(1/(sum(eHit))*sum((np.array(eHit)*(np.array(Z) - np.array(ZReal))**2)))
        self.novoLambdaShort = sum(eShort)/(sum(np.array(eShort)*np.array(Z)))
        
        self.saveParametros()
        
    def saveParametros(self):
        file = open(self.parametrosFile,'w')
        file.write("Alcance maximo: " + str(self.alcanceMax) + "\n")
        file.write("Desvio Hit: " + str(self.novoDesvioHit) + "\n")
        file.write("Lambda Short: " + str(self.novoLambdaShort) + "\n")
        file.write("zHit: " + str(self.zHit) + "\n")
        file.write("zShort: " + str(self.zShort) + "\n")
        file.write("zMax: " + str(self.zMax) + "\n")
        file.write("zRand: " + str(self.zRand))
        file.close()
        
         
if __name__ == '__main__':
    print "Oi!"

        