from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase

from panda3d.core import TextNode, InputDevice, loadPrcFileData, Vec3

from panda3d.core import InputDeviceManager
from panda3d.core import *

from panda3d.bullet import *
from direct.gui.OnscreenText import OnscreenText

import physics



class Stoplight(DirectObject):
    #stoplight node that gives boost on yellow and flings open on red

    def __init__(self):
       
        self.physics = physics.Physics()
        self.physics.setup()
        self.world = self.physics.world


        self.stoplightunit = BulletRigidBodyNode('Stoplight')
        self.stoplightmodel = loader.loadModel('../models/stoplight.egg')
        self.stoplightshape = BulletBoxShape(Vec3(13, 10, 0))
        
        #point and axis for hinge
        self.pivotA = Point3(7, 0, 0)
        self.axisA = Vec3(0, 1, 0)
        # self.pivotA = TransformState.makePosHpr(Point3(7, 0, 0), Vec3(0, 10, 0))
        # self.stoplightmodel.reparentTo(self.stoplightunit)
        # self.stoplightunit.node().addShape(self.stoplightshape)


        # self.blockade = loader.loadModel('../models/blockade.egg')
        

    def Greenlight(self):
        pass


    def Yellowlight(self):


        pass
    
    
    def Redlight(self):
    #use hiinge to do reverse trapdoor, box to push car into hole
        
        pass   