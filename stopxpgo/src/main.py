
from direct.stdpy import threading
from direct.stdpy.threading import current_thread
from panda3d.core import loadPrcFileData
# # loadPrcFileData("", "load-display p3tinydisplay")
# loadPrcFileData("", "load-display pandagles")
# loadPrcFileData("", "notify-level-egldisplay spam")
# loadPrcFileData("", "gl-debug true")
import sys
import random
import time

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

from direct.gui.OnscreenText import OnscreenText

from panda3d.core import *

from panda3d.bullet import *

# from panda3d.bullet import BulletWorld

from panda3d.direct import CMotionTrail
from panda3d.direct import CInterval

import simplepbr
import gltf
import physics
import stoplight
# import level
import vehicles
import random
import time
# import threading
loadPrcFileData("", """
            win-size 1680 1050
            window-title stopxgo
            show-frame-rate-meter #t
            framebuffer-multisample 1
            depth-bits 24
            color-bits 3
            alpha-bits 1
            multisamples 4
            view-frustum-cull 0
            textures-power-2 none
            hardware-animated-vertices #t
            gl-depth-zero-to-one true
            clock-frame-rate 60
            interpolate-frames 1
            cursor-hidden #t
            fullscreen #f
        """)
from panda3d.core import Thread
import direct.stdpy.threading

print(Thread.isThreadingSupported())
ROADUNITS1 = random.randint(100,300)
TIMEINTERVAL = random.randint(1, 10)
STREETLIGHTS = ROADUNITS1 // 2
ROADLENGTH = ROADUNITS1 * 20

print('road length:')
print(ROADLENGTH)

######TO-do figure out how to pass changing x into a function 
############fix boost so it addds to current acceleration
########random boost units?

##
#####camera should only move backwards on boost
#####
######Timer test




class Game(DirectObject):

  def __init__(self):

    super().__init__()
    gltf.patch_loader(loader)

    base.setBackgroundColor(0.1, 0.1, 0.8, 0.1)
    base.setFrameRateMeter(True)

    # base.cam.setPos(0, -20, 10)
    # base.cam.lookAt(0, 0, 10)
    self.worldNP = render.attachNewNode('World')
    # self.Vehicles = vehicles.Vehicles
    # self.worldNP = self.Vehicles.worldNP

    # # Light
    alight = AmbientLight('ambientLight')
    alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
    alightNP = render.attachNewNode(alight)


    dlight = DirectionalLight('directionalLight')
    dlight.setDirection(Vec3(1, 1, 0))

    dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
    dlightNP = render.attachNewNode(dlight)
    dlightNP.setPos(Vec3(0, 0, 4))
    # plight = PointLight('plight')
    # plnp = render.attachNewNode(plight)
    # plnp.setPos(0, 20, 7)
    self.worldNP.clearLight()
    render.clearLight()
    render.setLight(alightNP)
    # render.setLight(alightNP)
    # render.setLight(dlightNP)

    # # render.setLight(plnp)
    # self.worldNP.setLight(plnp)
    # self.worldNP.setLight(dlightNP)
    
    skybox = loader.loadModel("../models/NIGHTskydome")
    skybox.reparent_to(render)
    skybox.set_scale(2000)
    
    #shader
    self.scene_shader = Shader.load(Shader.SL_GLSL, "../shaders/simplepbr_vert_mod_1.vert", 
                                               "../shaders/simplepbr_frag_mod_1.frag")
    render.set_shader(self.scene_shader)
    render.set_antialias(AntialiasAttrib.MMultisample)
    # self.scene_shader = ShaderAttrib.make(self.scene_shader)
    # self.scene_shader = self.scene_shader.setFlag(ShaderAttrib.F_hardware_skinning, True)
    scene_filters = CommonFilters(base.win, base.cam)
    scene_filters.set_bloom()

    #keymap
    self.keyMap = {
                    "forward" : False,
                    "reverse" : False,
                    "turnleft" : False,
                    "turnright" : False,
                    "launchcar" : False,
                    "boost" : False}
    # Input
    self.accept('escape', self.doExit)
    self.accept('r', self.doReset)
    self.accept('f1', self.toggleWireframe)
    self.accept('f2', self.toggleTexture)
    self.accept('f3', self.toggleDebug)
    self.accept('f5', self.doScreenshot)
    #test changing variable
    # self.accept('t', self.testchange())
    
    self.accept("w", self.keyMap.__setitem__, ["forward", True])
    self.accept("w-up", self.keyMap.__setitem__, ["forward", False])
    self.accept("s", self.keyMap.__setitem__, ["reverse", True])
    self.accept("s-up", self.keyMap.__setitem__, ["reverse", False])
    # self.accept("t", self.keyMap.__setitem__, ["launchcar", True])
    inputState.watchWithModifiers('launch', 't')

    # inputState.watchWithModifiers('left', 'a')
    # inputState.watchWithModifiers('reverse', 's')
    # inputState.watchWithModifiers('right', 'd')
    # inputState.watchWithModifiers('turnLeft', 'q')
    # inputState.watchWithModifiers('turnRight', 'e')



    # Task
    taskMgr.add(self.update, 'updateWorld')
    


    #physics

    self.physics = physics.Physics()

    self.physics.setup()
    self.world = self.physics.world

    # setup

    # self.worldNP = self.physics.worldNP()
    # World
    self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
    self.debugNP.show()

######load VEHICLES and ENVIRONMENT
    self.stoplight = stoplight.Stoplight()
    self.loadcar()
    self.loadenv()
  
    self.enemyracers()
    self.setupcam()
    self.cameraNP.reparentTo(self.car)
   
    # self.level = level.Level()
    self.streetlights()
    # self.level.spawnroad()
    # self.loadstoplights()  
    self.spawnroad()
  
    self.roadunit()

#####controls the stoplights
    self.stoplighttimer(time = 2.0, pos = 0)
    # self.stoplighttimer(5.0, 1)
    # self.stoplighttimer(3.0, 1)
    # self.stoplighttimer2()
   
    # self.x = 0
    # self.stoplightcolors()
    # self.changecolor()
    
    
    
######lights1
    # self.stoplightcolors()
    # self.isgreen()
    # self.isyellow()
    # self.isred()

    # street.setH(90)

####COLLISION HANDLER
    #the traverser
    traverser = CollisionTraverser('carxstoplight')
    base.cTrav = traverser
   

    # handler for red light
    handlerred = CollisionHandlerEvent()
    handlerred.addInPattern('%fn-into-%in')

    #handler for yellowlight
    handleryellow = CollisionHandlerEvent()
    handleryellow.addInPattern('%fn-into-%in')
    handleryellow.addOutPattern('%fn-out-%in')
    
    # handler.addCollider()
    traverser.addCollider(self.chbnp, handlerred)
    traverser.addCollider(self.chbnp, handleryellow)
    # self.collHandEvent.addOutPattern('%fn-out-%in')

    # self.collCount = 0

    

    self.accept('car-into-stoplightyellow', self.boost)
    self.accept('car-into-stoplightred',  self.launchcar)

    # traverser.showCollisions(render)

  # def testchange(self):
  #   pass
  



  # _____HANDLER_____

  def doExit(self):
    self.cleanup()
    self.t1.cancel()
    self.t2.cancel()

    sys.exit(1)

  def doReset(self):
    self.cleanup()
    self.setup()

  def toggleWireframe(self):
    base.toggleWireframe()

  def toggleTexture(self):
    base.toggleTexture()

  def toggleDebug(self):
    if self.debugNP.isHidden():
      self.debugNP.show()
    else:
      self.debugNP.hide()

  def doScreenshot(self):
    base.screenshot('Bullet')

  # ____TASK___

  def processInput(self, dt):
    engineForce = 0.0
    brakeForce = 0.0

    # if inputState.isSet('forward'):
    if self.keyMap["forward"]:
      engineForce = 2500.0
      brakeForce = 0.0


    if self.keyMap["reverse"]:
      engineForce = 0
      brakeForce = 45.0
      # self.brakelight()
      # self.blight()

    self.vehicle.applyEngineForce(engineForce, 2);
    self.vehicle.applyEngineForce(engineForce, 3);
    self.vehicle.setBrake(brakeForce, 2);
    self.vehicle.setBrake(brakeForce, 3);

  def update(self, task):
    dt = globalClock.getDt()

    self.processInput(dt)
    self.world.doPhysics(dt, 10, 0.008)

    self.setupcam()
   
    self.blight()

    

    # self.stoplightcolors(0)
    # self.stoplightcolors(2)
    

    #print self.vehicle.getWheel(0).getRaycastInfo().isInContact()
    #print self.vehicle.getWheel(0).getRaycastInfo().getContactPointWs()

    #print self.vehicle.getChassis().isKinematic()


    return task.cont

  def cleanup(self):
    self.world = None
    self.worldNP.removeNode()
  
##########Create the level  
  def spawnroad(self):
    
    #Randomizes road length and loads stoplights


    self.road = [None] * ROADUNITS1
    self.stoplightarches = []
    self.hitboxes = []
    self.greenlights = []
    self.yellowlights = []
    self.redlights = []


#### this is to control each light individually
    self.GreenLightNP = []
    self.YellowLightNP = []
    self.RedLightNP = []

    self.roadnode = self.worldNP.attachNewNode('road')
    self.stoplightnode = self.worldNP.attachNewNode('stoplightnode')
    
    #####These nodes are for the stoplights so they can be switched out
    # self.GreenLightsNP = NodePath('greenlights')
    # self.YellowLightNP[0] = NodePath('yellowlights')
    # self.RedLightNP[0] = NodePath('redlights')


    self.roadnode.setShaderAuto()

    for x in range(ROADUNITS1):
      self.road[x] = loader.loadModel('../models/roadunit.glb')
      
      # self.road[x] = self.roadnode

      # self.road[x] = self.roadunit()

      if x == 0:
        self.road[x].reparentTo(self.roadnode)

      elif x in self.stoplight.stoplightpositions:
        #load stoplifght
        # 
########load stoplight units (archway and intersection)
        self.stoplightarches.append(loader.loadModel('../models/stoplightarch.glb'))
        # self.stoplight1 = Stoplight(loader.model(), interval_time, pos=x)
        # self.stoplight1.model.reparentTo()

        self.road[x] = loader.loadModel('../models/intersection.glb')

        self.stoplightarches[-1].reparentTo(self.road[x-1])
        self.road[x].reparentTo(self.road[x-1])

        self.road[x].setY(20)
        self.stoplightarches[-1].setY(20)

        self.stoplightarches[-1].wrtReparentTo(self.stoplightnode)
        self.road[x].wrtReparentTo(self.stoplightnode)


########hitboxes
        #####CHANGE STOPLIGHT HUITBOX NAME EVERYTIME IT ISAPPENDED
        self.hitboxes.append(self.stoplightnode.attachNewNode(CollisionNode(f'stoplighthitbox_{len(self.hitboxes)}')))

        self.hitboxes[-1].reparentTo(self.road[x-1])
        self.hitboxes[-1].setY(20)
        self.hitboxes[-1].node().addSolid(self.stoplight.hitboxy)
        
        # self.hitboxes[-1].show()


    

########Greenlights
        self.greenlights.append(loader.loadModel('../models/greenlight.glb'))
        

        self.greenlights[-1].reparentTo(self.road[x-1])
        self.greenlights[-1].setY(20) 

        self.GreenLightNP.append(NodePath('greenlight'))
  
########Yellowlights
        self.yellowlights.append(loader.loadModel('../models/yellowlight.glb'))

        self.yellowlights[-1].reparentTo(self.road[x-1])
        self.yellowlights[-1].setY(20) 

        self.YellowLightNP.append(NodePath('yellowlight'))

########Redlights
        self.redlights.append(loader.loadModel('../models/redlight.glb'))

        self.redlights[-1].reparentTo(self.road[x-1])
        self.redlights[-1].setY(20) 

        self.RedLightNP.append(NodePath('redlight'))
      


#########lights shouldnt be visible yet
        self.greenlights[-1].wrtReparentTo(self.GreenLightNP[-1])
        self.yellowlights[-1].wrtReparentTo(self.YellowLightNP[-1])
        self.redlights[-1].wrtReparentTo(self.RedLightNP[-1])




        # print("stoplight position test uwu")
        # print(x)
        # print(self.stoplightarches[-1].getY())
        # print(*self.stoplightarches)
        # self.GreenLightNP.ls() 
        # for i in self.GreenLightNP:
        #   print(self.GreenLightNP[i])

      


      else:
        self.road[x].reparentTo(self.road[x-1])

        self.road[x].setY(20)

        self.road[x].wrtReparentTo(self.worldNP)
    
    self.roadnode.flattenStrong()
    self.stoplightnode.flattenStrong()
  #   # self.roadnode.ls()
    # self.stoplightnode.ls()
    print(self.hitboxes)

  def roadunit(self):


######create collision geom for road

#####BOXSHAPE
    # (roadshape = BulletBoxShape(Vec3(20, ROADUNITS1 * 20, 0)))
    roadshape = BulletBoxShape(Vec3(20,  20, 0))
    self.roadnode.setCollideMask(BitMask32.allOn())
    self.roadNP = self.worldNP.attachNewNode(BulletRigidBodyNode('roadsh'))
    self.world.attachRigidBody(self.roadNP.node())
    
    # self.roadNP.node().addShape(roadshape)
    # self.roadNP.node().addShape(roadshape, TransformState.makePos(Point3(0, 20, 0)) )
    
    



    # self.roadNP.reparentTo(self.roadnode)
#########
    self.roadboxes = [None] * ROADUNITS1


    for x in range(ROADUNITS1):
      self.roadboxes[x] = self.roadNP
     
      if x == 0:
        self.roadNP.node().addShape(roadshape)



      else:
        self.roadboxes[x].node().addShape(roadshape, 
                                          TransformState.makePos(Point3(0, 20 * x, 0)) )


        # self.roadboxes[x].reparentTo(self.road[x-1])

        # self.roadboxes[x].setY(20)



  x = 0
  y = 0

  def change(self):
    #y#
    self.y += 1
    if self.y > 2:
      self.y = 0    

    #x#
    self.x += 1
    if self.x > 2:
      self.x = 0

  # print(x)
  # def change(self, var):
  #   return var + 1

#######TIMER THAT CONTROLS FIURST STOPLIGHT, FIND A WAY TO FIX
  def timer(self):
    pass
  def stoplighttimer(self, time, pos):
    def timerwithin():
      return self.stoplighttimer(time, pos)

#######
    self.firststoplightcolor = self.stoplight.colors[self.x]
    self.t1 = threading.Timer(time, timerwithin)
    self.t1.start()
    print('timertest uwu every 5 seconds')
    # self.change(x)
    self.change()
    self.stoplightcolors(pos)

######TIMER THAT CONTROLS THE SECON LIGHT ONLY FIND A WAY TO FIX
  # def stoplighttimer2(self, time, pos):
  #   def timerwithin():
  #     return self.stoplighttimer2(time, pos)


  #   self.secondstoplightcolor = self.stoplight.colors[self.y]
  #   self.t2 = threading.Timer(time, timerwithin)
  #   self.t2.start()
  #   # self.change(x)
  #   self.change()
    
  #   self.stoplightcolors2(pos)

      
  
  def stoplightcolors(self, x):
    # stoplightstates = self.stoplight.colors
    self.currentstate = self.stoplight.colors[self.x]
    self.currentstate2 = self.stoplight.colors[self.y]
    
 
    if self.currentstate == 'green':
      
      self.YellowLightNP[x].detachNode()
      self.RedLightNP[x].detachNode()
      self.GreenLightNP[x].reparentTo(self.stoplightnode)

      self.accept(f'car-into-stoplighthitbox_{x}',  self.isgreen)

    elif self.currentstate == 'yellow':
    #elif self.color == 'yellow', and :
      self.GreenLightNP[x].detachNode()
      self.RedLightNP[x].detachNode()
      self.YellowLightNP[x].reparentTo(self.stoplightnode)
      self.accept(f'car-into-stoplighthitbox_{x}',  self.boost)
    
    elif self.currentstate == 'red':
      self.YellowLightNP[x].detachNode()
      self.GreenLightNP[x].detachNode()
      self.RedLightNP[x].reparentTo(self.stoplightnode)
      self.accept(f'car-into-stoplighthitbox_{x}',  self.launchcar)
    
  # def stoplightcolors2(self, x):
  #   # stoplightstates = self.stoplight.colors
  #   self.currentstate = self.stoplight.colors[self.x]
  #   self.currentstate2 = self.stoplight.colors[self.y]
    
 
  #   if self.currentstate2 == 'green':
      
  #     self.YellowLightNP[x].detachNode()
  #     self.RedLightNP[x].detachNode()
  #     self.GreenLightNP[x].reparentTo(self.stoplightnode)

  #     self.accept('car-into-stoplighthitbox',  self.isgreen)



  #   elif self.currentstate2 == 'yellow':
  #   #elif self.color == 'yellow', and :
  #     self.GreenLightNP[x].detachNode()
  #     self.RedLightNP[x].detachNode()
  #     self.YellowLightNP[x].reparentTo(self.stoplightnode)
  #     self.accept('car-into-stoplighthitbox',  self.boost)
    
  #   elif self.currentstate2 == 'red':
  #     self.YellowLightNP[x].detachNode()
  #     self.GreenLightNP[x].detachNode()
  #     self.RedLightNP[x].reparentTo(self.stoplightnode)
  #     self.accept('car-into-stoplighthitbox',  self.launchcar)
    
    

    # if self.currentstate == 'green':
      
    #   self.GreenLightsNP.reparentTo(self.stoplightnode)

    # elif self.currentstate == 'yellow':
      
    #   self.YellowLightNP[0].reparentTo(self.stoplightnode)
    #   self.accept('car-into-stoplighthitbox',  self.boost)
    
    # elif self.currentstate == 'red':
      
    #   self.RedLightNP[0].reparentTo(self.stoplightnode)
    #   self.accept('car-into-stoplighthitbox',  self.launchcar)

    # if inputState.is_set('g'):
      
    #   self.GreenLightsNP.reparentTo(self.stoplightnode)

    # elif inputState.is_set('y'):
      
    #   self.YellowLightNP[0].reparentTo(self.stoplightnode)
    #   self.accept('car-into-stoplighthitbox',  self.boost)
    
    # elif inputState.is_set('r'):
      
    #   self.RedLightNP[0].reparentTo(self.stoplightnode)
    #   self.accept('car-into-stoplighthitbox',  self.launchcar)

#####THIS VARIABLE WILL BE USED TO CONTROL THE STOPLIGHT CHANGES


  











  def isyellow(self):
    # position2 = self.stoplightarch[2].getPos()
    
    self.YellowLightNP[0].reparentTo(self.stoplightnode)
    self.accept('car-into-stoplighthitbox',  self.boost)

  def isred(self):

    self.RedLightNP[0].reparentTo(self.stoplightnode)
    self.accept('car-into-stoplighthitbox',  self.launchcar)
    # self.redlight = loader.loadModel('../models/light.egg')
    # self.redlight.reparentTo(self.stoplightnode)
  

  def loadenv(self):
    pass



  def streetlights(self):
    ######loads streetlights and stoplights

    ######SPAWN STREETLIGHTS EVERY 4 ROADUNITS

    self.streetlightnode = self.worldNP.attachNewNode('streetlights')
    streetlights = loader.loadModel('../models/streetlamps.glb')
    streetlights.reparentTo(self.streetlightnode)
    self.streetlightnode.setY(20)
    
   ######### #light
    # streetlamp = PointLight('streetlamp')
    # streetlamp.setAttenuation(200)
    # streetlamp.setColor(Vec4(0.7, 0.4, 0.6, 1))
    
    # streetlampNP = self.worldNP.attachNewNode(streetlamp)
    # streetlampNP.setPos(Vec3(4,20,1))
    # streetlampNP.reparentTo(self.streetlightnode)

    # streetlampLNP = self.worldNP.attachNewNode(streetlamp)
    # streetlampLNP.setPos(Vec3(-10,0,10))
    # streetlampLNP.reparentTo(self.streetlightnode)

    # lamp = loader.loadModel('../models/lamp.egg')
    # lamp.reparentTo(streetlampNP)
    # self.worldNP.setLight(streetlampNP)
    # self.Vehiclenode.setLight(streetlampNP)
    # self.street.setLight(streetlampNP)
    # render.clearLight()
    # render.setLight(streetlampNP)

    # streetlight2 = self.worldNP.attachNewNode('streetlight2')
    # self.streetlightnode.copyTo(streetlight2)
    # streetlight2.reparentTo(self.street2)
#########
    self.streetlights = [None] * STREETLIGHTS





    # self.roadnode.setShaderAuto()

    for x in range(STREETLIGHTS):
      self.streetlights[x] = loader.loadModel('../models/streetlamps.glb')

      # self.road[x] = self.roadnode

      # self.road[x] = self.roadunit()

      if x == 0:
        self.streetlights[x].reparentTo(self.streetlightnode)
      
      # elif x in self.stoplight.stoplightpositions:
        
      #   self.streetlights[x] = loader.loadModel('../models/stoplightarch.glb')
      #   self.streetlights[x].reparentTo(self.streetlights[x-1])
      #   # self.streetlights[x].setY()

      else:
        self.streetlights[x].reparentTo(self.streetlights[x-1])

        self.streetlights[x].setY(40)


        # self.roadboxes[x].reparentTo(self.road[x-1])

        # self.roadboxes[x].setY(20)



  

  def loadcar(self):


    #car
    # self.car = loader.loadModel('../models/car3.egg')
    self.car = loader.loadModel('../models/gtier.glb')
    # carshader = Shader.load(Shader.SL_GLSL,
    #                         vertex="../shaders/carshader.vert",
    #                         fragment="../shaders/carshader.frag")
    # self.car.setShader(carshader)
    # self.car.setShaderAuto()
    self.car.setShader(self.scene_shader)
    
    # Chassis
    carshape = BulletBoxShape(Vec3(0.6, 1.4, 0.5))
    # cargeom = car.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
    # carshape = BulletConvexHullShape()
    # carshape.addGeom(cargeom)
    # car.reparentTo(self.worldNP)
    
    ts = TransformState.makePos(Point3(0, 0, 0.5))

    self.Vehiclenode = self.worldNP.attachNewNode(BulletRigidBodyNode('Vehicle'))
    self.Vehiclenode.node().addShape(carshape, ts)
    self.Vehiclenode.setPos(4, 3, 0)
    self.Vehiclenode.node().setMass(1000.0)
    self.Vehiclenode.node().setDeactivationEnabled(False)




    self.car.reparentTo(self.Vehiclenode)
    self.world.attachRigidBody(self.Vehiclenode.node())
    

    #np.node().setCcdSweptSphereRadius(1.0)
    #np.node().setCcdMotionThreshold(1e-7) 

    # Vehicle
    self.vehicle = BulletVehicle(self.world, self.Vehiclenode.node())
    self.vehicle.setCoordinateSystem(ZUp)
    
    self.world.attachVehicle(self.vehicle)



    #cars hitbox forred light
    self.chb = CollisionBox(Point3(1.1092, 2.1463, 0.09), Point3(-1, -2, 0.9))
    self.chbnp = self.Vehiclenode.attachNewNode(CollisionNode('car'))
    self.chbnp.node().addSolid(self.chb)
    self.chbnp.show()

######PRINT CARS SPEED
    #cars speed
    # self.speed = self.vehicle.getCurrentSpeedKmHour()

    # speedometer = TextNode('speedometer')
    # # carspeed = OnscreenText(text='Speed:' (self.speed), pos=(-0.5, 0.02), scale=0.07)
    # speedometer.setText(self.speed)
    # textnp = aspect2d.attachNewNode(speedometer)



    # Right front wheel
    np = loader.loadModel('../models/righttire.egg')
    np.reparentTo(self.worldNP)
    self.addWheel(Point3( 1.0,  1.05, 0.5), True, np)

    # Left front wheel
    np = loader.loadModel('../models/lefttire.egg')
    np.reparentTo(self.worldNP)
    self.addWheel(Point3(-1.0,  1.05, 0.5), True, np)

    # Right rear wheel
    np = loader.loadModel('../models/righttire.egg')
    np.reparentTo(self.worldNP)
    self.addWheel(Point3( 1.0, -1.05, 0.5), False, np)

    # Left rear wheel
    np = loader.loadModel('../models/lefttire.egg')
    np.reparentTo(self.worldNP)
    self.addWheel(Point3(-1.0, -1.05, 0.5), False, np)

    # Steering info
    self.steering = 0.0            # degree
    self.steeringClamp = 0.0      # degree
    self.steeringIncrement = 0.0 # degree per second

  def addWheel(self, pos, front, wheelnp):
    wheel = self.vehicle.createWheel()

    wheel.setNode(wheelnp.node())
    wheel.setChassisConnectionPointCs(pos)
    wheel.setFrontWheel(front)

    wheel.setWheelDirectionCs(Vec3(0, 0, -1))
    wheel.setWheelAxleCs(Vec3(1, 0, 0))
    wheel.setWheelRadius(0.25)
    wheel.setMaxSuspensionTravelCm(40.0)

    wheel.setSuspensionStiffness(40.0)
    wheel.setWheelsDampingRelaxation(2.3)
    wheel.setWheelsDampingCompression(4.4)
    wheel.setFrictionSlip(50.0);
    wheel.setRollInfluence(0.1)

  def enemyracers(self):
    shape = BulletBoxShape(Vec3(0.6, 1.4, 0.5))
    ts = TransformState.makePos(Point3(0, 0, 0.5))

    Chassisnode = self.worldNP.attachNewNode(BulletRigidBodyNode('enemyracer'))
    Chassisnode.node().addShape(shape, ts)
    Chassisnode.node().setMass(800.0)

    self.world.attachRigidBody(Chassisnode.node())

    loader.loadModel('../models/DMON.glb').reparentTo(Chassisnode)

    enemyvehicle = BulletVehicle(self.world, Chassisnode.node())
    enemyvehicle.setCoordinateSystem(ZUp)
    self.world.attachVehicle(enemyvehicle)
    


  def blight(self):
      self.tail = loader.loadModel('../models/brakelight tail')
      # brakelite = Material()
      # brakelite.setEmission((1, 0, 0, 0))
      # brakelite.setSpecular((1, 0, 0, 0))
      # self.tail.setMaterial(brakelite)
      
      self.tail.reparentTo(self.car)


      initpos = Vec3(0, 0, 0)
      braketail = LerpPosInterval(self.tail, 
                                  0.3, 
                                  Vec3(0, -11, 0), 
                                  Vec3(0, 0, 0))
      resetbrakelight = LerpPosInterval(self.tail, 
                                        0.3, 
                                        Vec3(0, 0, 0))                             
      if self.keyMap["reverse"]:

      
        growtail = Sequence(braketail)
        growtail.start()

      else: 
        self.tail.removeNode()
        # self.tail.reparentTo(self.worldNP)
        # resettail = Sequence(resetbrakelight)
        # resettail.start()
        

#####Stoplight events
  def isgreen(self, entry):
 
    pass
    # self.GreenLightsNP.reparentTo(self.stoplightnode)
    # self.greenlights[0].wrtReparentTo(self.worldNP)
    # self.greenlights[1].getPos

  def launchcar(self, entry):
  #launch car if it passes during red

    self.cameraNP.wrtReparentTo(self.worldNP)


    pFrom = Point3(0, 0, 0)
    pTo = Point3(2, 0, 10)
    pFrom = render.getRelativePoint(self.Vehiclenode, pFrom)
    pTo = render.getRelativePoint(self.Vehiclenode, pTo)

    v = pTo - pFrom
    v.normalize()
    v *= 50.0

    self.Vehiclenode.node().setLinearVelocity(v)  

    print(entry)

  def boost(self, entry):

    ####TO DO: use threading to load model so it doesnt lag initaiallalay






    motionlines = loader.loadModel('../models/motionlines.glb')
    # ml = render.attachNewNode("motionlines")
    # motionlines.reparentTo(ml)
    motionlines.reparentTo(self.Vehiclenode)
    motionlines.wrtReparentTo(self.worldNP)

    boost = 5000
    self.vehicle.applyEngineForce(boost, 2)
    self.vehicle.applyEngineForce(boost, 3)

    startpos = Vec3(0, -15, 4)
    maxpos = Vec3(0, -20, 4)
    
#####FIX THIS
    # camlerp = LerpPosInterval(self.cameraNP, 2, maxpos)
    # uncamlerp = LerpPosInterval(self.cameraNP, 1, startpos)

    # movecam = Sequence(camlerp)
    # movecam.start()
    # # if inputState.is_set('boost'):
    # #   
    # #   
    # # else:
    # resetcam = Sequence(uncamlerp)
    # resetcam.start()

    
    # force = Vec3(1, 0, 0)
    # force *= 100

    # boost = 2500
    # self.Vehiclenode.node().applyCentralForce(force)
    
    # pFrom = Point3(0, 0, 0)
    # pTo = Point3(0, 1, 0)
    # pFrom = render.getRelativePoint(self.Vehiclenode, pFrom)
    # pTo = render.getRelativePoint(self.Vehiclenode, pTo)

    # v = pTo - pFrom
    # v.normalize()
    # v *= 40.0

    # self.Vehiclenode.node().setLinearVelocity(v)  

    print(entry)
    


  def setupcam(self):
    base.disableMouse()
    self.cameraNP = base.cam
    # startpos = Vec3(0, -15, 4)
    # maxpos = Vec3(0, -20, 4)
    
    # camlerp = LerpPosInterval(self.cameraNP, 0.5, maxpos)
    # uncamlerp = LerpPosInterval(self.cameraNP, 0.7, startpos)
    # if self.keyMap['forward']:
    # # if self.accept(self.boost()):
    #   movecam = Sequence(camlerp)
    #   movecam.start()
    # else:
    #   resetcam = Sequence(uncamlerp)
    #   resetcam.start()

      

    base.cam.setPos(Vec3(0, -15, 4))
    base.cam.lookAt(Point3(0, 7, 3))

game = Game()
run()

