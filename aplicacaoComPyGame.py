'''
Created on Jun 5, 2017

@author: vinicius


'''

from particles import ParticleFilter
from math import pi, cos, sin, sqrt, trunc
import numpy as np
from funcoesProbabilidade import sample
import pygame
import time


R = 5.0
l = 19.0
largura, altura = 400, 400 
tempo = 1.0
i = 0
r = 0

posicoes = np.array([20.0,20.0,0.0])
estimativa = (0,0,0)
PosicaoRobo = (20,20,0)

RUIDO_MEDIDA = 5

numParticles = 5
pf = ParticleFilter(numParticles)


'''        Inicializacao Pygame            '''
pygame.init()
screen = pygame.display.set_mode((largura, altura+100))
done = False
bg = pygame.image.load("mapa.jpg")
fonte = pygame.font.SysFont("monospace", 15, True)
'''                 fim                   '''

k = 1.0
b = 0.49741883681

def moveRobo():
    global i
    global PosicaoRobo
    global posicoes
    i += 1
    if i < 70:
        e = k
        d = k
        
    elif i < 82:
        d = -b*k
        e = b*k
    
    elif i< 135:
        d = -k
        e = -k
    
    elif i < 147: 
        d = -b*k
        e = b*k
    
    elif i < 217:
        d = k
        e = k
    
    elif i< 229:
        d = -b*k
        e = b*k
        
    elif i < 282:
        d = -k
        e = -k
    
    elif i < 294:
        d = -b*k
        e = b*k
    
    else:
        i=0
        e = k
        d = k
        
    encoder = np.array([d,e])
    matriz1 = np.array([[R/2.0, R/2.0],[0, 0],[R/(2*l), -R/(2*l)]])
    matrizRotacao = np.array([[cos(posicoes[2]), -sin(posicoes[2]), 0],[sin(posicoes[2]), cos(posicoes[2]),0],[0,0,1]])
    velocidades = matriz1.dot(encoder)
    incrementos = matrizRotacao.dot(velocidades)
    posicoes += incrementos*tempo
    
    PosicaoRobo = (round(posicoes[0],2), round(posicoes[1],2), (round((posicoes[2])*180.0/pi,2)%360))
    
def desenhaParticulas():
    for p in pf.X:        
        pygame.draw.circle(screen, (0,0,255), (int(round(p.x)),int(round(p.y))), 1)
        
def desenhaRobo():
    global PosicaoRobo
    x, y, theta = PosicaoRobo
    pygame.draw.circle(screen,(0,255,0),(trunc(x),trunc(y)),7)
    x2 = x + 7*cos(-theta*pi/180)
    y2 = y + 7*sin(-theta*pi/180)    
    pygame.draw.line(screen,(255,0,0),(int(x2),int(y2)),(x,y),1)
    
def desenhaEstimativa():
    global estimativa
    estimativa = pf.estimativa()
    if (estimativa == -1):
        pass
    else:
        pygame.draw.circle(screen,(75,0,130),(trunc(estimativa[0]),trunc(estimativa[1])),5)
        x2 = estimativa[0] + 5*cos(-estimativa[2]*pi/180)
        y2 = estimativa[1] + 5*sin(-estimativa[2]*pi/180)    
        pygame.draw.line(screen,(139,0,139),(int(x2),int(y2)),(trunc(estimativa[0]),trunc(estimativa[1])),1)

def escreve():
    """Escreve Posicoes"""    
    try:
        distancia = sqrt((estimativa[0]-PosicaoRobo[0])**2 + (estimativa[1]-PosicaoRobo[1])**2)
        texto1 = "Real: " + str(PosicaoRobo)
        texto2 = "Estimada: " + str(estimativa)
        texto3 = "Distancia: " + str(distancia)
        label1 = fonte.render(texto1, 1, (255,255,255))
        label2 = fonte.render(texto2, 1, (255,255,255))
        label3 = fonte.render(texto3, 1, (255,255,255))
        screen.blit(label1, (10, 430))
        screen.blit(label2, (10, 450))
        screen.blit(label3, (10, 470))
    except:
        print "ERROR"
        
iteracoes = 0
import copy
while not done:
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
    screen.fill((0,0,0))
    screen.blit(bg, (0, 0))
    Xa = PosicaoRobo
    moveRobo()
    Xb = PosicaoRobo
    leiturasEncoder = (Xa, Xb)   
    u = pf.findU(leiturasEncoder) 
    xR, yR, thetaR = PosicaoRobo
    z = []
    for ang in range(-30,40,10):
        z.append((pf.rayCasting[xR,yR,((thetaR+ang)%360)]+ sample(RUIDO_MEDIDA),ang))
    
    soma = 0
    print "Here we go again"
    print pf.X
    copia = copy.deepcopy(pf.X)
    print "COPIA ", copia
    for teste in range(len(copia)):
        print copia[teste]
        pf.move(copia[teste],u)
        for medida in z:
            pf.sense(copia[teste], medida)
        
        soma += pf.X[teste].w
    normalizador = soma**-1
    #print soma, normalizador
    soma2 = 0
    for p in pf.X:
        antes = p.w
        p.w = p.w/soma
        depois = p.w
        #print "AD ", antes, depois
        soma2 += p.w
    
    #print soma2, pf.X
    
    if soma2 > 1.1:
        break
    desenhaParticulas()
    desenhaRobo()
    desenhaEstimativa()
    escreve()
    pygame.display.flip()
    print "ANTES ", pf.X
    pf.resample()
    print "DEPOIS ", pf.X
    w = []
    for j in pf.X:
        w.append(j.w)
    #print "Pesos apos", w
    #break
    time.sleep(1)
 
    
    