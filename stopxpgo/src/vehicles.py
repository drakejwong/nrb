import sys
from typing import Sequence
import direct.directbase.DirectStart
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import Sequence, Func, Wait

from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.IntervalGlobal import *

from panda3d.core import *
from panda3d.bullet import *

# from panda3d.bullet import BulletWorld

class Vehicles(DirectObject):

    def __init__(self):
    #   self.worldNP = render.attachNewNode('World')
        pass
    # def loadcar(self):
    #     self.car = loader.loadModel('../models/car3.egg')
    #     carshader = Shader.load(Shader.SL_GLSL,
    #                             vertex="../shaders/carshader.vert",
    #                             fragment="../shaders/carshader.frag")
    #     # self.car.setShader(carshader)
    #     self.car.setShaderAuto()


    #     # Chassis
    #     carshape = BulletBoxShape(Vec3(0.6, 1.4, 0.5))

