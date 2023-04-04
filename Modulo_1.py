#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# In[Librerias]
from osgeo import gdal, ogr
import numpy as np
import matplotlib.pyplot as plt
import math
import subprocess

# In[abrir raster]
def abrir_Imagen(nombre):
    ds = gdal.Open(nombre)
    if ds is None:
        print("Error al abrir la imagen")
    
    else:
        sist_referencia = ds.GetProjection()
        # Sist_referencia = Sist_referencia[:30] + ']'
        Caracteristicas = ds.GetGeoTransform()  
        vector_dem = ds.GetRasterBand(1).ReadAsArray().astype(float)
        
        
    return ds, sist_referencia, Caracteristicas, Caracteristicas[1], vector_dem

    
# In[Redondear]
def round_well(n):
    """
    Redondea el valor n

    Parameters
    ----------
    n : TYPE punto flotante
        DESCRIPTION. numero que se va a redondear

    Returns
    -------
    TYPE entero
        DESCRIPTION. numero rendondeado

    """
    if n - math.floor(n) < 0.5:
        return math.floor(n) # toma la parte entera del numero
    return math.ceil(n) # retorna el numero entero mayor 2.2 => 3    

# In[Perfil de elevacion]
def levantar_perfil(vector_dem, P1, P2, resolucion):
    """
    Realiza el Perfil de elevacion entre P1 y P2

    Parameters
    ----------
    vector_dem : TYPE float
        DESCRIPTION. valores de altura del modelo 
        de elevaciṕn digital
    P1 : TYPE float
        DESCRIPTION. punto inicial
    P2 : TYPE float
        DESCRIPTION. punto final
    resolucion : TYPE resolucion del DEM
        DESCRIPTION. resolucion obtenida con GetGeoTransform()

    Returns
    -------
    Perfil : TYPE vector float
        DESCRIPTION. valores de altura entre P1 y P2
    distancia_x : TYPE vector int
        DESCRIPTION. distancia entre el punto inicial y final

    """
    bandera = False
    r = [] # variable para hacer el cambio de variable
    a = 0
    i = 0
    pendiente = 0.0  # pendiente de la recta
    y = 0.0 # funcion de la recta y = mx + b
    acum = 0
    table = np.zeros([np.size(vector_dem, 1)+1, 2]) # vector donde ira los valores y de la recta
    L = 0
    
    # validar cual punto es mayor respecto a x
    if P1[0] > P2[0]:
        r = P1
        P1 = P2
        P2 = r
        bandera = True
        
    if P1[0] == P2[0] or P1[1] == P2[1]: # x1==x2 o y1==y2
        if P1[0] == P2[0]: # se encuentra en la misma columna x x1==x2
            if P1[1] > P2[1]:
                r = P1
                P1 = P2
                P2 = r
            Perfil = vector_dem[P1[0], P1[1]:P2[1]] #x1, y1:y2
            
        if P1[1] == P2[1]: # se encuentra en la misma fila y y1==y2
            Perfil = vector_dem[P1[0]:P2[0], P1[1]] #x1:x2, y1
                
        
        distancia_x = np.arange(len(Perfil))*0.0309
    
    else:
        pendiente = (P2[1]-P1[1])/(P2[0]-P1[0])
        #print('caso 2')
        for a in range(P1[0], P2[0]+1, 1):
            y = pendiente*(a - P1[0]) + P1[1] # funcion que representa la recta
        
            if y == round_well(y): # Numeros enteros
                table[i,:] = [a,y]
                acum += 1
            else: #Numeros Decimales
                if y % 0.5 == 0: # Guardar los velores de 0.5 el anterior y posterior
                    y = round_well(y)
                    table[i,:] = [a,y-1]
                    i += 1
                    table[i,:] = [a, y]
                    acum += 2
                    
                else: # Valores que No son multiplos de 0.5
                    y = round_well(y)
                    table[i,:] = [a,y]
                    acum += 1
            i += 1
        
        coordenadas = table[:acum,:]
        Perfil = np.zeros((len(coordenadas), 1))
        
        for i in range(0, len(coordenadas), 1):
            Perfil[i,:] = vector_dem[int(coordenadas[i,0]), int(coordenadas[i,1])]
           
        L = (np.sqrt((P2[0]-P1[0])**2
                      +(P2[1]-P1[1])**2)*0.0309)/(len(Perfil))
        distancia_x = np.arange(len(Perfil))*L
        
    
    if(bandera):
        return (np.flip(Perfil), distancia_x)#, coordenadas)
    else:
        return (Perfil, distancia_x)#, coordenadas)

# In[funcion para graficar recta entre P1 y P2]
def Trazar_recta(P1, P2):
    """
    Grafica la recta entre los puntos P1 y P2

    Parameters
    ----------
    P1 : TYPE array int 1x2
        DESCRIPTION. Punto inicial
    P2 : TYPE array int 1x2
        DESCRIPTION. Punto final

    Returns
    -------
    y : TYPE array float
        DESCRIPTION. variable dependiente    x : TYPE array int
        DESCRIPTION. variable independiente 

    """
    
    acum = 0
    f = np.zeros((np.abs(P1[0]-P2[0])+1 ,1))
    
    if P1[0] > P2[0]:
        r = P1
        P1 = P2
        P2 = r
        
    if P1[0] == P2[0] or P1[1] == P2[1]: # x1==x2 o y1==y2
        if P1[0] == P2[0]: # se encuentra en la misma columna x x1==x2
            if P1[1] > P2[1]:
                r = P1
                P1 = P2
                P2 = r
            x = np.arange(P1[1], P2[1])
            y = np.ones((len(x)))*P1[0]
            
        if P1[1] == P2[1]: # se encuentra en la misma fila y y1==y2
            y = np.arange(P1[0], P2[0])
            x = np.ones((len(y)))*P1[1]
    
    else:
        pendiente = (P2[1]-P1[1])/(P2[0]-P1[0])
        for a in range(P2[0]):
            f[a] = pendiente*(a - P1[0]) + P1[1] # funcion que representa la recta
            acum += 1
        y = f[:acum]
        x = np.arange(len(y))
        
    return (y, x)



