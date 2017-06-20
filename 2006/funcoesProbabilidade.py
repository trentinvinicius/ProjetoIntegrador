'''
Created on Mar 31, 2017

@author: vinicius
'''

from math import exp
import mpmath as mp
from random import uniform
from parametros import Parametros

def pHit(z, zReal, desvioHit = (Parametros.DESVIO_HIT), alcanceMax = (Parametros.ALCANCE_MAXIMO)):
    if (0 <= z <= alcanceMax):
        #n =  (mp.ncdf(alcanceMax,zReal,desvioHit) - mp.ncdf(0,zReal,desvioHit))**-1  #ta errado
        
        '''
        Usar uma area e calcular ncdf ao invez de npdf
        a probabilidade de um ponto eh zero, mas a valor da funcao nao eh
        '''
        #print "N ", n
        
        aux = 0
        #for i in range(alcanceMax*10):
        #    aux += mp.npdf(float(i)/10,zReal,desvioHit)
        #print "AREA ", aux
        #n = aux**-1  
        n = 0.1     
        #print "Com: ", (mp.ncdf(z+0.01,zReal,desvioHit - mp.ncdf(z-0.01,zReal,desvioHit))), "Sem: ", n*mp.npdf(z,zReal,desvioHit)
        return n*mp.npdf(z,zReal,desvioHit)
        #return (mp.ncdf(z+0.01,zReal,desvioHit - mp.ncdf(z-0.01,zReal,desvioHit)))
    else:
        return 0
        
def pShort(z, zReal, lambdaShort = (Parametros.LAMBDA_SHORT)):
    if (0 <= z <= zReal):
        n = 1/(1-exp(-lambdaShort*zReal))
        return n*lambdaShort*exp(-lambdaShort*zReal)
    else:
        return 0

def pMax(z, alcanceMax = (Parametros.ALCANCE_MAXIMO)):
    if (z == alcanceMax):
        return 1
    else:
        return 0

def pRand(z, alcanceMax = (Parametros.ALCANCE_MAXIMO)):
    if (0 <= z <= alcanceMax):
        return alcanceMax**-1
    else:
        return 0
    
def sample(var):
    '''
    Retorna uma amostra de uma distribuicao normal com media 0 e variancia var
    '''
    s = 0
    for i in range(12):
        s += uniform(-var,var)
    return 0.5*s


