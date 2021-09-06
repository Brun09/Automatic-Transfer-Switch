# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 15:53:05 2021

@author: Bruno
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    dados = pd.read_csv("iris.csv", sep=",", header = None)
    print(dados)
    
    dadosls = dados[:150]
    
    dadosls[4] = np.where(dados.iloc[:, -1]=='Iris-setosa', 1, 0)
    dadosls = np.asmatrix(dadosls, dtype = 'float64')
    return dadosls

class Perceptron(object):
    
    def __init__(self, num_entradas, epocas=10, taxa_aprendizagem=0.01):
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
            erro = 0
            for entradas, alvo in zip(entradas_treino, alvos):
                estimacao = self.calc_saida(entradas)
                erro = alvo - estimacao	
                self.pesos[1:] += np.squeeze(np.array(self.taxa_aprendizagem * erro * entradas))
                self.pesos[0] = self.taxa_aprendizagem * erro
                

basedados = load_data()

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
                
                
                
        
        
        
        
        
        
        
        
        
    