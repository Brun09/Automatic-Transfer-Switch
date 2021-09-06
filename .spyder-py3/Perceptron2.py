# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 09:29:04 2021

@author: Bruno
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    dados = pd.read_csv("iris.csv", sep=",", header = None)
    print(dados)

    #Selelciona apenas os 100 primeiros pontos, os quais correspondem as classes
    #Setosa e Versicolor (Classes linearmente separaveis)
    dadosls = dados[:100]
    #Subsititui na última coluna o label iris-setosa por 0 e iris-versicolor por 1
    #visando a classificação binaria
    dadosls[4] = np.where(dadosls.iloc[:, 1]=='Iris=setosa',0, 1)
    dadosls = np.asmatrix(dadosls, dtype = 'float64')
    return dadosls

class Perceptron(object):
    
    def __init__(self, num_entradas, epocas = 20, taxa_aprendizagem=0.01):
        self.epocas = epocas
        self.taxa_aprendizagem = taxa_aprendizagem
        self.pesos = np.zeros(num_entradas + 1) #mais 01 do bias
        
    
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
            erro = 0
            for entradas, alvo in zip(entradas_treino, alvos):
                estimação = self.calc_saida(entradas)
                erro = alvo - estimação
                print("erro:", erro, ", na epoca:", n_epoca)
                self.pesos[1:] += np.squeeze(np.asarray(self.taxa_aprendizagem * erro * entradas))
                self.pesos[0] += self.taxa_aprendizagem * erro
                


basedados = load_data()

#composição dos dados
'''
1. sepal length in cm
2. sepal width in cm
3. petal length in cm
4. petal width in cm
5. class: 
-- Iris Setosa: 50 primeiros elementos
-- Iris versicolour: 50 primeiros intermediarios
-- Iris Virginca: 50 elementos finais
'''

plt.scatter(np.array(basedados[:50,0]), np.array(basedados[:50,2]), marker='o', label='setosa')
plt.scatter(np.array(basedados[:50,0]), np.array(basedados[:50,2]), marker='x', label='versicolor')
plt.xlabel('comprimento da petala')
plt.ylabel('comprimento da sepala')
plt.legend()
plt.show()

#utilização

#entradas para treinamento
entradas_treino = []
entradas_treino.append(np.array([1, 1]))
entradas_treino.append(np.array([1, 0]))
entradas_treino.append(np.array([0, 1]))
entradas_treino.append(np.array([0, 0]))

#Saida OR
alvos = np.array([1, 1, 1, 0])

perceptron = Perceptron(2, 20, 0.1)#informamos apenas o numero de entradas (duas),
#demasi entradas ficam com valores padrão
perceptron.treinar(entradas_treino, alvos)

entrada_teste = np.array([1,1])
saida_teste1 = perceptron.calc_saida(entrada_teste)

entrada_teste = np.array([0,1])
saida_teste2 = perceptron.calc_saida(entrada_teste)