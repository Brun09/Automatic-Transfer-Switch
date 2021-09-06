# -*- coding: utf-8 -*-
"""
Spyder Editor

This is perceptron algorithm
"""

import numpy as np

class Perceptron(object):
    
    def __init__(self, num_entradas, epocas = 20, taxa_aprendizagem=0.01):
        self.epocas = epocas
        self.taxa_aprendizagem = taxa_aprendizagem
        #Os  pesos são todos inicializados aleatoriamente,
        #usando a função Numpy np.random.randn para gerar distribuições 
        #gaussianas com 0 de média e desvio padrão 1. Esta inicialização 
        #aleatória dá ao nosso algoritmo de descida do gradiente estocástico 
        #um local para começar.
        self.pesos = np.random.randn(num_entradas + 1) #mais 01 do bias
        
    
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
                self.pesos[1:] += self.taxa_aprendizagem * erro * entradas
                self.pesos[0] += self.taxa_aprendizagem * erro
                
#utilização

entradas_treino = []
entradas_treino.append(np.array([1, 1]))
entradas_treino.append(np.array([1, 0]))
entradas_treino.append(np.array([0, 1]))
entradas_treino.append(np.array([0, 0]))

#Saida OR
alvos = np.array([1, 1, 1, 0])

perceptron = Perceptron(2, 20, 0.01)#informamos apenas o numero de entradas (duas),
#demais entradas ficam com valores padrão
perceptron.treinar(entradas_treino, alvos)

entrada_teste = np.array([1,1])
saida_teste1 = perceptron.calc_saida(entrada_teste)

entrada_teste = np.array([0,1])
saida_teste2 = perceptron.calc_saida(entrada_teste)

