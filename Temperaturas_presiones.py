#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def datos_climatologicos(lat, h, s):
    """
    Calculo Atmósfera de referencia anual para latitudes bajas, 
    medias y altas
    bajas < 22ª
    medias [22ª, 45ª]
    altas >45ª 
    Parameters
    ----------
    lat : TYPE float
        DESCRIPTION. latitud [deg]
    h : TYPE float
        DESCRIPTION. altura sobre el nivel del mar [km]
    s : TYPE string
        DESCRIPTION. estacion del año. invierno o verano 

    Returns
    -------
    T : TYPE float
        DESCRIPTION. Temperatura [ªK]
    P : TYPE flot
        DESCRIPTION. Presion atmosferica [hPa]
    e : TYPE float 
        DESCRIPTION. presion vapor de agua [hPa]

    """
    if lat < 22:
        # Calculo de temperaturas [ªK]
        if (0<=h<17):
            T = 300.4222 - 6.3533*h + 0.005886*h**2
        elif (17<=h<47):
            T = 194 + (h-17)*2.533
        elif (47<=h<52):
            T = 270
        elif (52<=h<80):
            T = 270 - (h-52)*3.0714
        elif (80<=h<=100):
            T = 184
        # calculo de presiones [hPa]
        if (0<=h<=10):
            P = 1012.0306 - 109.0338*h + 3.6316*h**2
        elif (10<h<=72):
            P_10 = 1012.0306 - 109.0338*10 + 3.6316*10**2
            P = P_10*np.exp(-0.147*(h-10))
        elif (72<h<=100):
            P_10 = 1012.0306 - 109.0338*10 + 3.6316*10**2
            P_72 = P_10*np.exp(-0.147*(72-10))
            P = P_72*np.exp(-0.165*(h-72))
        # densidad vapor de agua [g/m³]
        if (0<=h<=15):
            p_vapor = 19.6542*np.exp(-0.2313*h - 0.1122*h**2 + 0.01351*h**3 - 0.0005923*h**4)
        elif h>15:
            p_vapor = 0
            
    elif (22<=lat<=45):
        if (s=='verano'):
            # Calculo de temperaturas [ªK]
            if (0<=h<13):
                T = 294.9838 - 5.2159*h - 0.07109*h**2
            elif (13<=h<17):
                T = 215.5
            elif (17<=h<47):
                T = 215.5*np.exp((h-17)*0.008128)
            elif (47<=h<53):
                T = 275
            elif (53<=h<80):
                T = 275 + (1 - np.exp((h-53)*0.06))*20
            elif (80<=h<=100):
                T = 175
            # calculo de presiones [hPa]
            if (0<=h<=10):
                P = 1012.8186 - 111.5569*h + 3.8646*h**2
            elif (10<h<=72):
                P_10 = 1012.8186 - 111.5569*10 + 3.8646*10**2
                P = P_10*np.exp(-0.147*(h-10))
            elif (72<h<=100):
                P_10 = 1012.8186 - 111.5569*10 + 3.8646*10**2
                P_72 = P_10*np.exp(-0.147*(72-10))
                P = P_72*np.exp(-0.165*(h-72))
            
            # densidad vapor de agua [g/m³]
            if (0<=h<=15):
                p_vapor = 14.3542*np.exp(-0.4174*h - 0.02290*h**2 + 0.01351*h**3)
            elif h>15:
                p_vapor = 0
            
        elif (s=='invierno'):
            # Calculo de temperaturas [ªK]
            if (0<=h<10):
                T = 272.7241 - 3.6217*h - 0.1759*h**2
            elif (10<=h<33):
                T = 218
            elif (33<=h<47):
                T = 218 + (h-33)*3.3571
            elif (47<=h<53):
                T = 265
            elif (53<=h<80):
                T = 265 - (h-53)*2.0370
            elif (80<=h<=100):
                T = 210
            # calculo de presiones [hPa]
            if (0<=h<=10):
                P = 1018.8627 - 124.2954*h + 4.8307*h**2
            elif (10<h<=72):
                P_10 = 1018.8627 - 124.2954*10 + 4.8307*10**2
                P = P_10*np.exp(-0.147*(h-10))
            elif (72<h<=100):
                P_10 = 1018.8627 - 124.2954*10 + 4.8307*10**2
                P_72 = P_10*np.exp(-0.147*(72-10))
                P = P_72*np.exp(-0.155*(h-72))
            
            # densidad vapor de agua [g/m³]
            if (0<=h<=10):
                p_vapor = 3.4742*np.exp(-0.2697*h - 0.03604*h**2 + 0.0004489*h**3)
            elif h>10:
                p_vapor = 0
    
    elif lat>45:
        if (s=='verano'):
            # Calculo de temperaturas [ªK]
            if (0<=h<10):
                T = 286.8374 - 4.7805*h - 0.1402*h**2
            elif (10<=h<23):
                T = 225
            elif (23<=h<48):
                T = 225*np.exp((h-23)*0.008317)
            elif (48<=h<53):
                T = 277
            elif (53<=h<79):
                T = 277 - (h-53)*4.0769
            elif (79<=h<=100):
                T = 171
            # calculo de presiones [hPa]
            if (0<=h<=10):
                P = 1018.0278 - 113.2494*h + 3.9408*h**2
            elif (10<h<=72):
                P_10 = 1018.0278 - 113.2494*10 + 3.9408*10**2
                P = P_10*np.exp(-0.140*(h-10))
            elif (72<h<=100):
                P_10 = 1018.0278 - 113.2494*10 + 3.9408*10**2
                P_72 = P_10*np.exp(-0.140*(72-10))
                P = P_72*np.exp(-0.165*(h-72))
            
            # densidad vapor de agua [g/m³]
            if (0<=h<=15):
                p_vapor = 8.988*np.exp(-0.3614*h - 0.005402*h**2 - 0.001955*h**3)
            elif h>15:
                p_vapor = 0
        
        elif (s=='invierno'):
            # Calculo de temperaturas [ªK]
            if (0<=h<8.5):
                T = 257.4345 + 2.3474*h + 0.08473*h**2
            elif (8.5<=h<30):
                T = 217.5
            elif (30<=h<50):
                T = 217.5 + (h-30)*2.125
            elif (50<=h<54):
                T = 260
            elif (54<=h<=100):
                T = 260 - (h-54)*1.667
            # calculo de presiones [hPa]
            if (0<=h<=10):
                P = 1010.8828 - 122.2411*h + 4.554*h**2
            elif (10<h<=72):
                P_10 = 1010.8828 - 122.2411*10 + 4.554*10**2
                P = P_10*np.exp(-0.147*(h-10))
            elif (72<h<=100):
                P_10 = 1010.8828 - 122.2411*10 + 4.554*10**2
                P_72 = P_10*np.exp(-0.147*(72-10))
                P = P_72*np.exp(-0.150*(h-72))
            
            # densidad vapor de agua [g/m³]
            if (0<=h<=10):
                p_vapor = 1.2319*np.exp(0.07481*h - 0.0981*h**2 + 0.00281*h**3)
            elif h>10:
                p_vapor = 0
    
    # Presion vapor de agua [hPa]
    e = (p_vapor*T)/216.7
    
    return T, P, e