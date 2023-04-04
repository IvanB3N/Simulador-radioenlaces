#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from osgeo import gdal
import math
import matplotlib.pyplot as plt

def verificar_limites(L1, L2, P1, P2):
	if L2[0] <= P1[0] <= L1[0] and L1[1] <= P1[1] <= L2[1]:
		flag_P1 = True
	else:
		flag_P1 = False

	if L2[0] <= P2[0] <= L1[0] and L1[1] <= P2[1] <= L2[1]:
		flag_P2 = True
	else:
		flag_P2 = False
		
	return flag_P1, flag_P2

def puntos_(gt, Xsize, Ysize):
    ulx = gt[0] # esquina superior izquierda x0
    uly = gt[3] # esquina superior izquierda y0
    res = gt[1] # resolucion
    

    lrx = ulx + Xsize*res # esquina superior derecha x1
    lry = uly - Ysize*res # esquina inferior izquierda y1
    
    punto1 = (uly, ulx) # esquina izquierda superior
    punto2 = (lry, lrx) # esquina derecha inferior
    punto3 = (lry, ulx) # esquina izquierda inferior
    punto4 = (uly, lrx) # esquina derecha superior
    
    
    return punto1, punto2, punto3, punto4

def round_well(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n) # toma la parte entera del numero
    return math.ceil(n) # retorna el numero entero mayor 2.2 => 3 

def coordenadas_Geo2cart(latitud, longitud, resolucion, L1):
    x = abs(round((L1[1]-longitud)/resolucion))
    y = abs(round((L1[0]-latitud)/resolucion))
    return y, x

   



