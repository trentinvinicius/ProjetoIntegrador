'''
Created on Apr 18, 2017

@author: vinicius

Esse arquivo serve para executar movimentos de translacao e rotacao e gravar o valor real medido
gerando ao final dois arquivos (um para translacao e outro para rotacao) com os valores real e esperado 
para serem usados na obtencao dos parametros intrinsicos de movimento

'''

import numpy as np
import sys

translacao = []
rotacao = []
mov = ''

def sair():
    print "Gravando dados..."
    np.save('translacao.npy', translacao)
    np.save('rotacao.npy', rotacao)
    print "Dados gravados"
    sys.exit()
        
def funcao():
    f = raw_input("Informe o tipo de movimento (t = translacao r = rotacao) ou digite 'fim' para sair: ")
    global mov
    if f == 't': 
        mov = 1
        print "Translacao"
    elif f == 'r':
        mov = 0
        print "Rotacao"
    elif f == 'fim':
        sair()
    else:
        print "Dado incorreto, informe novamente!"
        funcao()
        
funcao()

while True:
    d = raw_input("Informe a distancia em cm ou digite 'v' para voltar: ")
    if d == 'v':
        funcao()
    else:
        try:
            valor = float(d)
            if mov == 't':
                #translacao(valor)
                pass
            else:
                #rotacao(valor)
                pass
            
            tMedida = raw_input("Informe a distancia medida em cm: ")
            try:
                valorMedido = float(tMedida)
                print mov
                if mov:
                    translacao.append((valor,valorMedido))
                else:
                    rotacao.append((valor,valorMedido))
            except ValueError:
                print "Dado incorreto!"
        except ValueError:
            print "Dado incorreto!"

