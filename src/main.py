
#from pandac.PandaModules import loadPrcFileData
#loadPrcFileData('', 'load-display tinydisplay')

#loadPrcFileData('', 'bullet-additional-damping true')
#loadPrcFileData('', 'bullet-additional-damping-linear-factor 0.005')
#loadPrcFileData('', 'bullet-additional-damping-angular-factor 0.01')
#loadPrcFileData('', 'bullet-additional-damping-linear-threshold 0.01')
#loadPrcFileData('', 'bullet-additional-damping-angular-threshold 0.01')

import sys
import direct.directbase.DirectStart

from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.ShowBase import ShowBase

from direct.directutil import Mopath
from direct.interval.MopathInterval import *
from direct.interval.IntervalGlobal import *
from direct.interval.LerpInterval import LerpPosInterval
from direct.directdevices.DirectDeviceManager import DirectAnalogs, DirectButtons, DirectDeviceManager, DirectDials, DirectTimecodeReader, DirectTracker

from panda3d.egg import EggNurbsCurve

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import LMatrix4
from panda3d.core import TransformState
from panda3d.core import BitMask32
from panda3d.core import NodePath
from panda3d.core import InputDeviceManager, InputDevice
from panda3d.core import loadPrcFileData
from panda3d.core import *

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletBodyNode
from panda3d.bullet import BulletCharacterControllerNode

import physics
from gpad import ControllerInput
# from car import Carmoves

loadPrcFileData("", """
    default-fov 60
    notify-level-device debug
""")

    #variables for road
ROAD_SEGMENT_LENGTH = 320
ROAD_TIME = 3.97

base.destroy()

class Game(ShowBase):

  def __init__(self):

    ShowBase.__init__(self)
    self.setBackgroundColor(0.1, 0.1, 0.8, 1)
    self.setFrameRateMeter(True)




    # sys.path.insert(0, "../../")
    # sys.path.insert(0, "C:\Users\CJ\Documents\dev\Panda3D-1.10.7-x64\RenderPipeline-master")

    #     # Import the main render pipeline class
    # from rpcore import RenderPipeline

    #     # Construct and create the pipeline
    # self.render_pipeline = RenderPipeline()
    # self.render_pipeline.create(self)
    #cam setup
    # parentnode = render.attachNewNode('camparent')
    
    # parentnode.setEffect(CompassEffect.make(render)) # NOT inherit rotation
    # parentnode.reparentTo(carNP) # inherit transforms
    #     # the camera
    # self.camera.reparentTo(parentnode)
    # self.camera.lookAt(parentnode)
    # self.camera.setY(-10) # camera distance from model
   
    # self.cam.setPos(0, -20, 4)
    # self.cam.lookAt(0, 0, 0)
    
    

    #load skybox
    # self.skybox = loader.loadModel("../models/skybox")
    # self.skybox.setScale(100)
    # self.skybox.reparentTo(render)
    # self.skybox.setShaderOff()
    # self.skybox.setBin('background', 0)
    # self.skybox.setDepthWrite(0)
    # self.skybox.setLightOff()

    skybox = loader.loadModel("../models/NIGHTskydome")
    skybox.reparent_to(render)
    skybox.set_scale(2000)

    # skybox_texture = loader.loadTexture("../textures/nightsky.png")
    # skybox_texture.set_minfilter(SamplerState.FT_linear)
    # skybox_texture.set_magfilter(SamplerState.FT_linear)
    # skybox_texture.set_wrap_u(SamplerState.WM_repeat)
    # skybox_texture.set_wrap_v(SamplerState.WM_mirror)
    # skybox_texture.set_anisotropic_degree(16)
    # skybox.set_texture(skybox_texture)

    # skybox_shader = Shader.load(Shader.SL_GLSL, "skybox.vert.glsl", "skybox.frag.glsl")
    # skybox.set_shader(skybox_shader)


    # Light
    alight = AmbientLight('ambientLight')
    alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
    alightNP = render.attachNewNode(alight)

    dlight = DirectionalLight('directionalLight')
    dlight.setDirection(Vec3(1, 1, -1))
    dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
    dlightNP = render.attachNewNode(dlight)

    render.clearLight()
    render.setLight(alightNP)
    render.setLight(dlightNP)


    #world node for static objexcts/environment
    self.worldNP = render.attachNewNode('World') 
    #gamenode for dynamic objects also moves through environment
    self.gameNP = render.attachNewNode('Game')
    self.gameNP.setHpr(180, 0, 0)
    #fog
    # self.fogbox = loader.loadModel('../models/fogbox')
    # fogbox.reparentTo(self.worldNP)
    # acidfog = Fog("Acid Fog")
    # acidfog.setColor(0.5, 0.7, 0.5)
    # acidfog.setExpDensity(0.0009)
    # self.fogbox.setFog(acidfog)
    plight = PointLight('streetlight')
    plight.setColor((0.5, 0.2, 0.2, 1))
    plight.attenuation = (0, 0, 1)
    lightNP1 = self.gameNP.attachNewNode(plight)
    lightNP1.setPos(10, 0, 10)
    self.gameNP.setLight(lightNP1)

    # self.gameNP.setHpr(1, 1, 20)
    # self.gameNP.setPos(-32, 133, 1)
    
    #load environ model WORLDNP
    # self.track = loader.loadModel("../models/testtrack4.egg")
    # self.environ = loader.loadModel("../models/endlessroad.egg")
    # self.environ.setScale(10, 10, 10)
    # # self.environ.setPos(0, 0, 0)
    # self.environ.reparentTo(self.worldNP)



    


    # Physics
    self.physics = physics.BulletPhysics()
    self.physics.setup()
    self.world = self.physics.world
    # self.worldNP.attachNewNode(self.physics.debugNP())
    # self.Gamenode.physsetup()
    #self.world.setWorldTransform(LMatrix4(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    # Task
    taskMgr.add(self.update, 'updateWorld')

    #collisionshape for road
    
    # trackgeom = self.environ.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
    # mesh = BulletTriangleMesh()
    # mesh.addGeom(trackgeom)
    # tshape = BulletTriangleMeshShape(mesh, dynamic=False)
    
    # trackshape = BulletRigidBodyNode('Track')
    # tshapeNP = self.worldNP.attachNewNode(trackshape)
    # tshapeNP.node().addShape(tshape)
    # tshapeNP.node().setMass(0)
    #tshape.setScale(10, 10, 10)

    # self.world.attachRigidBody(tshapeNP.node())

    
    #ground box with collision (gameNP)

    self.roadshape = BulletBoxShape(Vec3(20, 2, 1))
    self.roadNP = self.gameNP.attachNewNode(BulletRigidBodyNode('road'))
    self.roadNP.node().addShape(self.roadshape)
    self.roadNP.setPos(0, 1, 0)
    self.roadNP.setCollideMask(BitMask32.allOn())

    self.world.attachRigidBody(self.roadNP.node())
    self.roadNP.reparentTo(self.gameNP)
    
    # self.roadUnit = loader.loadModel('../models/roadunit')
    
    # self.roadUnit.reparentTo(self.roadNP)

    shape2 = BulletPlaneShape(Vec3(0, 0, 1), 1)

    self.groundNP = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
    self.groundNP.node().addShape(shape2)
    self.groundNP.setPos(0, 0, -2)
    self.groundNP.setCollideMask(BitMask32.allOn())

    self.world.attachRigidBody(self.groundNP.node())



    # Keyboard input

    
    self.accept('escape', self.doExit)
    self.accept('r', self.doReset)
    self.accept('f1', self.toggleWireframe)
    self.accept('f2', self.toggleTexture)
    self.accept('f3', self.toggleDebug)
    self.accept('f5', self.doScreenshot)
    self.accept('space', self.doJump)

    inputState.watchWithModifiers('forward', 'w')
    inputState.watchWithModifiers('left', 'a')
    inputState.watchWithModifiers('reverse', 's')
    inputState.watchWithModifiers('right', 'd')
    inputState.watchWithModifiers('turnLeft', 'q')
    inputState.watchWithModifiers('turnRight', 'e')

    #Gamepad input

    # self.ControllerInput = ControllerInput()

    self.gamepad = None
    devices = self.devices.getDevices(InputDevice.DeviceClass.gamepad)

    if devices:
        self.connect(devices[0])


    
    self.accept("connect-device", self.connect)
    self.accept("disconnect-device", self.disconnect)

    self.accept("escape", exit)

    self.accept("gamepad-back", self.doExit)
    self.accept("gamepad-start", self.doExit)
    self.accept("gamepad-face_x", self.doReset)
    self.accept("gamepad-face_a", self.action, extraArgs=["face_a"])
    self.accept("gamepad-face_a-up", self.actionUp)
    self.accept("gamepad-face_b", self.action, extraArgs=["face_b"])
    self.accept("gamepad-face_b-up", self.actionUp)
    self.accept("gamepad-face_y", self.action, extraArgs=["face_y"])
    self.accept("gamepad-face_y-up", self.actionUp)


    # car (that we control) GAMENP
    car = loader.loadModel('../models/car2.egg')
    geom = car.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
    carshape = BulletConvexHullShape()
    carshape.addGeom(geom)



    # shape = BulletSphereShape(0.5)
    self.car = BulletCharacterControllerNode(carshape, 0.4)
    self.carNP = self.gameNP.attachNewNode(self.car)
    self.carNP.setPos(0, 0, 5)
    self.carNP.setHpr(90, 0, 0)
    self.carNP.reparentTo(self.gameNP)
    self.carNP.setCollideMask(BitMask32.allOn())
    self.world.attachCharacter(self.car)
    # self.carNP.setScale(2, 2, 1)
    # 
    # #self.carNP.node().setDeactivationEnabled(False)



    #car (model)
    
    car.setPos(0, 0, 0)
    car.setHpr(-90, 0, 0)
    car.clearModelNodes()
    car.reparentTo(self.carNP)

    

    

   

    self.spawnroads()
    self.movealongtrack()
    #BGM
    bgm = self.loader.loadSfx('../sounds/loop2.wav')
    bgm.setVolume(0.5)
    bgm.setLoop(True)
    bgm.play()

    #camerasetup
    self.setupcam()
    self.cameraNP.reparentTo(car)
  # _____HANDLER_____


  #gamepadconnect/disconnect
  def connect(self, device):
        """Event handler that is called when a device is discovered."""

        # We're only interested if this is a gamepad and we don't have a
        # gamepad yet.
        if device.device_class == InputDevice.DeviceClass.gamepad and not self.gamepad:
            print("Found %s" % (device))
            self.gamepad = device

            # Enable this device to ShowBase so that we can receive events.
            # We set up the events with a prefix of "gamepad-".
            self.attachInputDevice(device, prefix="gamepad")

            # Hide the warning that we have no devices.


  def disconnect(self, device):
        """Event handler that is called when a device is removed."""

        if self.gamepad != device:
            # We don't care since it's not our gamepad.
            return

        # Tell ShowBase that the device is no longer needed.
        print("Disconnected %s" % (device))
        self.detachInputDevice(device)
        self.gamepad = None

        # Do we have any other gamepads?  Attach the first other gamepad.
        devices = self.devices.getDevices(InputDevice.DeviceClass.gamepad)
        if devices:
            self.connect(devices[0])
        else:
            # No devices.  Show the warning.
            self.lblWarning.show()
  def action(self, button):
        # Just show which button has been pressed.
        self.lblAction.text = "Pressed \5%s\5" % button
        self.lblAction.show()

  def actionUp(self):
        # Hide the label showing which button is pressed.
        self.lblAction.hide()


  def setupcam(self):
    self.disableMouse()
    self.cameraNP = self.cam
    self.cam.setPos(0, -15, 6)
    self.cam.lookAt(self.carNP)

  def doExit(self):
    self.cleanup()
    sys.exit(1)

  def doReset(self):
    self.cleanup()
    self.setup()

  def toggleWireframe(self):
    self.toggleWireframe()

  def toggleTexture(self):
    self.toggleTexture()

  def toggleDebug(self):
    if self.debugNP.isHidden():
      self.debugNP.show()
    else:
      self.debugNP.hide()

  def doScreenshot(self):
    self.screenshot('Bullet')

  # ____TASK___

  def processInput(self, dt):
    speed = Vec3(0, 0, 0)
    omega = 0.0

    if inputState.isSet('forward'): speed.setX( 2.0)
    if inputState.isSet('reverse'): speed.setX(-2.0)
    if inputState.isSet('left'):    speed.setY(10)
    if inputState.isSet('right'):   speed.setY( -10)
    if inputState.isSet('turnLeft'):  omega =  120.0
    if inputState.isSet('turnRight'): omega = -120.0

    self.car.setAngularMovement(omega)
    self.car.setLinearMovement(speed, True)

    # force *= 30.0
    # torque *= 2.0

    # force = render.getRelativeVector(self.carNP, force)
    # torque = render.getRelativeVector(self.carNP, torque)

    # self.carNP.node().setActive(True)
    # self.carNP.node().setKinematic(True)
    # self.carNP.node().applyCentralForce(force)
    # self.carNP.node().applyTorque(torque)
    
  def doJump(self):
    self.car.setMaxJumpHeight(5.0)
    self.car.setJumpSpeed(10.0)
    self.car.doJump()


  
  def update(self, task):
    dt = globalClock.getDt()

    self.processInput(dt)
    #self.world.doPhysics(dt)
    self.world.doPhysics(dt, 5, 1.0/180.0)

    return task.cont
  
  def spawnroads(self):
    self.road = [None] * 4
    
    for x in range(4):
      #Load roads
      self.road[x] = loader.loadModel('../models/endlessroad.egg')

      #only first road visible
      if x == 0:
        self.road[x].reparentTo(self.worldNP)
      else: 
        self.road[x].reparentTo(self.road[x-1])

      self.road[x].setPos(0, -ROAD_SEGMENT_LENGTH, 0)



  def movealongtrack(self):


    self.road = self.road[1:] + self.road[0:1]

    self.road[0].setY(0)
    self.road[0].reparentTo(self.worldNP)
    self.road[0].setScale(1, 1, 1)
    self.road[3].reparentTo(self.road[2])
    self.road[3].setY(-ROAD_SEGMENT_LENGTH)

    self.move = Sequence(
      LerpFunc(self.road[0].setY,
                duration=ROAD_TIME,
                fromData=0,
                toData=ROAD_SEGMENT_LENGTH),
      Func(self.movealongtrack)
    )


    
    self.move.start()

    # duration = 10
    # pos = Point3(0, -500,0)
    
    # trackInterval = LerpPosInterval(self.worldNP,
    #                 duration,
    #                 pos,
    #                 other = None,
    #                 blendType='noBlend',
    #                 bakeInStart=1,
    #                 fluid=0,
    #                 name='trackInterval')
    # self.trackpath = Sequence(trackInterval)
    # self.trackpath.start()
    
    # i1 = gameNP.posInterval(1.0, Point3(20, 1, 1) )

    
    


  # def movebox(self, dt):

    
    
    



  # def cleanup(self):
  #   self.world.removeRigidBody(self.groundNP.node())
  #   self.world.removeRigidBody(self.carNP.node())
  #   self.world = None

  #   self.debugNP = None
  #   self.groundNP = None
  #   self.carNP = None

  #   self.worldNP.removeNode()

  # def setup(self):
    

  #   # World
  #   self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
  #   self.debugNP.show()
  #   self.debugNP.node().showWireframe(True)
  #   self.debugNP.node().showConstraints(True)
  #   self.debugNP.node().showBoundingBoxes(False)
  #   self.debugNP.node().showNormals(True)

  #   #self.debugNP.showTightBounds()
  #   #self.debugNP.showBounds()

  #   self.world = BulletWorld()
  #   self.world.setGravity(Vec3(0, 0, -9.81))
  #   self.world.setDebugNode(self.debugNP.node())
    
    




  #   # Ground (static)
  #   shape2 = BulletPlaneShape(Vec3(0, 0, 1), 1)

  #   self.groundNP = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
  #   self.groundNP.node().addShape(shape2)
  #   self.groundNP.setPos(0, 0, -2)
  #   self.groundNP.setCollideMask(BitMask32.allOn())

  #   self.world.attachRigidBody(self.groundNP.node())




 
    # self.parentnode.reparentTo(carNP) # inherit transforms


    # Bullet nodes should survive a flatten operation!
    #self.worldNP.flattenStrong()
    #render.ls()

game = Game()
game.run()


