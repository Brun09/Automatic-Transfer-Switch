# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 10:38:39 2021

@author: Bruno
"""

import numpy as np
import pandas as pd
import neurolab as nl

def load_data():
    dados = pd.read_csv("iris.csv", sep=",", header = None)
    print(dados)

    #Selelciona apenas os 100 primeiros pontos, os quais correspondem as classes
    #Setosa e Versicolor (Classes linearmente separaveis)
    dadosls = dados[:150]
    #Subsititui na última coluna o label iris-setosa por 0 e iris-versicolor por 1
    #visando a classificação binaria
    dadosls[4] = np.where(dadosls.iloc[:, -1]=='Iris=setosa',1, np.where(dadosls.iloc[:, -1]=='Iris-versicolor', 0, -1))
    dadosls = np.asmatrix(dadosls, dtype = 'float64')
    return dadosls

basedados = load_data()

entradas = basedados[:,0:4]
alvos = basedados[:,-1]

#topologia da rede

dim1_min, dim1_max = entradas[:,0].min(), entradas[:,0].max()
dim2_min, dim2_max = entradas[:,1].min(), entradas[:,1].max()
dim3_min, dim3_max = entradas[:,2].min(), entradas[:,2].max()
dim4_min, dim4_max = entradas[:,3].min(), entradas[:,3].max()

dim1 = [dim1_min, dim1_max]
dim2 = [dim2_min, dim2_max]
dim3 = [dim3_min, dim3_max]
dim4 = [dim4_min, dim4_max]

num_saidas = 1
num_neu_ocultos = 4

net = nl.net.newff([dim1, dim2, dim3, dim4], [num_neu_ocultos, num_saidas])

error = net.train(entradas, alvos, epochs=500, show=1, goal=0.01)

import pylab as pl
pl.plot(error)
pl.xlabel('numero de épocas')
pl.ylabel('erro de treinamento')
pl.grid()
pl.show()

testes = [[5.1, 3.5, 1.4, 0.2]]

testev = [[7, 3.2, 4.7, 1.4]]

testei = [[6.3, 3.3, 6, 2.5]]

print("A saida para", testes, "é ", net.sim(testes))

print("A saida para", testev, "é ", net.sim(testev))

print("A saida para", testei, "é ", net.sim(testev))