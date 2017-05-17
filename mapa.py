'''
Created on Mar 30, 2017

@author: vinicius
'''
import pygame
import numpy as np
import cv2
import matplotlib.pyplot as plt

largura, altura = 400, 400                  # largura e altura do mapa considerando 1 pixel = 1 cm


""" Cria mapa """
mapa = np.ones((largura, altura), np.float32)
mapa[0:2,0:altura] = np.zeros((2,altura))
mapa[0:largura,0:2] = np.zeros((largura,2))
mapa[largura-2:largura,0:altura] = np.zeros((2,altura))
mapa[0:largura,altura-2:altura] = np.zeros((largura,2))
mapa[70:170,70:170] = np.zeros((100,100))
for i in range(100):
    for j in range(largura-100+i,largura):
        mapa[j,altura-1-i]=0.0
np.save("mapa.npy", mapa)        
""" """


""" Dilitar mapa """
mapaImg = cv2.cvtColor(mapa,cv2.COLOR_GRAY2BGR)
kernel = np.ones((10,10),np.uint8)
mapaDilatado = cv2.erode(mapaImg,kernel,iterations = 2) #cada iteracao adiciona uma margem de 5 cm nas paredes, margem de 4 cm no quadrado, margem de 8 cm no triangulo
mapaDilatadoSalvar = mapaDilatado[:,:,1]
np.save("mapaDilatado.npy",mapaDilatadoSalvar)
""" """


""" Plotar mapa e mapa dilatado """
fig = plt.figure()
b = fig.add_subplot(1,2,1)
plt.imshow(mapaImg)
#plt.imsave("mapa.jpg",mapaImg)
b.set_title("Mapa")
b = fig.add_subplot(1,2,2)
plt.imshow(mapaDilatado)
#plt.imsave("mapaDilatado.png",mapaDilatado)
b.set_title("Mapa Dilatado")
plt.show()
""" """



'''Desenhar mapa na tela
pygame.init()
screen = pygame.display.set_mode((400, 400))
done = False

def desenha_mapa(mapa, surf):
    for i in range(largura):
        for j in range(altura):
            if mapa[i,j] == 1.0:
                pygame.draw.line(surf, (0,0,255), (i,j), (i,j))
                
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        desenha_mapa(mapa, screen)
        pygame.display.flip()

'''        
        