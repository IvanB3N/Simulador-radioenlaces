#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def espacio_libre(F, D):
    """
    Modelo de propagacion espacio libre

    Parameters
    ----------
    F : TYPE float
        DESCRIPTION. frecuecia de operacion [MHz]
    D : TYPE float
        DESCRIPTION. distancia del radioenlace [Km]

    Returns
    -------
    Lfs : TYPE float
        DESCRIPTION. Potencia recibida [dB]

    """   
    F = F*1000
    Lfs = 32.45 + 20*np.log10(F) + 20*np.log10(D)
    
    return Lfs
