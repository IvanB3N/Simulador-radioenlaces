#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Temperaturas_presiones import *
from espacio_libre import *
from Atenuacion_gases import *
from Atenuacion_lluvia import *
from Atenuacion_nubes import *
import math



def atenuaciones(f,d,Gr,Gt,por,zon,latitud,h):
    #Constantes extraidas de documentacion
    porcentajes = {
    'A' : [8,5,2,0.8,0.99] , #99% , 97% , 90% , 70% , 0%
    'B' : [12,6,3,2,0.5] ,   #[0] , [1] , [2] , [3] , [4]
    'C' : [15,9,5,2.8,0.7] ,
    'D' : [19,13,8,4.5,2.1] ,
    'E' : [22,12,6,2.4,0.6] ,
    'F' : [28,15,8,4.5,1.7] ,
    'G' : [30,20,12,7,3] , 
    'H' : [32,18,10,4,2] ,  
    'J' : [35,28,20,13,8] , 
    'K' : [42,23,12,4.2,1.5] , 
    'L' : [60,33,15,7,2] , 
    'M' : [63,40,22,11,4] , 
    'N' : [95,65,35,15,5] , 
    'P' : [145,105,65,34,12] , 
    'Q' : [115,96,72,49,24]     
    
    }

    dic = {99:0, 97:1, 90:2, 70:3, 0:4}
    
    estacion = 'verano' 
    
    porc = dic[por]

    R = porcentajes[zon][porc]

    pt = (100-por)/100 #  porcentaje de tiempo en un margen entre el 0,001% y 1% (%)

    M = 0.05 #g/m³

    Pt_max = 0.5 # watt Potencia de transmision maxima 500 mW

    [T, p, e] = datos_climatologicos(latitud, h, estacion)
    
    k = 1.39e-23 # Cosntante de Boltzman
    b = 1e9      # Ancho de banda mmWave
    pw = k*T*b   # Potencia de ruido
    
    PN_dbm = 10*math.log10(1000*pw)
    
    Lfs = espacio_libre(f, d)
    Ag = atenuacion_gases(f, T, p, e, d)
    [All_v, All_h] = atenuacion_lluvia(f, d, R, pt)
    An = atenuacion_nubes(f, M, d)

    Pt = 10*np.log10(Pt_max*1e3) # [dBm] potencia de trasmision

    Pr_v = Pt + Gt + Gr - Lfs - Ag - All_v - An #[dBm] Potencia recibida p. vertical
    Pr_h = Pt + Gt + Gr - Lfs - Ag - All_h - An #[dBm] Potencia recibida p. horizontal
    
    return Pr_v, Pr_h , PN_dbm
