'''
Created on May 3, 2017

@author: vinicius
'''
import numpy as np
import pygame
import time
from particleFilter import ParticleFilter
from math import cos, sin, pi
from funcoesProbabilidade import sample


largura, altura = 400, 400 
pf = ParticleFilter()
pygame.init()
screen = pygame.display.set_mode((largura, altura))
done = False
bg = pygame.image.load("mapa.jpg")
i = 0
X = []
PosicaoRobo = (20,20,0)
for j in range(99):
    X.append(pf.newRandomParticle()) 
X = []
X.append((20,20,0))  
#X.append(pf.newRandomParticle()) 
def move():
    global i
    global u
    global PosicaoRobo
    i += 1
    if (i>=60):
        i = 0
    Xa = (0,0,0)
    if (i<15):
        PosicaoRobo = ((1+i)*20,20,0)
        if(i==0):
            Xb = (0,0,270)
        else:
            Xb = (20,0,0)        
    elif(i<30):
        PosicaoRobo = (300 ,(i-14)*20,270)
        if (i==15):
            Xb = (0,0,270)
        else:
            Xb = (0,20,0)
    elif(i<45):
        PosicaoRobo = (300 -(i-30)*20,300, 180)
        if(i==30):
            Xb = (0,0,270)
        else:
            Xb = (-20,0,0)
    elif(i<60):
        PosicaoRobo = (20,300 - (i-45)*20, 90)
        if(i==45):
            Xb = (0,0,270)
        else:
            Xb = (0,-20,0)
    x, y, theta = PosicaoRobo
    pygame.draw.circle(screen,(0,255,0),(x,y),7)
    x2 = x + 7*cos(-theta*pi/180)
    y2 = y + 7*sin(-theta*pi/180)    
    pygame.draw.line(screen,(255,0,0),(int(x2),int(y2)),(x,y),1)
    #u = (Xa,Xb)

def drawParticles(particles):
    for p in particles:
        x, y, theta = p
        pygame.draw.circle(screen, (0,0,255), (x,y), 1)
        
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        screen.blit(bg, (0, 0))
        
        Xa = PosicaoRobo              
        move()
        Xb = PosicaoRobo
        u = (Xa,Xb)
        print "U E X, ", u, X
        X = pf.motionUpdate(u, X)
        print "X ", X
        
        drawParticles(X)  
        pygame.display.flip()
       
        #X = pf.motionUpdate(u, X)
        xR, yR, thetaR = PosicaoRobo
        z = pf.rayCasting[xR,yR,thetaR] #+ sample(5)     
        W = pf.measurementUpdate(z,X)
        #print "Medidas observada ", z, W
        soma = sum(W)
        W = [w/soma for w in W]
        #(pVelha[a] -PosicaoRobo[a] for a in range(3))
        print "Posicao ROBO ", PosicaoRobo
        
        #testar lowVarianceSampler pq nao faz sentido reduzir tanto e fazer ficar com 0 w quando X = (0,0,0)
        #print "ANtes ", X, W
        X = pf.lowVarianceSampler(X, W)    
        #print "DEpois ", X, W    
        
    
        time.sleep(1)