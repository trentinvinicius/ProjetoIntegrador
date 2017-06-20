'''
Created on Apr 9, 2017

@author: vinicius
'''

"""" posicao sensor em relacao origem
 [[x0], [y0], [1]] = [[cos(theta) sin(theta) x],[-sin(theta) cos(theta) y],[0 0 1]]*[[cos(angPescoco)*Xsensor + sin(angPescoco)*Ysensor],[-sin(angPescoco)*Xsensor + cos(angPescoco)*Ysensor],[1]]
 sendo (x,y,theta) a posicao do robo em relação a origem
       (Xsensor, Ysensor) a posicao do sensor em relacao ao centro do robo
       angPescoco o angulo do servo motor da cabeca em relacao ao centro do robo
       
angulo de leitura do sensor = theta + angPescoco (horario +, anti-horario - ?)

esse é a posição da leitura em relação a origem,
como comparar posição com do robo?
pq a particula x, y, theta representa a posição do robo e não a posição do sensor
aplicar movimento do pescoço e deslocamento do sensor tbm as particulas 
e pegar valor real baseado nessa posição
 """