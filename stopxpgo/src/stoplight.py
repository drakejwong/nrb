from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase

from panda3d.core import TextNode, InputDevice, loadPrcFileData, Vec3

from panda3d.core import InputDeviceManager
from panda3d.core import *
from panda3d.bullet import *
from direct.gui.OnscreenText import OnscreenText

import physics

import random
import time


# class Stoplight(loader.model(), interval_time, pos):
class Stoplight():
    #stoplight node that gives boost on yellow and flings open on red

    def __init__(self):
       
########THE POSITUIONS OF EACH STOPLIGHT UNIT
        self.stoplightpositions = [6, 36, 60, 90, 127]    

########different states for each sotplight
        self.colors = ['green', 'yellow', 'red']
        # self.currentstate = self.colors[0]

        # time.sleep(5)

        # self.currentstate = self.colors[1]

        # time.sleep[5]

        # self.currentstate = self.colors[2]
    
    

        
    #create a hitbox for yellow and red lights


        self.hitboxy = CollisionBox(Point3(-10, 0, 0), Point3(10, 20, 10))
        self.hitboxr = CollisionBox(Point3(-10, 0, 0), Point3(10, 20, 10))
    

 
    def stoplighttimer(self):
        pass
        

    def Greenlight(self):
        pass


    def Yellowlight(self):
    #if car is in hitbox, it gets a speedboost



        self.lighty = loader.loadModel('../models/yellowlight.egg')
        self.lighty.reparentTo(self.stoplightmodel)
    
    
    def Redlight(self):
    #if car is in hitbox, it launches

        self.hitboxr = CollisionBox(Point3(-10, 0, 0), Point3(10, 20, 10))
        

        self.lights = loader.loadModel('../models/light.egg')
        self.lights.reparentTo(self.stoplightmodel)
        red = Material()
        red.setAmbient((0,1,0,1))
        red.setEmission((0,1,0,0))

        self.lights.setMaterial(red)


     