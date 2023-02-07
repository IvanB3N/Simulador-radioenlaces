#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def atenuacion_nubes(f, M, d):
    """
    Calcula la atenuacion debida a las nubes

    Parameters
    ----------
    f : TYPE float
        DESCRIPTION. frecuencia de operacion [GHz]
    M : TYPE float
        DESCRIPTION. Densidad de agua líquida en la nube o la niebla [g/m³]
    d : TYPE float
        DESCRIPTION. distancia del radienlace [km]

    Returns
    -------
    A : TYPE float
        DESCRIPTION. Atenuacion [dB]

    """
    T = 273.15 # 0ªC
    theta = 300/T
    
    # La permitividad dieléctrica compleja del agua
    epsilon_0 = 77.66 + 103.3*(theta-1)
    epsilon_1 = 0.0671*epsilon_0
    epsilon_2 = 3.52
    
    # frecuencias de relajación principal fp y secundaria fs
    fp = 20.20 - 146*(theta-1) + 316*(theta-1)**2
    fs = 39.8*fp
    
    epsilon1 = (epsilon_0-epsilon_1)/(1+(f/fp)**2) + (epsilon_1-epsilon_2)/(1+(f/fs)**2) + epsilon_2
    epsilon2 = (f*(epsilon_0 - epsilon_1))/(fp*(1+(f/fp)**2)) + (f*(epsilon_1-epsilon_2))/(fs*(1++(f/fs)**2))
    n = (2 + epsilon1)/epsilon2
    K1 = (0.819*f)/(epsilon2*(1 + n**2))
    
    A = K1*M*d    
    return A