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
import pandas as pd

import uncertainties
from uncertainties import ufloat
import difflib

# units
ureg = pn.UnitRegistry(system='mks',autoconvert_offset_to_baseunit=True)
pe = ureg.parse_expression

ureg.define('fraction = [] = frac')
ureg.define('percent = 1e-2 frac = pct')
ureg.define('ppm = 1e-6 fraction')
ureg.default_format = 'P'


# CONSTANTS
import scipy.constants as cm

class PhysicalConstants:
    def __init__(self, **kwargs):
        self.constants = {
            'g': 'standard acceleration of gravity',
            'm_e': 'electron mass',
            'e': 'elementary charge',
            'c': 'speed of light in vacuum',
            'hp': 'Planck constant',
            'e0': 'electric constant'
        }
        self.constants.update(kwargs)
        self.constants_df = pd.DataFrame(cm.physical_constants).T
        self.constants_df['c'] = self.constants_df.index
        self.constants_df = self.constants_df.reset_index(drop=True)

        # Attribute während der Initialisierung setzen
        self._set_initial_attributes()

    def _set_initial_attributes(self):
        for constant_name, quant in self.constants.items():
            setattr(self, constant_name, self.get_constant(quant))

    def get_constant(self, quant):
        row = self.constants_df[self.constants_df['c'] == quant].reset_index(drop=True)
        constant_value = row[0][0] * ureg(row[1][0])
        return constant_value

    def populate_namespace(self, namespace=None):
        if namespace is None:
            namespace = globals()

        for constant_name in dir(self):
            if not constant_name.startswith('_') and hasattr(self, constant_name) and constant_name not in namespace:
                namespace[constant_name] = getattr(self, constant_name)
                
    def search_constant(self, search_term):
        # Suche nach dem Suchbegriff in den Konstantennamen
        matched_constants = self.constants_df['c'].str.contains(search_term, case=False)

        # Extrahiere die Zeilen, die Übereinstimmungen haben
        matching_rows = self.constants_df[matched_constants].copy()

        # Verwende difflib, um die besten Übereinstimmungen und ihre Ähnlichkeiten zu finden
        matching_rows['matches'] = matching_rows['c'].apply(lambda x: difflib.get_close_matches(x.lower(), [search_term.lower()], n=3, cutoff=0.7))

        # Extrahiere die besten Übereinstimmungen und ihre Ähnlichkeiten
        matching_rows['best_matches'] = matching_rows['matches'].apply(lambda x: x[0] if x else None)
        matching_rows['match_similarity'] = matching_rows['matches'].apply(lambda x: difflib.SequenceMatcher(None, x[0], search_term.lower()).ratio() if x else None)

        # Sortiere die Ergebnisse nach der Ähnlichkeit absteigend
        matching_rows = matching_rows.sort_values(by=['match_similarity'], ascending=False)

        # Wähle die besten drei Treffer aus
        top_three_matches = matching_rows.head(3)[['c', 0, 1]].reset_index(drop=True)

        return top_three_matches
    
cn = PhysicalConstants()
cn.populate_namespace()


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
