# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 10:10:03 2021

@author: Bruno
"""

import neurolab as nl

#função logica

entradas = [[0,0], [0,1], [1,0], [1,1]]
alvos = [[0], [1], [1], [0]]
         
#cria uma rede com duas entradas 

net = nl.net.newff([[0,1],[0,1]], [3,1])

#treina
error = net.train(entradas, alvos, epochs=100, show=1, goal=0.001)

import pylab as pl
pl.plot(error)
pl.xlabel('numero de épocas')
pl.ylabel('erro de treinamento')
pl.grid()
pl.show()

resultado = net.sim([[0,1]])
print(resultado)