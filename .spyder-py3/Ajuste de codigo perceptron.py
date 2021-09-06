# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 10:28:58 2021

@author: Bruno
"""


 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_data():
   
    dados = pd.read_csv("iris.csv", sep=",", header = None)

    dadosls = dados[:150]

    
    dadosls[4] = np.where(dados.iloc[:, -1]=='Iris-setosa', 1, 0)

    dadosls = np.asmatrix(dadosls, dtype = 'float64')

    tamanho = dadosls.shape[0]
    tamanho_indices = range(0,tamanho)
    random_indices = np.random.choice(tamanho, size=105, replace=False)
    random_linhas = dadosls[random_indices, :]
    
    
    treino = dadosls[random_indices, :]
    indice_teste = list(set(tamanho_indices)-set(random_indices))
    teste = dadosls[indice_teste,:]
    return random_linhas,treino,teste
    
    
class Perceptron(object):
    
    def __init__(self, num_entradas, epocas=5, taxa_aprendizagem=0.01):
        self.epocas = epocas
        self.taxa_aprendizagem = taxa_aprendizagem
        self.pesos = np.random.randn(num_entradas + 1)
        
    def calc_saida(self, entradas):
        net = np.dot(entradas, self.pesos[1:]) + self.pesos[0]
        if net > 0:
            saida = 1
        else: 
            saida = 0
        return saida
    
    def treinar(self, entradas_treino, alvos):
        n_epoca = 0
        for _ in range(self.epocas):
            n_epoca = n_epoca + 1
            print(n_epoca)
            erro = 0
            if n_epoca <= self.epocas: 
              for entradas, alvo in zip(entradas_treino, alvos):
                  cont = 0
                  soma_erro_epoca = 0
                  estimacao = self.calc_saida(entradas)
                  erro = alvo - estimacao
                  print('%.7f' % (erro))
                  self.pesos[1:] += np.squeeze(np.array(self.taxa_aprendizagem * erro * entradas))
                  self.pesos[0] = self.taxa_aprendizagem * erro
                  soma_erro_epoca = soma_erro_epoca + abs(erro) 
                  cont += 1
            
              erro_medio_epoca = soma_erro_epoca/cont
              print("o erro medio na epoca é: %.7f" % erro_medio_epoca)
            elif erro_medio_epoca <= 1:
                  break
            else: break
        
base = load_data()
basedados = base[0]
treino = base[1]
teste = base[2]

#composição dos dados
'''
1. sepal length in cm
2. sepal width in cm
3. petal length in cm
4. petal width in cm
5. class
--Iris setosa: 50 primeiros elementos
--Iris Versicolour: 50 elementos intermediarios
--Iris virginica: 50 elementos finais
'''

plt.scatter(np.array(basedados[:50,0]), np.array(basedados[:50,2]), marker = 'o', label = 'setosa')
plt.scatter(np.array(basedados[50:,0]), np.array(basedados[50:,2]), marker = 'o', label = 'versicolour')
plt.xlabel('Comprimento da pétala')
plt.ylabel('Comprimento da sépala')
plt.legend()
plt.show()


entradas_treino =  treino[:,:-1]

alvos = treino[:,-1]

perceptron = Perceptron(4)
perceptron.treinar(entradas_treino,alvos)

acertos=0


for ind in range(len(teste)):
    entrada_teste = np.matrix(teste[ind,:-1])  
    saida_teste = perceptron.calc_saida(entrada_teste)
    if(saida_teste == teste[ind,4]):
        acertos = acertos+1
    
print("Total: ",len(teste),"\nAcertos: ",acertos, "\nAssertividade", (acertos/len(teste)*100),"%")     
        

'''
entradas_treino = basedados[:, :-1]

alvos = basedados[:, -1]

perceptron = Perceptron(4)

perceptron.treinar(entradas_treino, alvos)

entrada_teste = np.array([5.1, 3.5, 1.4, 0.2])
saida_teste1 = perceptron.calc_saida(entrada_teste)
                
entrada_teste = np.array([7, 3.2, 4.5, 1.4])
saida_teste2 = perceptron.calc_saida(entrada_teste)
                
entrada_teste = np.array([6.3, 3.3, 6, 2.5])
saida_teste3 = perceptron.calc_saida(entrada_teste)
'''         

        