#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create pixel image
"""
from infomodules.pixelimage import *
from ipywidgets import interactive,IntSlider, Text, Layout, Textarea
import matplotlib.pyplot as plt
from matplotlib.image import imread
import numpy as np

class interactivepixelimage(pixelimage):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_colormap(one="black")

        self.initbin = '10011100011111110111000111111000111111000111111101111110101011111000111111101111111101111111010111110111011011111110'

    def f(self, image_bin, bitlaenge):
        self.initfig()
        try:
            imsize = (self.todez(image_bin[:bitlaenge]),self.todez(image_bin[bitlaenge:2*bitlaenge]))
            self.create_pixel_image(bimage=image_bin[2*bitlaenge:],imsize=imsize)
            self.plot(self.ax[0])
        except:
            try:
                image = imread("nbmedia/spacecat.jpg")
                im = self.ax[0].imshow(image)
                self.ax[0].get_xaxis().set_visible(False)
                self.ax[0].get_yaxis().set_visible(False)
            except: pass