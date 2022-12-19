#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
turtle modules
-- init a turtle on a canvas
"""
import ipyturtle3 as ipyturtle
from ipyturtle3 import hold_canvas
import time
import random

def newturtle(width=400,height=250):
    # Hier legen wir fest wie der Hintergrund aussieht
    myCanvas=ipyturtle.Canvas(width=width,height=height)
    display(myCanvas)
    myTS=ipyturtle.TurtleScreen(myCanvas)
    myTS.clear()
    myTS.bgcolor("lightgreen")

    # Schildi die Schildkröte wird erschaffen
    turtle=ipyturtle.Turtle(myTS)

    myTS.delay(200)
    return turtle
