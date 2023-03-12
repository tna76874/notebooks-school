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


class newturtle(customturtle):
    def __init__(self,*args,**kwargs):
        self.config =   {
                        'width'  : 400,
                        'height' : 250,
                        'canvas' : None,
                        'screen' : None,
                        }
        self.config.update(kwargs)
        
        if isinstance(self.config['canvas'],type(None)) & isinstance(self.config['screen'],type(None)):
            self.canvas = ipyturtle.Canvas(width=self.config['width'],height=self.config['height'])       
            display(self.canvas)
            self.screen=ipyturtle.TurtleScreen(self.canvas)
            self.screen.clear()
            self.screen.bgcolor("lightgreen")
            self.screen.delay(200)
        else:
            self.screen=self.config['screen']
       
        super().__init__(self.screen)

        self.shape("turtle")

    def route(self):
        runner = newturtle(screen=self.screen)
        self.screen.delay(2)
        runner.color('red')
        runner.speed(1000)
        runner.pendown()
        stepsize = 20
        increment = 10
        for i in range(5):
            runner.forward(stepsize)
            runner.left(90)
            stepsize += increment

    def introimage(self):   
        """
        letting turtle run introimage of skript
        from:
        https://github.com/williamnavaraj/ipyturtle3.git
        """
        colors = ['red', 'purple', 'blue', 'green', 'orange', 'yellow']
        self.shape("turtle")
        self.speed(1000)
        self.screen.bgcolor('white')
        self.screen.delay(1)
        for x in range(100):
            with(hold_canvas(self.canvas)):
                self.pencolor(colors[x%6])
                self.width(x//100 + 1)
                self.forward(x)
                self.left(59)

if __name__ == "__main__":
    turtle = newturtle()
    turtle.shape("turtle")
    turtle.speed(100)
    turtle.penup()
    turtle.goto(-100,-50)
    turtle.setheading(0)
    turtle.pendown()
    turtle.forward(200)
    turtle.left(90)
    turtle.forward(100)

    turtle2 = newturtle(screen=turtle.screen)
    turtle2.shape("turtle")
    turtle2.color('red')