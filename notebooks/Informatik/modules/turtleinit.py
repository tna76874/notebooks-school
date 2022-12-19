#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
turtle modules
-- init a turtle on a canvas
"""
import ipyturtle3 as ipyturtle
from ipyturtle3 import hold_canvas
import numpy as np
import time
import random

class customturtle(ipyturtle.Turtle):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def gox(self,steps):
        self.goto(self.position()[0]+steps,self.position()[1])

    def goy(self,steps):
        self.goto(self.position()[0],self.position()[1]+steps)
    
    def godown(self,steps):
        self.goy(-steps)

    def goup(self,steps):
        self.goy(steps)

    def goleft(self,steps):
        self.gox(-steps)
        
    def goright(self,steps):
        self.gox(steps)
    
    def goxy(self,x,y):
        x,y = list(np.array(self.position()) + np.array([x,y]))
        self.goto(x,y)
    
    def diagonal(self,angle,steps):
        """
        Walking a diagonal without rotating the turtle.
        """
        angle = angle/180*np.pi
        x,y = list(np.array(self.position()) + np.array([np.cos(angle)*steps, np.sin(angle)*steps]))
        self.goto(x,y)        


def newturtle(width=400,height=250):
    # Hier legen wir fest wie der Hintergrund aussieht
    myCanvas=ipyturtle.Canvas(width=width,height=height)
    display(myCanvas)
    myTS=ipyturtle.TurtleScreen(myCanvas)
    myTS.clear()
    myTS.bgcolor("lightgreen")

    # Schildi die Schildkröte wird erschaffen
    turtle=customturtle(myTS)

    myTS.delay(200)
    return turtle
