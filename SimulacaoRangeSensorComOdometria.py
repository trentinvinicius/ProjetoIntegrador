'''
Created on May 3, 2017

@author: vinicius
'''
import numpy as np
import pygame
import time
from particleFilterComRangeSensor import ParticleFilter
from math import cos, sin, pi, trunc, sqrt
from funcoesProbabilidade import sample


largura, altura = 400, 400 
pf = ParticleFilter()
pygame.init()
screen = pygame.display.set_mode((largura, altura+100))
done = False
bg = pygame.image.load("mapa.jpg")
i = 0
r = 0
RUIDO_COMANDO = 1
RUIDO_MEDIDA = 5

fonte = pygame.font.SysFont("monospace", 15, True)

X = []
estimativa = (0,0,0)
PosicaoRobo = (20,20,0)


for j in range(2000):
    X.append(pf.newRandomParticle()) 
#X = []
#X.append((20,20,0))  
#X.append(pf.newRandomParticle())

R = 5.0
l = 19.0
posicoes = np.array([20.0,20.0,0.0])
tempo = 1.0

k = 1.0
b = 0.49741883681
https://github.com/ros-planning/navigation/issues/20
https://github.com/ros-planning/navigation/issues/499
adicionar https://github.com/ros-planning/navigation/blob/groovy-devel/amcl/src/sensors/amcl_odom.cpp#L119
def move():
    global i
    global PosicaoRobo
    global posicoes
    i += 1
    #print i
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
    velocidades = matriz1.dot(encoder) #np.dot(encoder,matriz1)
    incrementos = matrizRotacao.dot(velocidades)
    posicoes += incrementos*tempo
    #print posicoes, velocidades
    
    PosicaoRobo = (round(posicoes[0],2), round(posicoes[1],2), (round((posicoes[2])*180.0/pi,2)%360))
                        
def desenhaParticulas(particles):
    for p in particles:
        x, y, theta = p
        pygame.draw.circle(screen, (0,0,255), (x,y), 1)

def desenhaRobo():
    global PosicaoRobo
    x, y, theta = PosicaoRobo
    pygame.draw.circle(screen,(0,255,0),(trunc(x),trunc(y)),7)
    x2 = x + 7*cos(-theta*pi/180)
    y2 = y + 7*sin(-theta*pi/180)    
    pygame.draw.line(screen,(255,0,0),(int(x2),int(y2)),(x,y),1)

def desenhaEstimativa(X, W):
    global estimativa
    estimativa = pf.estimativa(X, W)
    if (estimativa == -1):
        pass
    else:
        #print "DESENHOU"
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

#time.sleep(5)  
iteracoes = 0     
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        screen.fill((0,0,0))
        screen.blit(bg, (0, 0))
        Xa = PosicaoRobo 
        xa = Xa[0] #+ sample(1)
        ya = Xa[1] #+ sample(1)
        thetaa = Xa[2] #+ sample(1)
        XaRuido = (xa, ya, thetaa)
        move()
        Xb = PosicaoRobo
        xb = Xb[0]# + sample(RUIDO_COMANDO)
        yb = Xb[1] #+ sample(RUIDO_COMANDO)
        thetab = Xb[2]# + sample(RUIDO_COMANDO)
        XbRuido = (xb, yb, thetab)
        u = (XaRuido,XbRuido)
        #print XaRuido, XbRuido, u
        X = pf.motionUpdate(u, X)
        u = (Xa,Xb)
        desenhaParticulas(X)          
        
        
       
        #X = pf.motionUpdate(u, X)
        xR, yR, thetaR = PosicaoRobo
        z = []
        for ang in range(-30,40,10):
            z.append(pf.rayCasting[xR,yR,((thetaR+ang)%360)]+ sample(RUIDO_MEDIDA)) #+ sample(5)      
           
        W = pf.measurementUpdate(z,X)
        #print W
        #print "Medidas observada ", z, W
        soma = sum(W)
        W = [w/soma for w in W]
        
        """
        x, y, theta = PosicaoRobo
        pygame.draw.circle(screen,(0,255,0),(x,y),7)
        x2 = x + 7*cos(-theta*pi/180)
        y2 = y + 7*sin(-theta*pi/180)    
        pygame.draw.line(screen,(255,0,0),(int(x2),int(y2)),(x,y),1)
        
        estimativa = pf.estimativa(X, W)
        if (estimativa == -1):
            pass
        else:
            print "DESENHOU"
            pygame.draw.circle(screen,(0,0,0),(trunc(estimativa[0]),trunc(estimativa[1])),4)
            x2 = estimativa[0] + 4*cos(-estimativa[2]*pi/180)
            y2 = estimativa[1] + 4*sin(-estimativa[2]*pi/180)    
            pygame.draw.line(screen,(255,0,255),(int(x2),int(y2)),(trunc(estimativa[0]),trunc(estimativa[1])),1)
        """
        desenhaRobo()
        desenhaEstimativa(X, W)
        escreve()
        
        
        pygame.display.flip()
        
        
        
        
        
        #(pVelha[a] -PosicaoRobo[a] for a in range(3))
        #print "Posicao ROBO ", PosicaoRobo
        
        #testar lowVarianceSampler pq nao faz sentido reduzir tanto e fazer ficar com 0 w quando X = (0,0,0)
        #print "ANtes ", X, W
        #if (iteracoes == 22):
        #    pygame.image.save(screen,"/home/vinicius/Dropbox/PROJETO/DesenhosImagens/reamostragem3.png")
        nome = "/home/vinicius/Dropbox/PROJETO/DesenhosImagens/reamostragem" + str(iteracoes) + ".png"
        iteracoes += 1                             
        r +=1
        if (r==1):
            X = pf.lowVarianceSampler(X, W)
            r = 0;  
            #print "REAMOSTROU" #, iteracoes 
        #print "DEpois ", X, W    
        #
        
        #pygame.image.save(screen, nome)
        #time.sleep(0.01)