#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import numpy as np

def calculo_torres(f,distancia_x,perfil,estado,torre_fija,htorre,n):
    '''
    Calculo altura de torres y zona Fresnel,  existen 3 casos para el caculo de estos parametros:
        
        1. No existen obstaculo entre los puntos y la linea de vista esta libre, se calcula solo la zona Fresnel
        2. Existe un obstaculo entre los puntos y la linea de vista esta obstruida, se calcula la altura de torres 
            necesaria y la zona Fresnel.
        3. Existe una torre fija en TX/RX, se calcula unicamente la altura de la nueva torre y la zona Frensel, se evalua 
            si existe un obstaculo. 

    Parameters
    ----------
    f : TYPE int
        DESCRIPTION. frecuecnia del radioenlace [GHz]
    distancia_x : TYPE np.array
        DESCRIPTION. vector con distancia del radioenlace [Km]
    perfil : TYPE np.array
        DESCRIPTION. vector con valores de altura entre los dos puntos del radioenlace [m]
    estado : TYPE int
        DESCRIPTION. bandera que indica la existencia de una torre fija o no
    torre_fija : TYPE string
        DESCRIPTION. indica donde se encuentra la torre fija TX/RX
    htorre : TYPE float
        DESCRIPTION. altura de la torre fija en caso de existir [m]
    n : TYPE int
        DESCRIPTION. numero de la zona Fresnel a calcular

    Returns
    -------
    htorres : TYPE float
        DESCRIPTION. altura de las torres o torre, calculada [m]
    rn : TYPE int
        DESCRIPTION. zona Fresnel calculada [m]
     vector + rn : TYPE np.array
        DESCRIPTION. vector con los valores para graficar la linea de vista (LoS)

    '''
    
    hobs = np.max(perfil) #Altura del punto mas alto en el perfil
    d1 = distancia_x[np.argmax(perfil)] #Distancia desde el inicio hasta el puntos mas alto
    d2 = np.max(distancia_x) - distancia_x[np.argmax(perfil)] #Distancia desde el punto mas alto al final
    d = np.max(distancia_x) #Distancia total
    c1 = perfil[0] #Valor de altura inicial
    c2 = perfil[-1] #Valor de altura final
    
    if estado == 1:                  #Indica que existe una torre fija cuando estado = 1
        if c1 == hobs or c2 == hobs: #El punto de altura mayor se encuentra en TX o RX
            d1 = d/2                 #Distancias iguales 
            d2 = d1
            rn = calculo_torres1(f,d1,d2,n) #Calculo zona fresnel
            
            #Calculo de torres y vector de Linea de vista libre sin torre fija
            vector, htorres = calcularLoSTorreFija(distancia_x, perfil, rn, torre_fija, htorre, estado,rn)
            
            #Calcular Zona Fresnel
            varRaw, varRaw_, ubicacionObs = calcularLoS(distancia_x, perfil,0) # Se obtiene ubicacion del obstaculo en el vector
            
            #En este caso, se toman nuevos valores de distancia, si existe un obstaculo entre los puntos
            if(ubicacionObs != 0):    
                d1 = distancia_x[ubicacionObs]
                d2 = np.max(distancia_x) - distancia_x[ubicacionObs]
                rn = calculo_torres1(f,d1,d2,n) #Es necesario calcular Zona Fresnel de nuevo si se cambia las distancias
            
            #Calculos con una torre fija
        else:
            if torre_fija == 'RX' : #La torre fija se encuentra en RX
                h1 = float(htorre) #Se captura el valor de la torre fija
                if c2>c1: #El valor de altura final es mayor que el final, se referencia puntos respecto al menor
                    hobs = hobs - c1
                    h = c2 - c1
                    htorres, rn = calculo_torres5(f, d2, d1, n, hobs, h1, h)
        #         
                
                if c1>c2 : #El valor de altura inicial es mayor que el final, se referencia puntos respecto al menor                  
                    hobs = hobs - c1
                    h = c1 - c2
                    htorres, rn = calculo_torres4(f, d1, d2, n, hobs, h1, h)
                vector, htorres = calcularLoSTorreFija(distancia_x, perfil, htorres, torre_fija, htorre, estado,rn)
        #          
            if torre_fija == 'TX' : #La torre fija se encuentra en TX
                h1 = float(htorre) #Se captura el valor de la torre fija
                if c2>c1: #El valor de altura final es mayor que el final, se referencia puntos respecto al menor
                    hobs = hobs - c1
                    h = c2 - c1
                    htorres, rn = calculo_torres4(f, d1, d2, n, hobs, h1, h)
        #         
                
                if c1>c2 : #El valor de altura inicial es mayor que el final, se referencia puntos respecto al menor 
                    hobs = hobs - c1
                    h = c1-c2                  
                    htorres, rn = calculo_torres5(f, d1, d2, n, hobs, h1, h) 
                    
                #Calculo de vector para graficar linea de vista y verificar si la altura de las torres es correcta
                vector, htorres = calcularLoSTorreFija(distancia_x, perfil, htorres, torre_fija, htorre, estado,rn)
        
                
    else: #Calculos sin torres fijas, estado es diferente de "1"
     
        if c1 == hobs or c2 == hobs: #Verificar que existe un  obstaculo entre Tx y Rx
            d1 = d/2                 #Distancias iguales 
            d2 = d1
            rn = calculo_torres1(f,d1,d2,n) #Calculo zona Fresnel
            
            vector, htorres , ubicacionObs = calcularLoS(distancia_x, perfil,0)# Se obtiene ubicacion del obstaculo en el vector
            
            #En este caso, se toman nuevos valores de distancia, si existe un obstaculo entre los puntos
            if(ubicacionObs != 0):
                d1 = distancia_x[ubicacionObs]
                d2 = np.max(distancia_x) - distancia_x[ubicacionObs]
                rn = calculo_torres1(f,d1,d2,n) #Es necesario calcular Zona Fresnel de nuevo si se cambia las distancias
   
        else:          
            if c2>c1: #El valor de altura final es mayor que el final, se referencia puntos respecto al menor
                hobs = hobs - c1
                h = c2 - c1
                htorres, rn = calculo_torres2(f, d1, d2, h, n, hobs)
   
    
            if c1==c2:
                # Los puntos Tx y Rx estan al mismo nivel
                htorres, rn = calculo_torres3(f, d2, d1, n, hobs)
    
                
            if c1>c2:#El valor de altura inicial es mayor que el final, se referencia puntos respecto al menor 
                hobs = hobs - c2
                h = c1 - c2
                htorres , rn= calculo_torres2(f, d2, d1, h, n, hobs)
                
        #Calculo de vector para graficar linea de vista y verificar si la altura de las torres es correcta        
        vector, htorres , varRaw = calcularLoS(distancia_x, perfil,htorres)
        
    return htorres, rn, vector + rn

#  Sin obstaculos
def calculo_torres1(f,d1,d2,n):
    #Calculo de zona Fresnel
    
    c = 3e8  # velocidad de la luz
    f = f*1e9
    lb = c/f  # longitud de onda
    
    rn = math.sqrt((n*lb*d1*d2)/(d1+d2)) #Calcula de zona Fresnel, distancias iguales
    
    return rn

#  Obstaculos en el trayecto
def calculo_torres2(f, d1, d2, a2, n, hobs):
    #Calculo de zona Fresnel
    
    c = 3e8 # velocidad de la luz
    f = f*1e9
    lb = c/f  # longitud de onda

    a = a2*d1/(d1+d2)  # altura de obstaculo LoS
    heff = a-hobs  # altura efectiva

    rn = math.sqrt((n*lb*d1*d2)/(d1+d2))  # zona fresnal numero n

    htorres = rn - heff  # altura torres

    return htorres, rn

#Sin obstaculo y torres al mismo nivel 
def calculo_torres3(f, d1, d2, n, hobs):
    #Calculo de zona Fresnel
    
    c = 3e8  # velocidad de la luz
    f = f*1e9
    lb = c/f  # longitud de onda

    rn = math.sqrt((n*lb*d1*d2)/(d1+d2))  # zona fresnal numero n

    htorres = rn + hobs  # altura torres

    return htorres, rn

#Altura torre fija caso 1
def calculo_torres4(f,d1,d2,n,hobs,h1,h):
    #Calculo de zona Fresnel
    
    c = 3e8  # velocidad de la luz
    f = f*1e9
    lb = c/f  # longitud de onda
    # hobs = 150 #altura obstaculo
    rn = math.sqrt((n*lb*d1*d2)/(d1+d2)) #zona fresnal numero n


    h2 = ((hobs-h1+rn)*((d1+d2)/d1)) - h - h1

    # hp = h-h1
    htorre = h2 #altura de la torre fija
    
    return htorre, rn

#Altura torre fija caso 2
def calculo_torres5(f,d1,d2,n,hobs,h1,h):
    #Calculo de zona Fresnel
    
    c = 3e8  # velocidad de la luz
    f = f*1e9
    lb = c/f  # longitud de onda
    # hobs = 150 #altura obstaculo
    rn = math.sqrt((n*lb*d1*d2)/(d1+d2)) #zona fresnal numero n


    h2 = ((hobs+rn-h1-h)*((d1+d2)/d1)) + hobs + rn

     
    htorre = h2# + h - h1#altura de la torre fija
    
    return htorre, rn



def angulos(h1,h2,d):
    '''
    Calcular los angulos de inclinacion entre los puntos 

    Parameters
    ----------
    h1 : TYPE float
        DESCRIPTION. valor de altura punto incial [m]
    h2 : TYPE float
        DESCRIPTION. valor de altura punto final [m]
    d : TYPE float
        DESCRIPTION. distancia entre los dos puntos [km]

    Returns
    -------
    TYPE angulo1 , angulo2
        DESCRIPTION. angulo de inclinacion 

    '''
    d = d*1000
    if (isinstance(h1, float) == False):
        h1 = h1[0]
        h2 = h2[0]
        
    if h1 > h2:
        h = h1-h2
                
        angulo1 = np.degrees(np.arctan(h/d))
        angulo2 = angulo1*(-1)
        return round(angulo1,2),round(angulo2,2)
    
    else:
        h = h2-h1
        angulo1 = np.degrees(np.arctan(h/d))
        angulo2 = angulo1*(-1)
        return round(angulo1,2),round(angulo2,2)

def calcularLoS(distancia_x, perfil,htorres):
    '''
    Calcular la linea de vista entre dos puntos, verificando si existe obscatulo entre estos

    Parameters
    ----------
    distancia_x : TYPE np.array
        DESCRIPTION. vector con distancia de radioenlace
    perfil : TYPE np.array
        DESCRIPTION. vector con valores de altura entre los dos puntos
    htorres : TYPE float
        DESCRIPTION. de altura de las torres

    Returns
    -------
    vector : TYPE np.array
        DESCRIPTION. vector con los valores de altura para la lina de vista sin obstrucciones 
    htorres + a: TYPE float
        DESCRIPTION. valor de las torres con la suma de altura para superar obstaculo, si existe
    ubicacionObs : TYPE int
        DESCRIPTION. valor de ubicacion en el vector, donde se encuentra el obstaculo

    '''
    perfilCrudo = np.copy(perfil) #Se copia el vector perfil para trabajar con este y no modificar original
     
    x1 = distancia_x[-1] #Valor x final
    x2 = distancia_x[0] #Valor x inicial
    y1 = perfilCrudo[-1] #Valor y final
    y2 = perfilCrudo[0] #Valor y inicial
    

    
    vector = generarVectorLoS(y1,y2,x1,x2,distancia_x) #Se calcula el vector linea de vista

    a , flag, ubicacionObs = verificarLoS(vector, perfilCrudo,htorres) #Verificar si existen obstaculos en vector de LoS
    if flag == True and htorres > a:
        vector = vector + a + htorres      #Se suman la variable 'a' en caso de obscatulo y la altura de torres        
    elif flag == True and htorres < a:
        vector = vector + a
    else:
        vector = vector + htorres
        
    return vector , a , ubicacionObs

def calcularLoSTorreFija(distancia_x, perfil,htorres,torre_fija,htorre,estado,rn):
    '''
    Calcular la linea de vista entre dos puntos cuando existe una torre fija, verificando si existe obstaculo entre estos

    Parameters
    ----------
    distancia_x : TYPE np.array
        DESCRIPTION. vector con distancia de radioenlace [km]
    perfil : TYPE np.array
        DESCRIPTION. vector con valores de altura entre los dos puntos [m]
    htorres : TYPE float
        DESCRIPTION. altura de las torres [m]
    torre_fija : TYPE string
        DESCRIPTION. indica donde se encuentra la torre fija TX/RX
    htorre : TYPE float
        DESCRIPTION. valor torre fija
    estado : TYPE int
        DESCRIPTION. bandera que indica la existencia de una torre fija o no
    rn : TYPE int
        DESCRIPTION. zona Fresnel calculada [m]

    Returns
    -------
    vector : TYPE np.array
        DESCRIPTION. vector con los valores de altura para la lina de vista sin obstrucciones 
    htorres + vector[i] - perfilCrudo[i] TYPE float
        DESCRIPTION. valor de altura de la torre fija

    '''
    
    perfilCrudo = np.copy(perfil) #Se copia el vector perfil para trabajar con este y no modificar original
    
    if (torre_fija == 'TX' and estado == 1):
        perfilCrudo[0] += htorre #Se suma el valor de la torre fija en TX
        perfilCrudo[-1] += htorres #Se suma el valor de zona Fresnel en RX
    elif(torre_fija == 'RX' and estado == 1):
        perfilCrudo[-1] += htorre #Se suma el valor de la torre fija en RX
        perfilCrudo[0] += htorres  #Se suma el valor de la zona Fresnel en TX
        
    
    x1 = distancia_x[-1] #Valor x final
    x2 = distancia_x[0] #Valor x inicial
    y1 = perfilCrudo[-1] #Valor y final
    y2 = perfilCrudo[0] #Valor y inicial
    

    
    vector = generarVectorLoS(y1,y2,x1,x2,distancia_x) #Se calcula el vector linea de vista

    
      
    if (estado ==1 and torre_fija == 'TX') :     #Caso de torre fija y existe obstaculo en LoS
        a,flag = verificarLoSTorreFija(vector, perfilCrudo)  #Verificar si existen obstaculos en vector de LoS con torre fija
        
        for i in range (100): # Se verifica que la linea de vista no sea obstruida
            if a==0:
                break
            vector = generarVectorLoS(vector[-1]+a+rn,vector[0],x1,x2,distancia_x)
            a,flag = verificarLoSTorreFija(vector, perfilCrudo) 
      
        return vector , htorres + vector[-1] - perfilCrudo[-1]
    elif (estado ==1 and torre_fija == 'RX'):
        a,flag = verificarLoSTorreFija(vector, perfilCrudo) 
        for i in range (100): # Se verifica que la linea de vista no sea obstruida
            if a==0:
                break
            vector = generarVectorLoS(vector[-1],vector[0]+a+rn,x1,x2,distancia_x)
            a,flag = verificarLoSTorreFija(vector, perfilCrudo) 

          
        return vector , htorres + vector[0] - perfilCrudo[0]


def generarVectorLoS(y1,y2,x1,x2,distancia_x):
    '''
    Se genera un vector con los valores entre dos coordendas usando ecuacion de la recta

    '''
    m =(y2 - y1)/(x2 - x1)#Se calcula ecuacion de la recta LoS
    b = y2 - m*x2
    
    vector = []
    for i in range(len(distancia_x)):        #Se crea el vector para graficar LoS
        vector.append(distancia_x[i]*m + b)
    vector = np.array(vector)
    
    return vector

def verificarLoS(vector, perfilCrudo,htorres):
    '''
    Se verifica que no existan obstaculos en la linea de vista, en caso de existir se captura el valor 
    de altura necesario para superar dicho obstaculo
    '''
    a = 0
    flag1 = False
    ubicacionObs = 0
    for i in range(len(vector)):    #Se comprueba que LoS no sea obstaculizada
        if vector[i] + htorres < perfilCrudo[i]:
            if perfilCrudo[i] - vector[i] > a:
                a = perfilCrudo[i] - vector[i]  #En caso de obstaculo, se guarda la altura de este
                flag1 = True
                ubicacionObs = i
    return a, flag1, ubicacionObs

def verificarLoSTorreFija(vector, perfilCrudo):
    '''
    Se verifica que no existan obstaculos en la linea de vista con torre fija, en caso de existir se captura el valor 
    de altura necesario para superar dicho obstaculo
    '''
    a = 0
    flag1 = False
    for i in range(len(vector)):    #Se comprueba que LoS no sea obstaculizada
        if vector[i] < perfilCrudo[i]:
            
            if perfilCrudo[i] - vector[i] > a:
                a = perfilCrudo[i] - vector[i]  #En caso de obstaculo, se guarda la altura de este  

                flag1 = True
  
    return a, flag1