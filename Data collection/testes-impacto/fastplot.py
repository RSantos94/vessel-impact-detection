#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 10:17:08 2021

@author: marcelino
@author: Ruben santos
"""

import numpy as np
import matplotlib.pyplot as plt

def desenha(x,y,ytxt,fname):
    ymax=0
    ymin=0
    xtmax=0
    xtmin=0
    n=0
    janelinha=100
    for xi,yi in zip(x,y):
        if yi>ymax:
            ymax=yi
            xtmax=xi
            posmax=n
        if yi<ymin:
            ymin=yi
            xtmin=xi
            posmin=n
        n+=1
        
    plt.plot(x,y)
    plt.text(xtmax,ymax,"v="+format(ymax,"6.2f")+"@ t="+format(xtmax,"6.2f"))
    plt.text(xtmin,ymin,"v="+format(ymin,"6.2f")+"@ t="+format(xtmin,"6.2f"))

    plt.xlabel("tempo (s)")
    plt.ylabel(ytxt)
    plt.savefig(testname+"-"+accelname+"-"+fname)
    plt.show()
    plt.clf()
    pos1=min(posmax,posmin)-int(janelinha/2)
    pos2=max(posmax,posmin)+int(janelinha*1.5)
    
    zoomplot(x[pos1:pos2],y[pos1:pos2],ytxt,testname+"-"+accelname+"-zoom_"+fname)
    
def zoomplot(x,y,ytxt,fname):
    ymax=0
    ymin=0
    xtmax=0
    xtmin=0
    n=0
    for xi,yi in zip(x,y):
        if yi>ymax:
            ymax=yi
            xtmax=xi
        if yi<ymin:
            ymin=yi
            xtmin=xi
        n+=1
        
    plt.plot(x,y)
    plt.text(xtmax,ymax,"v="+format(ymax,"6.2f")+"@ t="+format(xtmax,"6.2f"))
    plt.text(xtmin,ymin,"v="+format(ymin,"6.2f")+"@ t="+format(xtmin,"6.2f"))

    plt.xlabel("tempo (s)")
    plt.ylabel(ytxt)
    plt.savefig(fname)
    plt.show()
    plt.clf()
    
def loaddata(fname,skiprows,skipcolumn):
    f=open(fname,"r")
    linhas=f.readlines()
    f.close()
    resultado=[]
    for l in range(skiprows,len(linhas)):
        linha=linhas[l].strip().split(",")
        resultado.append(linha[skipcolumn:])
    return resultado

testpath = "testes-impacto"
testname = "teste-009"
accelname = "acc003"
filename = testname+"/data-"+accelname+".csv"
dados=loaddata(filename,2,1)


dados=np.array(dados)

leg=["ax (m/s²)","ay (m/s²)","az (m/s²)"]
# array de tempo
tempo=[]
n=0
for t in dados[:,6]:
    tt=float(t)/1000.
    if n>0:
        if tt<tempo[-1]:
            print("erro",n,tt,tempo[-1])
    tempo.append(float(t)/1000.)
    n+=1

# leituras a retirar no fim e no início por causa do posicionamento do equipamento
nleitfin=1000
tempo=tempo[1000:n-nleitfin]

for c in range(3):
    y=[]
    for acel in dados[:,c]:
        y.append(float(acel)/1000.)
        
    y1=y[1000:n-nleitfin]
    ymed=sum(y1)/len(y1)
    y=[]
    for yi in y1:
        y.append(yi-ymed)
    print(len(tempo),len(y))
    desenha(tempo,y,leg[c],str(c)+".png")
    
    # determinar picos e desenhar
    maximo=max(y)
    # admite-se que sempre que o aceleração ultrapassar amax/4 é uma pancada
    encosto=maximo/4.
    janela=500
    ni=0
    i=0
    # correr todo o array para detetar e desenhar os picos 
    while i<len(y):
        if y[i]>encosto:
            # desenhar janela
            ni+=1
            antes=int(janela/2)
            depois=janela
            desenha(tempo[i-antes:i+depois],y[i-antes:i+depois],leg[c],"Enc_d"+str(c+1)+"_"+str(ni))
            i+=janela
        else:
            i+=1