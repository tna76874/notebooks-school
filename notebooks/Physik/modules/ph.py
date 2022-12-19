#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
physics modules
"""
# modules
import pint as pn
from sympy.utilities.lambdify import lambdify, implemented_function, lambdastr
import sympy as sp
import numpy as np

import uncertainties
from uncertainties import ufloat

# units
ureg = pn.UnitRegistry(system='mks',autoconvert_offset_to_baseunit=True)
pe = ureg.parse_expression

ureg.define('fraction = [] = frac')
ureg.define('percent = 1e-2 frac = pct')
ureg.define('ppm = 1e-6 fraction')
ureg.default_format = 'P'

# classes
class einsetzen(object):
    def __init__(self, func=None,werte={}):
        self.werte = werte
        self.func = func
        
        if not isinstance(self.func,type(None)):
            self.ensure_sympy_func()
            self.ensure_sympy_vars()
            self.calc_missing_vars()
            self.print_result()
    
    def ensure_base_units():
        for key,value in self.werte.items():
            self.werte[key] = value.to_base_units()
        
    def ensure_sympy_func(self):
        if not isinstance(self.func,sp.core.symbol.Symbol):
            LS, RS = self.func.split("=")
            self.func = sp.sympify(LS)-sp.sympify(RS)
    
    def ensure_sympy_vars(self):
        sym_werte = {}
        for key,value in self.werte.items():
            if isinstance(key,sp.core.symbol.Symbol):
                sym_werte[key] = value
            else:
                sym_werte[sp.sympify(key)] = value
        self.werte = sym_werte
        
    def place_vals_in_funct(self,func,werte):
        if isinstance(func,pn.Quantity):
            unit = self.func.u
            func = self.func.m
        else:
            unit = 1
        lam = lambdify(tuple(werte.keys()),func)
        result = lam(*list(werte.values()))*unit
        result = result.to_base_units()
        return result
        
    def calc_missing_vars(self):
        symbols = list()
        for k in self.werte.keys(): symbols+=list(k.free_symbols)
        given_symbols = list(self.func.free_symbols)

        for i in list(set(given_symbols).difference(set(symbols))):
            if set(symbols).issubset((set(given_symbols)|set([i]))):
                sols = sp.solve(self.func,i)
                for idx, sol in enumerate(sols):
                    if len(sols)>1:
                        key = sp.sympify(str(i)+'_'+str(idx+1))
                    else:
                        key = i
                    self.werte[key] = self.place_vals_in_funct(sol,self.werte)
                    
    def print_result(self):
        for key,val in self.werte.items():
            print("{key}={val:~P}".format(key=str(key),val=val))
            
    def result(self):
        result = dict()
        for key,value in self.werte.items():
            result[str(key)] = value
        return result
