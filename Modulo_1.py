# In[inicio. Pasos para el Modulo 1]
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
Pasos para el modulo 1: cargar y procesamiento de imagenes:
    1. Escoger la zona de interes en google earth y guardar el poligono con 
    extension .kml
    2. Descargar las imagenes de modelo de elevacion digital (DEM) 
    y las imagenes en multiples bandas
    3. Cargar todas las imagenes con gdal
    4. Referenciar todas las imagenes al mismo sistema de referencia,
    tener en cuenta la resolucion
    5. Pasar el poligono de kml a shp para cargarlo con ogr
    6. Recortar todas las imagenes con el poligono
    7. Ubicar lo dos puntos de interes para el radioenlace 
    8. Calcular el perfil de elevacion entre los dos puntos 
    9. Asignar el valor del indice de vegetacion normalizado a cada punto 
    del perfil de elevacion
"""

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
        
        # if sist_referencia[:30] != 'PROJCS["WGS 84 / UTM zone 18N"':
        #     resolucion = Caracteristicas[1]*100000
        # else:
        #     resolucion = Caracteristicas[1]
        
    return ds, sist_referencia, Caracteristicas, Caracteristicas[1], vector_dem

# In[Reproyectar]
def Reproyetar(imagen):
    [ds, sis_referencia, Caracteristicas, resolucion, vector_dem] = abrir_Imagen(imagen)
    
    if sis_referencia[:20]=='PROJCS["WGS 84 / UTM':
        ds = gdal.Warp(imagen, ds, dstSRS = "EPSG:4326")

# In[Validar la resolucion de los raster]
def Ajuste_res(imagen1, imagen2, imagen3):
    [ds, sis_referencia, Caracteristicas, resolucion, vector_dem] = abrir_Imagen(imagen1)
    [ds1, sis_referencia1, Caracteristicas1, resolucion1, vector_dem1] = abrir_Imagen(imagen2)
    [ds2, sis_referencia2, Caracteristicas2, resolucion2, vector_dem2] = abrir_Imagen(imagen3)
    
    if resolucion > resolucion1:
        print("1")
        resmax = resolucion
        ds1 = gdal.Warp(imagen2, ds1, xRes = resmax, yRes = resmax, resampleAlg = 'bilinear')
        ds2 = gdal.Warp(imagen3, ds2, xRes = resmax, yRes = resmax, resampleAlg = 'bilinear')
        
    if resolucion1 > resolucion: 
        print("2")
        resmax = resolucion1
        ds = gdal.Warp(imagen1, ds, xRes = resmax, yRes = resmax, resampleAlg = 'bilinear')
    
# In[convertir kml a shp]
def KmlToShp(input_file):
    output_file = input_file.replace('kml', 'shp')
    cmd = 'ogr2ogr -f "ESRI Shapefile"' + '\t' + output_file + '\t' + input_file
    subprocess.Popen(cmd,shell=True)
    return output_file
    
# In[Abrir archivo shp]
def abrir_Shp(fileName):
    file = ogr.Open("fileName") 
    shape = file.GetLayer(0)
    #first feature of the shapefile
    feature = shape.GetFeature(0)
    first = feature.ExportToJson()
    
    return first# (GeoJSON format)

# In[Recortar Raster]
def Recortar_raster(imagen, archivo_shp):
    [ds, proj, carac, resolucion, vec] = abrir_Imagen(imagen)
    output_tif = "Recorte.tif"
    Raster_clip = gdal.Warp(output_tif, ds, 
                            cutlineDSName = archivo_shp,
                    cropToCutline = True, dstNodata = 0)
    return Raster_clip, output_tif

def Recortar_raster1(imagen, archivo_shp):
    [ds, proj, carac, resolucion, vec] = abrir_Imagen(imagen)
    output_tif = "Recorte1.TIF"
    Raster_clip = gdal.Warp(output_tif, ds, 
                            cutlineDSName = archivo_shp,
                    cropToCutline = True, dstNodata = 0)
    return Raster_clip, output_tif

def Recortar_raster2(imagen, archivo_shp):
    [ds, proj, carac, resolucion, vec] = abrir_Imagen(imagen)
    output_tif = "Recorte2.TIF"#imagen
    Raster_clip = gdal.Warp(output_tif, ds, 
                            cutlineDSName = archivo_shp,
                    cropToCutline = True, dstNodata = 0)
    return Raster_clip, output_tif
    
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
        
        # L = (math.sqrt((P2[0]-P1[0])**2+(P2[1]-P1[1])**2)*resolucion*100)/len(Perfil)
        # distancia_x = np.arange(len(Perfil))*L
    
    print(f'''
              len perfi: {len(Perfil)}
              L: {L}
              ''') 
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

# In[Calculo de indice de vegetacion normalizado NDVI]
def ndvi(Banda_4, Banda_5, coordenadas):
    red = np.zeros((len(coordenadas), 1))
    nir = np.zeros((len(coordenadas), 1))
    
    (ds, proj, carac, res, vector_B4) = abrir_Imagen(Banda_4)
    (ds2, proj2, carac2, res2, vector_B5) = abrir_Imagen(Banda_5)
    
    for i in range(0, len(coordenadas), 1):
        red[i,:] = vector_B4[int(coordenadas[i,0]), int(coordenadas[i,1])]
        nir[i,:] = vector_B5[int(coordenadas[i,0]), int(coordenadas[i,1])]
    
    vector_ndvi = np.where(nir+red==0., 0, (nir-red)/(nir+red))
    
    return vector_ndvi

