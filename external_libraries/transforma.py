# transforma.py
# J.Marcelino
# 2022-09-07/08


import numpy as np
import math
from matplotlib import pyplot as plt

def plotplac(plac,pontos,name):
    plac.append(plac[0])
    xy=np.array(plac)
    plt.plot(xy[:,0],xy[:,1],"-")
    xy=np.array(pontos)
    plt.plot(xy[:,0],xy[:,1],".")
    titulo=name.replace(".png","")
    plt.title(titulo)
    plt.axis("scaled")
    plt.savefig(name)
    plt.show()
    
def interpola(pqsieta,p2,Ns):
    qsi=pqsieta[0]
    eta=pqsieta[1]
    xy=np.array(p2)
    x=calcN(Ns[0],qsi,eta)*xy[0,0]+calcN(Ns[1],qsi,eta)*xy[1,0]+calcN(Ns[2],qsi,eta)*xy[2,0]+calcN(Ns[3],qsi,eta)*xy[3,0]
    y=calcN(Ns[0],qsi,eta)*xy[0,1]+calcN(Ns[1],qsi,eta)*xy[1,1]+calcN(Ns[2],qsi,eta)*xy[2,1]+calcN(Ns[3],qsi,eta)*xy[3,1]
    return x,y

def calcN(N,qsi,eta):
    return N[0]+N[1]*qsi+N[2]*eta+N[3]*qsi*eta

def fN(x,y): # cada polinómio
    return [1,x,y,x*y]

def calculaN(xy): 
    vN=[]
    for pt in xy: # define o polinómio associado a cada ponto
        vN.append(fN(pt[0],pt[1]))
    vN=np.array(vN)
    vN1=np.linalg.inv(vN)
    # define as funcões para darem 1 no ponto nodal e 0 nos restantes
    Ni=[]
    for i in range(4):
        zeroum=np.array([0,0,0,0])
        zeroum[i]=1
        Ni.append(vN1.dot(zeroum))
        
    return Ni
# transformação de coordenadas

p2=[[-100,-100],[100,-100],[100,100],[-100,100]] # referencial real
p1=[[50,10],[200,50],[180,90],[0,40]] # referencial foto



# calculo das funcões de interpolação
Ns=calculaN(p1)

# # definição de uma forma geométrica no espaço da foto
# # por exemplo um circulo
# r=30
# xc=180
# yc=90
# xy=[]

# for i in range(360):
    # xy.append([xc+r*math.cos(i),yc+r*math.sin(i)])

x1=(50+0)/2
x2=(200+180)/2

xy=[]
for i in range(100):
    xi=x1+(x2-x1)/100*i
    yi=10*math.sin(xi*3.14/180*4)+i
    xy.append([xi,yi])


# calcular na realidade
xyr=[]
for p in xy:
    xyr.append(interpola(p,p2,Ns))


plotplac(p1,xy,"na_foto.png")
plotplac(p2,xyr,"na_realidade.png")
