#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: lmh
"""
import matplotlib.pyplot as plt
import numpy as np
from sympy.utilities.lambdify import lambdify, implemented_function, lambdastr
import sympy as sp
sf = sp.sympify
plt.rcParams['text.usetex'] = True

class plotfig(object):
    def __init__(self,**kwargs):
        self.fig = None
        self.ax = None
        self.initfig(**kwargs)

        self.x = sp.symbols('x', real=True)

        self.X = np.linspace(-10,10,1000)
        
    def initfig(self,h=1,v=1,size=1.5,sharex=True,sharey=True,wspace = 0.2,hspace = 0.2,figsize=[6,2]):
        self.fig, self.ax = plt.subplots(v,h,sharey=sharey,sharex=sharex,figsize=tuple(np.array(figsize)*size))
        self.fig.subplots_adjust(wspace = wspace,hspace = hspace)
        try: self.ax = list(self.ax.flatten())
        except: self.ax = [self.ax]

    def symplot(self, *args, **kwargs,):
        confs = {
                'ax'   : None, 
                'idx'  : 0, 
                'x'    : [-10,10,1000],
                'lims' : [None, None, None, None],
                'style': {},
                }
        confs.update(kwargs)
        plotstyle = {
                    #'color'     : '#1f77b4',
                    #'marker'    : None,
                    #'linestyle' : '-',
                    #'linewidth' : 1,
                    #'markersize': 5,
                    #'clip_on'   : True,
                    }
        plotstyle.update(confs['style'])
        
        if isinstance(confs['ax'],type(None)): ax = self.ax[confs['idx']]
        X = np.linspace(*confs['x'])
        for f in args:
            VARS = tuple(list(f.free_symbols))
            f_l = lambdify(VARS,f)
            Y = f_l(X)
            ax.plot(X,Y,**plotstyle)
        
    def plot(self,x,y,idx=0,ax=None,xl=None,yl=None,title=None,args={}):
        if isinstance(ax,type(None)): ax = self.ax[idx]

        plotstyle = {
                    'color'     : 'black',
                    'marker'    : 'x',
                    'linestyle' : 'None',
#                    'linewidth' : 1,
                    'markersize': 5,
                    'clip_on'   : True,
                    }
        plotstyle.update(args)
        ax.plot(x.m,y.m,**plotstyle)
        if xl != None:
            ax.set_xlabel(u'%s in %s'%(xl,"{:~P}".format(x.u)))
        if yl != None:
            ax.set_ylabel(u'%s in %s'%(yl,"{:~P}".format(y.u)))
        if title!=None:
            ax.set_title(title)
            
    def scheme_scale(self,ax,margin=0.5):
        ax.axis(False)
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        ax.set_xlim(xmin-margin, xmax+margin)
        ax.set_ylim(ymin-margin, ymax+margin)
        
    def grid(self,grain: list = [1,0.1,1,0.1], idx='all',ax=None,):
        """
        grain: [X-Major, Y-Major, X-Minor, Y-Minor]
        """
        axes = self.get_ax(ax=ax,idx=idx)
        for ax in axes:
            if grain[0]!= None:
                ax.xaxis.set_major_locator(plt.MultipleLocator(grain[0]))
            if grain[2]!= None:
                ax.yaxis.set_major_locator(plt.MultipleLocator(grain[2]))
            if grain[1]!= None:
                ax.xaxis.set_minor_locator(plt.MultipleLocator(grain[1]))
            if grain[3]!= None:
                ax.yaxis.set_minor_locator(plt.MultipleLocator(grain[3]))
            ax.grid(True,which='both')

    def get_ax(self,ax=None,idx='all'):
        if isinstance(idx,str):
            if idx=='all':
                axes = self.ax
                
        if isinstance(ax,type(None)) & isinstance(idx,int):
            axes = [ self.ax[idx] ]  
        
        return axes

    def arrowed_spines(self,ax=None,idx='all',equal=False, delta=0.2, lims: list = [None, None, None, None], ceil_lims = True):
        axes = self.get_ax(ax=ax,idx=idx)
        for ax in axes:
            self.set_lims(ax,lims=lims)
            if ceil_lims:
                _, _, _, _ = self.ceil_lims(ax)
            self.arrowed_spines_for_ax(ax,delta=delta)
        
        if equal: _ = [ ax.set_aspect('equal') for ax in axes ]
            
            
    def arrowed_spines_for_ax(self, ax,delta=0.2):
        # https://matplotlib.org/stable/gallery/spines/centered_spines_with_arrows.html
        # Move the left and bottom spines to x = 0 and y = 0, respectively.
        ax.spines[["left", "bottom"]].set_position(("data", 0))
        # Hide the top and right spines.
        ax.spines[["top", "right"]].set_visible(False)

        # Draw arrows (as black triangles: ">k"/"^k") at the end of the axes.  In each
        # case, one of the coordinates (0) is a data coordinate (i.e., y = 0 or x = 0,
        # respectively) and the other one (1) is an axes coordinate (i.e., at the very
        # right/top of the axes).  Also, disable clipping (clip_on=False) as the marker
        # actually spills out of the axes.
        ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

        # Ensure axis labels even if axis are shared
        ax.xaxis.set_tick_params(labelbottom=True)
        ax.yaxis.set_tick_params(labelleft=True)

        # hide 0 tick labels not to overlap with axis
        xticks = [float(k.get_position()[0]) for k in ax.xaxis.get_majorticklabels()]
        yticks = [float(k.get_position()[1]) for k in ax.yaxis.get_majorticklabels()]
        
        # hide ticks
        ax.tick_params(left=False, bottom=False)

        ## hide x 0 conditional
        if 0 in xticks:
            if not (yticks.index(0)==1) :
                ax.xaxis.get_major_ticks()[xticks.index(0)].label1.set_visible(False)

        ## always hide y 0
        if 0 in yticks:
            ax.yaxis.get_major_ticks()[yticks.index(0)].label1.set_visible(False)
        
        ## hide last x and y ticks
        xmin, xmax = ax.get_xlim() 
        ymin, ymax = ax.get_ylim()
        
        if xmax in xticks:
            ax.xaxis.get_major_ticks()[xticks.index(xmax)].label1.set_visible(False)

        if ymax in yticks:
            ax.yaxis.get_major_ticks()[yticks.index(ymax)].label1.set_visible(False)
        
        # Annotate x and y        
        ax.annotate('$x$', xy=(1,0), xytext=(xmax, -delta), transform=ax.transAxes, ha='center', va='center',fontsize=12)
        ax.annotate('$y$', xy=(0,1), xytext=(-delta, ymax), transform=ax.transAxes, ha='center', va='center',fontsize=12)

    def ceil_lims(self,ax):
        xmin, xmax = ax.get_xlim() 
        ymin, ymax = ax.get_ylim()

        ax.set_xlim(np.ceil(np.abs(xmin))*np.sign(xmin), np.ceil(np.abs(xmax))*np.sign(xmax))
        ax.set_ylim(np.ceil(np.abs(ymin))*np.sign(ymin), np.ceil(np.abs(ymax))*np.sign(ymax))

        xmin, xmax = ax.get_xlim() 
        ymin, ymax = ax.get_ylim()

        return xmin, xmax, ymin, ymax
    
    def set_lims(self,ax, lims: list = [None, None, None, None]):
        """
        lims = [xmin, xmax, ymin, ymax]
        """
        if lims[0] != None: ax.set_xlim(left=lims[0])
        if lims[1] != None: ax.set_xlim(right=lims[1])
        if lims[2] != None: ax.set_ylim(bottom=lims[2])
        if lims[3] != None: ax.set_ylim(top=lims[3])

        xmin, xmax = ax.get_xlim() 
        ymin, ymax = ax.get_ylim()

        return xmin, xmax, ymin, ymax

    def save(self,savename: str='plot', **kwargs):
        cvars =         {
                        'bbox_inches'   : 'tight',
                        'pad_inches'    : 0,
                        'dpi'           : 400,
                        'format'      : 'pdf',
                        }
        cvars.update(kwargs)
        
        self.fig.savefig(savename+'.'+cvars['format'], **cvars)