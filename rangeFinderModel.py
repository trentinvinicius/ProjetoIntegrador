'''
Created on Apr 1, 2017

@author: vinicius
'''

import funcoesProbabilidade
from parametros import Parametros


class RangeFinderModel(object):
    '''
    classdocs
    '''


    def __init__(self, z, zReal):
        '''
        Constructor
        O modelo de medida recebe o conjunto de valores lidos pelo sensor (z) e o conjunto de valores
        reais obtidos atraves do ray casting na posicao da particula (zReal) e os compara resultando na 
        probabilidade das medidas da particula serem as medidas reais do robo.
        '''
        self.z = z
        self.zReal = zReal
        #self.calcularProbabilidade()
        
    def calcularProbabilidade(self):
        q = 1
        for i in range(len(self.z)):
            #print d, 'A'
            #z, zReal = self.dados[i]  #x, y, theta nao precisa
            p = (Parametros.ZHIT) * funcoesProbabilidade.pHit(self.z[i], self.zReal[i]) + \
                (Parametros.ZSHORT) * funcoesProbabilidade.pShort(self.z[i], self.zReal[i]) + \
                (Parametros.ZMAX) * funcoesProbabilidade.pMax(self.z[i]) + \
                (Parametros.ZRAND) * funcoesProbabilidade.pRand(self.z[i])
            #print p
            q *= p       
        return q
            

            
if __name__ == '__main__':
    
    d = [(400,400)]
    print RangeFinderModel(d).calcularProbabilidade()
    
           
            