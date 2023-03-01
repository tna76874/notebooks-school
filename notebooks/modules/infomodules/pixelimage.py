#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create pixel image
"""

from PIL import ImageColor, Image, ImageOps
from itertools import cycle
import numpy as np
import matplotlib.pyplot as plt


class pixelimage(object):
    def __init__(self,**kwargs):
        self.config={
                    }
        self.config.update(kwargs)
        self.fig = None
        self.ax = None
        
        self.set_colormap()
        
        self.image = None
        self.minbit = 4
        setattr(self, 'bnum', None)
        setattr(self, 'dims', None)
        setattr(self, 'bit', None)
        setattr(self, 'bw', None)
        setattr(self, 'bh', None)
        setattr(self, 'w', None)
        setattr(self, 'h', None)
        
    def set_colormap(self, one: str = "white" ):
        if one.lower()=="white":
            colormap = {'1' : ImageColor.getrgb("white"), '0' : ImageColor.getrgb("black") }
            cmapn = {'white' : '1' , 'black' : "0" }
        else:
            colormap = {'1' : ImageColor.getrgb("black"), '0' : ImageColor.getrgb("white") }
            cmapn = {'white' : '0' , 'black' : "1" }
        setattr(self, 'cmap', colormap)
        setattr(self, 'cmapn', cmapn)

    def update_attr(self):
        self.set_dims()
        config =    {
                    'bnum'  : self.bnum,
                    'dims'  : self.dims,
                    'bit'   : self.bit,
                    'bw'    : self.bw,
                    'bh'    : self.bh,
                    'w'     : self.w,
                    'h'     : self.h,
                    'whnum' : self.whnum,
                    }
        self.config.update(config)
        self.config.update(self.cmapn)
    
    def set_dims(self):
        bit = np.array([len(self.tobin(self.dims[0], mark=False)),len(self.tobin(self.dims[1], mark=False)), self.minbit]).max()
        setattr(self, 'bw', self.tobin(self.dims[0], mark=False, bit=bit))
        setattr(self, 'bh', self.tobin(self.dims[1], mark=False, bit=bit))
        setattr(self, 'bit', bit)
        w, h = self.dims
        setattr(self, 'w', w)
        setattr(self, 'h', h)
        setattr(self, 'whnum', str(self.bw)+str(self.bh)+str(self.bnum))
    
    def initfig(self,h=1,v=1,size=1.5,sharex=True,sharey=True,wspace = 0.2,hspace = 0.2,figsize=[6,2]):
        self.fig, self.ax = plt.subplots(v,h,sharey=sharey,sharex=sharex,figsize=tuple(np.array(figsize)*size))
        self.fig.subplots_adjust(wspace = wspace,hspace = hspace)
        try: self.ax = list(self.ax.flatten())
        except: self.ax = [self.ax]
        
    def read_pixel_image(self,path: str):
        rawimage = np.array(ImageOps.grayscale(Image.open(path)))
        dims = rawimage.shape[:2][::-1]

        image = list()
        for i in rawimage:
            image+=list(i)
            
        bnum = ''.join([ '1' if k > 100 else '0' for k in image ])

        setattr(self, 'bnum', bnum)
        setattr(self, 'dims', dims)

        self.update_attr()

    def create_pixel_image(self, bimage=None, imsize: tuple = (9, 9), minbit: int = 4):
        """ 
        https://towardsdatascience.com/how-to-resize-images-using-python-8aaba74602ed
        """
        
        if not isinstance(bimage,type(None)):
            binnumber = bimage
            self.bnum = bimage
            self.dims = imsize
        else:
            binnumber = self.bnum
            imsize = self.dims

        self.minbit = minbit
        self.update_attr()
        
        blocksize = 1
        width = imsize[0]
        height = imsize[1]
        img: list = []
        numbers = cycle(str(binnumber))
        for _ in range(height):
          row: list = []
          for _ in range(width):
            number = next(numbers)
            color = self.cmap[number]
            for _ in range(blocksize):
              values = list(color)
              row.append(values)
          [img.append(row) for _ in range(blocksize)] # creates row height
          
        self.image = np.flipud(img)
        
    def tobin(self,dez,bit=None,mark=True):
        bz = bin(dez).replace('0b','')
        if not isinstance(bit,type(None)):
            if len(bz)<bit:
                bz = ''.join(['0']*(bit-len(bz))) + bz
        if mark: bz += 'b'
        return bz
    
    def todez(self,bz):
        return int(str(bz).replace('b',''),2)
    
    def grid(self,ax,grain=[1,0.1,1,0.1]):
        if isinstance(ax,type(None)): ax = self.ax[idx]
        if grain[0]!= None:
            ax.xaxis.set_major_locator(plt.MultipleLocator(grain[0]))
        if grain[2]!= None:
            ax.yaxis.set_major_locator(plt.MultipleLocator(grain[2]))
        if grain[1]!= None:
            ax.xaxis.set_minor_locator(plt.MultipleLocator(grain[1]))
        if grain[3]!= None:
            ax.yaxis.set_minor_locator(plt.MultipleLocator(grain[3]))
        ax.grid(True,which='both')
    
    def plot(self,ax):
        ax.imshow(self.image, aspect='equal', origin='lower', extent = (0, self.dims[0], 0, self.dims[1]))
        ax.set_aspect('equal')
        ax.set(xticklabels=[])
        ax.set(yticklabels=[])
        ax.tick_params(left = False,bottom=False)
        self.grid(ax,grain=[1,None,1,None])

    def save(self,fig,**kwargs):
        cvars =         {
                        'bbox_inches'   : 'tight',
                        'pad_inches'    : 0,
                        'dpi'           : 400,
                        'savename'      : 'A.pdf',
                        'format'        : 'pdf',
                        }
        cvars.update(kwargs)
        savename = cvars['savename']
        imgformat = cvars['format']
        cvars.pop('savename')
        cvars.pop('format')
        fig.savefig(savename + f'.{imgformat}', **cvars)
    
    def speichern(self):
        self.save(self.figure,savename='bild',format='jpg')

# Hard-coded driver function to run the program
def main(): pass
    
# Executes the main function
if __name__ == '__main__':
    plt.close('all')
    
    pxim = pixelimage()
    pxim.set_colormap(one="black")
    w = pxim.todez("1001")
    h = pxim.todez("1011")
    imsize = (w,h)
    image_bin = '000000000000010000000011000000011100000010110000010010000010000001110000011110000001100000000000000'
    pxim.create_pixel_image(bimage=image_bin,imsize=imsize)
    pxim.initfig()
    
    pxim.plot(pxim.ax[0])

    # pxim.read_pixel_image('smiley.png')
    # pxim.save(pxim.fig, savename="test")