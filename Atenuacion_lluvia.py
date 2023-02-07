#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def atenuacion_lluvia(f, d, R, P):
    """
    Calcula la atenuacion debido a la lluvia para las polarizaciones 
    vertical y horizontal
    
    Parameters
    ----------
    f : TYPE float
        DESCRIPTION. frecuencia de operacion [GHz]
    d : TYPE float
        DESCRIPTION. distancia del radioenlace
    R : TYPE float
        DESCRIPTION. Intemsidad de lluvia mm/h
    P : TYPE float
        DESCRIPTION. Porcentaje de lluvia ½

    Returns
    -------
    Ap_v : TYPE float
        DESCRIPTION. Atenuacion debido a la lluvia en polarizacion vertical[dB]
    Ap_h : TYPE float
        DESCRIPTION. atenuacion debido a la lluvia en polarizacion horizontal [dB]

    """
    
    # In[CALCULO DE CONSTANTES PARA POLARIZACION VERTICAL]
    vertical = {1: [-3.80595, -3.44965, -0.39902, 0.50167],
                2: [0.56934, -0.22911, 0.73042, 1.07319],
                3: [0.81061, 0.51059, 0.11899, 0.27195],
                4: -0.16398,
                5: 0.63297,
                6: [-0.07771, 0.56727, -0.20238, -48.2991, 48.5833],
                7: [2.33840, 0.95545, 1.14520, 0.791669, 0.791459],
                8: [-0.76284, 0.54039, 0.26809, 0.116226, 0.116479],
                9: -0.053739,
                10: 0.83433}
    
    logk_v = 0
    for i in range(0,4):
        logk_v = logk_v + vertical[1][i]*np.exp(-((np.log10(f)-vertical[2][i])/vertical[3][i])**2)   
    logk_v = logk_v + vertical[4]*np.log10(f) + vertical[5]
    k_v = 10**logk_v
    
    alpha_v = 0
    for i in range(0,5):
        alpha_v = alpha_v + vertical[6][i]*np.exp(-((np.log10(f)-vertical[7][i])/vertical[8][i])**2)
    alpha_v = alpha_v + vertical[9]*np.log10(f) + vertical[10]
    
    r_v = 1/((0.477*d**(0.633)*R**(0.073*alpha_v)*f**0.123)-(10.579*(1-np.exp(-0.024*d))))
    
    if r_v > 2.5:
        r_v = 2.5
    
    Lef_v = d*r_v #d distancia del radioenlace [km]; r factor de distancia 
    Yr_v = k_v*(R**alpha_v)
    
    Av = Yr_v*Lef_v
    
    
    # In[CALCULO DE CONSTANTES PARA POLARIZACION HORIZONTAL]
    
    horizontal = {1: [-5.33980, -0.35351, -0.23789, -0.94158],
                  2: [-0.10008, 1.26970, 0.86036, 0.64552],
                  3: [1.13098, 0.45400, 0.15354, 0.16817],
                  4: -0.18961,
                  5: 0.71147,
                  6: [-0.14318, 0.29591, 0.32177, -5.37610, 16.1721],
                  7: [1.82442, 0.77564, 0.63773, -0.96230, -3.29980],
                  8: [-0.55187, 0.19822, 0.13164, 1.47828, 3.43990],
                  9: 0.67849,
                  10: -1.95537}
    
    logk_h = 0
    for i in range(0,4):
        logk_h = logk_h + horizontal[1][i]*np.exp(-((np.log10(f)-horizontal[2][i])/horizontal[3][i])**2)   
    logk_h = logk_h + horizontal[4]*np.log10(f) + horizontal[5]
    k_h = 10**logk_h
    
    alpha_h = 0
    for i in range(0,5):
        alpha_h = alpha_h + horizontal[6][i]*np.exp(-((np.log10(f)-horizontal[7][i])/horizontal[8][i])**2)
    alpha_h = alpha_h + horizontal[9]*np.log10(f) + horizontal[10]
    
    r_h = 1/((0.477*d**(0.633)*R**(0.073*alpha_h)*f**0.123)-(10.579*(1-np.exp(-0.024*d))))
    
    if r_h > 2.5:
        r_h = 2.5
    
    Lef_h = d*r_h #d distancia del radioenlace [km]; r factor de distancia 
    Yr_h = k_h*(R**alpha_h)
    
    Ah = Yr_h*Lef_h
    
    # In[Cálculo de la atenuación por lluvia excedida durante un porcentaje de tiempo p]
    
    if f>=10:
        C0 = 0.12 + 0.4*(np.log10(f/10)**0.8)
    else:
        C0 = 0.12
    
    C1 = (0.07**C0)*(0.12**(1-C0))
    C2 = 0.855*C0 + 0.546*(1-C0)
    C3 = 0.139*C0 + 0.043*(1-C0)
    
    Ap_v = Av*C1*P**(-(C2+(C3*np.log10(P)))) # atenuacion debido a la lluvia [dB]
    Ap_h = Ah*C1*P**(-(C2+(C3*np.log10(P)))) # atenuacion debido a la lluvia [dB]
    
    return Ap_v, Ap_h