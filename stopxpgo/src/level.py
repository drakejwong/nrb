
from panda3d.core import *

from panda3d.bullet import *

import random

import sys
from typing import Sequence
import direct.directbase.DirectStart
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import Sequence, Func, Wait

from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from direct.interval.LerpInterval import LerpPosInterval
from direct.filter.CommonFilters import CommonFilters
from direct.interval.IntervalGlobal import *
ROADUNITS1 = 150
STREETLIGHTS = ROADUNITS1 // 2
ROADLENGTH = ROADUNITS1 * 20

class Level(DirectObject):
    

        def spawnroad(self):
    
            #Randomizes road length
            self.road = [None] * ROADUNITS1
            self.roadnode = self.worldNP.attachNewNode('road')

            # self.roadnode.setShaderAuto()

            for x in range(ROADUNITS1):
              self.road[x] = loader.loadModel('../models/roadunit.glb')

              # self.road[x] = self.roadnode

              # self.road[x] = self.roadunit()

              if x == 0:
                self.road[x].reparentTo(self.roadnode)
              else:
                self.road[x].reparentTo(self.road[x-1])

                self.road[x].setY(20)

                self.road[x].wrtReparentTo(self.worldNP)

            self.roadnode.flattenStrong()
            # self.roadnode.ls()

  
  
