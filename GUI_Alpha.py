#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os.path
import subprocess

# Librerias necesarias para la ejecucion de la interfaz
import Alpha
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox,QWidget,QVBoxLayout,QApplication
from Modulo_1 import *
from Zona_fresnel import *
from levantar_perfil import *
from atenuaciones import *

#Librerias que permiten plotear en la interfaz
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

#Se crea la clase para elaborar las graficas en la interfaz
class MatplotlibWidget(QWidget):
    def __init__(self,parent= None):
        super(MatplotlibWidget, self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axis = self.figure.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.layoutvertical = QVBoxLayout(self)
        self.layoutvertical.addWidget(self.toolbar)
        self.layoutvertical.addWidget(self.canvas)
        
#Clase principal donde se ejecuta la interfaz        
class MainWidget(QWidget, Alpha.Ui_Form):
    #Inicizlizacion de variables e interfaz
     def __init__(self):
         super(MainWidget,self).__init__()
         self.setupUi(self)
         self.init_widget()
         
         #Variable de control para estado de checkbox
         self.check = 2
         self.torre = '0'
         
         self.boton1.clicked.connect(self.getDEM)
         self.boton7.clicked.connect(self.calculos)
         self.checkTorre.stateChanged.connect(self.estadoTorre)
     
     #Funcion para cambiar el estado en caso de existir torre fija
     def estadoTorre(self):
         if self.check == 1:
             self.check = 0
         else:
             self.check = 1
 
     
    #Funcion para crear widget en la interfaz 
     def init_widget(self):
         self.matplotlibwidget = MatplotlibWidget()
         self.layoutvertical = QVBoxLayout(self.widget1)
         self.layoutvertical.addWidget(self.matplotlibwidget)
    
    #Funcion para obtener la ruta del archivo .tif
     def getDEM(self):
         
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open file', '/home')
        self.fn_dem = str(filename)
        self.dirDem.setText(self.fn_dem)


    #Funcion principal que para calcular los datos del radio enlace
     def calculos(self):
         
        QApplication.setOverrideCursor(Qt.WaitCursor)#El cursor cambia de icono (cargando)
        fn_dem = self.fn_dem #Se captura la ruta del archivo .tif
        

        #Lectura de archivos .tif con libreria de GDAL        
        ds = gdal.Open(fn_dem) #Se obtiene todos los datos en el archivo cargado
        vector_dem = ds.GetRasterBand(1).ReadAsArray() #Matriz con datos de elevacion 
        
        gt = ds.GetGeoTransform() 
        Xsize = ds.RasterXSize # tamaño en X
        Ysize = ds.RasterYSize # tamaño en Y
        
        #Obtencion de coordenadas del archivo
        puntos = puntos_(gt, Xsize, Ysize)

        # Limites 
        resolucion = gt[1]
        
        L1 = puntos[0] # origen uly, ulx
        L2 = puntos[1] # opuesto a origen lry, lrx

        L3 = puntos[2] # lly, llx
        L4 = puntos[3] # ury. urx
        
        #TOMA DE PUNTOS
        p10 = self.p1La.text() #Latitud TX
        p11 = self.p1Lo.text() #Longitud TX
        p20 = self.p2La.text() #Latitud RX
        p21 = self.p2Lo.text() #Longitud RX
        #Conversion de variables String -> Float
        p10 = float(p10)
        p11 = float(p11)
        p20 = float(p20)
        p21 = float(p21)

        #CAPTURA DE VARIABLES DE ENTRADA
        f = self.frecuencia.text() #Frecuencia[GHz]
        n = self.nzf.text() #Numero zona frensel
        n = int(n) #Conversion String -> Integer
        
        nElement = self.Gt.text()  #Numero de elementos en arreglo
        nElement = float(nElement) #Conversion String -> Float
        
        gainR = self.Gr.text()  #Ganancia por elemento en arreglo
        gainR = float(gainR) #Conversion String -> Float
        
        gmax_db = round(10*np.log10(nElement*gainR),2) #Calculo de ganancia maxima para arreglo de antenas
        
        #Validacion de archivos cargados
        if ".tif" != os.path.splitext(fn_dem)[1]:
            QMessageBox.about(self, "Error", "Archivo dem incorrecto")
            QApplication.restoreOverrideCursor() #Detener cargando en el cursor
            return
        
        if str.isdigit(f) == False:
            QMessageBox.about(self, "Error", "Reingrese frecuencia")
            QApplication.restoreOverrideCursor() #Detener cargando en el cursor
            return        
        f = float(f)
        
        #Coordenadas 
        cd1 = [p10,p11] #TX
        cd2 = [p20,p21] #RX
        
        #Comprueba si las coordenadas digitadas se encuentras en rango
        banderasC = verificar_limites(L1, L2, cd1, cd2)
        
        P1 = coordenadas_Geo2cart(cd1[0], cd1[1], resolucion, L1) # y1, x1 /TX
        P2 = coordenadas_Geo2cart(cd2[0], cd2[1], resolucion, L1) # y2, x2 /RX
        
        #Verificar Coordenadas 
        if banderasC[0] == False or banderasC[1] == False:
            ##Ventana emergente
            if banderasC[0] == False:
                QMessageBox.about(self, "Error", "Reingrese coordenada RX")
            if banderasC[1] == False:
                QMessageBox.about(self, "Error", "Reingrese coordenada TX")
            QApplication.restoreOverrideCursor()#Detener cargando en el cursor
            return
        
        #Calculo de perfil de elevacion y distancia entre coordenadas 
        Perfil, distancia_x =  levantar_perfil(vector_dem, P1, P2, resolucion)

        self.perfil = Perfil
        self.distancia_x = distancia_x
        distancia = float(np.max(self.distancia_x))

        #Se capturan variables para calculo de atenuacion por lluvias
        por = self.porcentaje.currentText() #Porcentaje excedido de lluvia
        por = float(por) #Conversion String -> Float
        zon = self.zona.currentText() #Zonade lluvias en el mapa
        zon = str(zon) #Conversion String -> Float
        
        #Promedio de latitud para calculo de variables 
        lat = (p10+p20)/2        
        
        #CALCULO ALTURA DE TORRES
 
        estado = int(self.check) #Se comprueba si existe torre fija 
        
        torre_fija = str(self.torreFija.currentText()) #Se comprueba torre fija en TX/RX
        htorre = self.htorre.text() #Altura de torre fija
        
        #Se captura altura de torre en caso de existir una torre fija
        if estado ==1:
            htorre = float(htorre)
            
        asn = np.max(self.perfil)/1e3 #Altura sobre el nivel del mar
        
        #CALCULO POTENCIA RECIBIDA Y POTENCIA DE RUIDO
        [Pr_v, Pr_h, PN_dbm] = atenuaciones(f,distancia,gmax_db,gmax_db,por,zon,lat,asn)
        
        #Calculo de altura torres, zona fresnel y linea de vista
        self.htorres, rn, vector = calculo_torres(f,self.distancia_x,self.perfil,estado,torre_fija,htorre,n)                             
        
        #Verificar si variable es flotante o arreglo
        if(isinstance(self.htorres, float) == False):
            self.htorres = self.htorres[0]
        #Calculo angulos de antenas  
        angulo1,angulo2 = angulos(vector[0], vector[-1], self.distancia_x[-1])
        
        #Codigo para plotear
        self.matplotlibwidget.axis.clear() #Se borra grafica actual
        self.matplotlibwidget.axis.plot(self.distancia_x, self.perfil, linewidth=2 , label = 'DEM') #Grafica perfil elevacion
        self.matplotlibwidget.axis.plot(self.distancia_x, vector,label = 'LoS') #Grafica linea de vista
        self.matplotlibwidget.axis.grid() #Se activa malla en la grafica
        self.matplotlibwidget.axis.scatter(self.distancia_x[0],vector[0],s=10,color="red") #Punto en TX
        self.matplotlibwidget.axis.scatter(self.distancia_x[-1],vector[-1],s=10,color="green") #Punto en RX
        self.matplotlibwidget.axis.annotate('TX', (self.distancia_x[0],vector[0])) #Nombrar punto TX
        self.matplotlibwidget.axis.annotate('RX', (self.distancia_x[-1],vector[-1])) #Nombrar punto RX
        self.matplotlibwidget.axis.set_title("Perfil de Elevación") #Titulo grafica
        self.matplotlibwidget.axis.set_xlabel("Distancia [km]") #Titulo eje x
        self.matplotlibwidget.axis.set_ylabel("Altura [m]") #Titulo eje y
        self.matplotlibwidget.axis.legend() #Mostrar nombres de cada plot
        self.matplotlibwidget.canvas.draw() #Dibujar en widget
        
        #Publicacion de resultados
        if estado !=1:
            resultado = f'''Altura torres: {round(self.htorres,2)} m
Distancia: {round(distancia,2)} km   
Zona Fresnel: {round(rn,2)} m
Potencia Vertical:  {round(Pr_v,2)} dBm
Potencia Horizontal:  {round(Pr_h,2)} dBm
Potencia Ruido:  {round(PN_dbm,2)} dBm
Angulos: {angulo1}°, {angulo2}°
SNR: {round((Pr_v) - PN_dbm,2)}
        '''
        else:
            if torre_fija == 'RX':
                torre_fija = 'TX'
            else: 
                torre_fija = 'RX'
            resultado = f'''Altura torre {torre_fija}: {round(self.htorres,2)} m
Distancia: {round(distancia,2)} km   
Zona Fresnel: {round(rn,2)} m
Potencia Vertical:  {round(Pr_v,2)} dBm
Potencia Horizontal:  {round(Pr_h,2)} dBm
Potencia Ruido:  {round(PN_dbm,2)} dBm 
Angulos: {angulo1}°, {angulo2}°
SNR: {round((Pr_v) - PN_dbm,2)}
        '''     
        self.resultados.setText(resultado) #Mostrar resultados en pantalla
        
    
        QApplication.restoreOverrideCursor() #Detener cargando en el cursor
    
         
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWidget()
    w.show()
    sys.exit(app.exec_())

        
