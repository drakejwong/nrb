
from pandac.PandaModules import loadPrcFileData
# loadPrcFileData('', 'load-display tinydisplay')

import sys
from typing import Sequence
import direct.directbase.DirectStart

from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.IntervalGlobal import *

from panda3d.core import *
from panda3d.bullet import *

# from panda3d.bullet import BulletWorld

from panda3d.direct import CMotionTrail
from panda3d.direct import CInterval

import physics
import stoplight

class Game(DirectObject):

  def __init__(self):
    base.setBackgroundColor(0.1, 0.1, 0.8, 1)
    base.setFrameRateMeter(True)

    # base.cam.setPos(0, -20, 10)
    # base.cam.lookAt(0, 0, 10)

    # # Light
    alight = AmbientLight('ambientLight')
    alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
    alightNP = render.attachNewNode(alight)

    dlight = DirectionalLight('directionalLight')
    dlight.setDirection(Vec3(1, 1, -1))
    dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
    dlightNP = render.attachNewNode(dlight)

    plight = PointLight('plight')
    plnp = render.attachNewNode(plight)
    plnp.setPos(0, 20, 7)

    render.clearLight()
    render.setLight(alightNP)
    # render.setLight(dlightNP)


    skybox = loader.loadModel("../models/NIGHTskydome")
    skybox.reparent_to(render)
    skybox.set_scale(2000)


    #keymap
    self.keyMap = {
                    "forward" : False,
                    "reverse" : False,
                    "turnleft" : False,
                    "turnright" : False}
    # Input
    self.accept('escape', self.doExit)
    self.accept('r', self.doReset)
    self.accept('f1', self.toggleWireframe)
    self.accept('f2', self.toggleTexture)
    self.accept('f3', self.toggleDebug)
    self.accept('f5', self.doScreenshot)
    self.accept('g', self.testhinge)
    
    self.accept("w", self.keyMap.__setitem__, ["forward", True])
    self.accept("w-up", self.keyMap.__setitem__, ["forward", False])
    self.accept("s", self.keyMap.__setitem__, ["reverse", True])
    self.accept("s-up", self.keyMap.__setitem__, ["reverse", False])
    inputState.watchWithModifiers('forward', 'w')
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

    self.worldNP = render.attachNewNode('World')
    # self.worldNP = self.physics.worldNP()
    # World
    self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
    self.debugNP.show()

    self.loadcar()
    self.loadenv()
    #cAMERa
    self.setupcam()
    self.cameraNP.reparentTo(self.car)

    # street.setH(90)

    # render.setLight(plnp)
    self.worldNP.setLight(plnp)
    self.worldNP.setLight(dlightNP)
    

  # _____HANDLER_____

  def doExit(self):
    self.cleanup()
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
    self.brakelight()
    self.blight()
    

    #print self.vehicle.getWheel(0).getRaycastInfo().isInContact()
    #print self.vehicle.getWheel(0).getRaycastInfo().getContactPointWs()

    #print self.vehicle.getChassis().isKinematic()

    return task.cont

  def cleanup(self):
    self.world = None
    self.worldNP.removeNode()

  def loadenv(self):

    #load environ
    self.street = loader.loadModel('../models/street.egg')
    streetgeom = self.street.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
    streetmesh = BulletTriangleMesh()
    streetmesh.addGeom(streetgeom)
    streetshape = BulletTriangleMeshShape(streetmesh, dynamic=False)


    self.street.setCollideMask(BitMask32.allOn())
    streetNP = self.worldNP.attachNewNode(BulletRigidBodyNode('Street'))
    streetNP.node().addShape(streetshape)
    self.world.attachRigidBody(streetNP.node())
    # streetNP.setH(-90)
    self.street.reparentTo(streetNP)

    #secondunit
    self.street2 = loader.loadModel('../models/street2.egg')
    self.street2.reparentTo(render)
    self.street2.setY(110)
    streetshape2 = BulletBoxShape(Vec3(13, 100, 0))
    streetNP2 = self.worldNP.attachNewNode(BulletRigidBodyNode('Street2'))
    self.world.attachRigidBody(streetNP2.node())
    streetNP2.node().addShape(streetshape2)
    streetNP2.setY(100)
    self.street2.reparentTo(self.street)



    self.stoplight = stoplight.Stoplight()
    self.stoplightnode = self.worldNP.attachNewNode(self.stoplight.stoplightunit)
    self.world.attachRigidBody(self.stoplightnode.node())
    
    self.stoplight.stoplightmodel.reparentTo(self.stoplightnode)
    self.stoplightnode.node().addShape(self.stoplight.stoplightshape)
    self.stoplightnode.setY(200)
    # self.stoplightnode.setZ(1)
    # self.stoplightnode.setY(10)
    # stoplightNP = self.worldNP.attachNewNode(BulletRigidBodyNode('Stoplight'))

    # hinge = BulletHingeConstraint(self.stoplightnode.node(), self.stoplight.pivotA, self.stoplight.axisA)
    # hinge.setLimit(-180, 90, softness=0.9, bias=0.3, relaxation=1.0)
    # self.world.attachConstraint(hinge)    

    pivotB = Point3(0, 0, 10)
    axisB = Vec3(0, 1, 0)
    # hinge = BulletHingeConstraint(self.stoplightnode, pivotB, axisB, True)
    # hinge.setDebugDrawSize(2.0)
    # hinge.setLimit(-180, 90, softness=0.9, bias=0.3, relaxation=1.0)
    # self.world.attachConstraint(hinge)



    self.barrier = loader.loadModel('../models/barrier.egg')
    self.barrier.reparentTo(render)



    # streetshader = Shader.load(Shader.SL_GLSL,
    #                         vertex="../shaders/streetshader.vert",
    #                         fragment="../shaders/streetshader.frag")
    # self.street.setShader(streetshader)  
    self.street.setShaderAuto()  


  def loadcar(self):


    #car
    self.car = loader.loadModel('../models/car4.egg')
    carshader = Shader.load(Shader.SL_GLSL,
                            vertex="../shaders/carshader.vert",
                            fragment="../shaders/carshader.frag")
    # self.car.setShader(carshader)
    self.car.setShaderAuto()

    # self.carlookat = self.car.attachNewNode(empty)

    
    # Chassis
    carshape = BulletBoxShape(Vec3(0.6, 1.4, 0.5))
    # cargeom = car.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
    # carshape = BulletConvexHullShape()
    # carshape.addGeom(cargeom)
    # car.reparentTo(self.worldNP)
    
    ts = TransformState.makePos(Point3(0, 0, 0.5))

    Vehiclenode = self.worldNP.attachNewNode(BulletRigidBodyNode('Vehicle'))
    Vehiclenode.node().addShape(carshape, ts)
    Vehiclenode.setPos(0, 0, 1)
    Vehiclenode.node().setMass(1000.0)
    Vehiclenode.node().setDeactivationEnabled(False)

    self.car.reparentTo(Vehiclenode)
    self.world.attachRigidBody(Vehiclenode.node())

    #np.node().setCcdSweptSphereRadius(1.0)
    #np.node().setCcdMotionThreshold(1e-7) 

    # Vehicle
    self.vehicle = BulletVehicle(self.world, Vehiclenode.node())
    self.vehicle.setCoordinateSystem(ZUp)
    
    self.world.attachVehicle(self.vehicle)
 



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
    self.steeringClamp = 45.0      # degree
    self.steeringIncrement = 120.0 # degree per second

  def addWheel(self, pos, front, np):
    wheel = self.vehicle.createWheel()

    wheel.setNode(np.node())
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

  def brakelight(self):
    #create motion trail from brakelight position 1 to brakelight position 1*Dt when released
    p1 = self.car.find("**/blpr")
    # dt = globalClock.getDt()
    # p2 = p1 * dt

    # braketrail = loader.loadModel('../models/braketrail.egg')
    # braketrail.reparentTo(render)
    # braketrail.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
   
    #create geom for brakelight
    format = GeomVertexFormat.get_v3n3c4t2()
    # format = GeomVertexFormat.get_v3c4()

    
    
    vdata = GeomVertexData('blgeom', format, Geom.UHDynamic)
    vdata.setNumRows(4) 
    
    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    texcoord = GeomVertexWriter(vdata, 'texcoord')
    
    vertex.addData3(1, 0, 1)
    normal.addData3(0, 0, 1)
    color.addData4(1, 0, 0.2, 0.5)
    texcoord.addData2(1, 0)

    vertex.addData3(1, 1, 1)
    normal.addData3(0, 0, 1)
    color.addData4(1, 0, 0.2, 0.5)
    texcoord.addData2(1, 1)

    vertex.addData3(0, 1, 1)
    normal.addData3(0, 0, 1)
    color.addData4(1, 0, 0.2, 0.5)
    texcoord.addData2(0, 1)

    vertex.addData3(0, 0, 1)
    normal.addData3(0, 0, 1)
    color.addData4(1, 0, 0.2, 0.5)
    texcoord.addData2(0, 0)


    prim = GeomTriangles(Geom.UHDynamic)
    prim.addVertices(0, 1, 2)
    # prim.addVertices(3, 4, 6)

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    brakegeom = GeomNode('brakelight')
    brakegeom.addGeom(geom)

    
    #
    # brakegeom.setPos(Vec3(0, 0, 2))

    # self.worldNP.attachNewNode(brakegeom)
    
    
    if self.keyMap["reverse"]:
      self.car.attachNewNode(brakegeom)
      brakegeom.addGeom(geom, RenderState.makeEmpty())
      brakelight = CMotionTrail()
      brakelight.addVertex(LVector4(1, 0, 0, 1), LVector4(0, 0, 0, 0), LVector4(0, 1), 0.1)
      brakelight.setGeomNode(brakegeom)
      brakelight.setParameters(0.1, 1, use_texture = False, calculate_relative_matrix = True, use_nurbs = False, resolution_distance = 1)
      
      # brakelight.updateMotionTrail()
      # brakelightNP = self.worldNP.attachNewNode(brakelight)

  def blight(self):
      self.tail = loader.loadModel('../models/brakelight tail')
      self.tail.reparentTo(self.car)
  
      initpos = Vec3(0, 0, 0)
      braketail = LerpPosInterval(self.tail, 
                                  0.3, 
                                  Vec3(0, -10, 0), 
                                  Vec3(0, 0, 0))
      if self.keyMap["reverse"]:

      
        growtail = Sequence(braketail)
        growtail.start()

      # else: 
      #   self.tail.removeNode()



  def testhinge(self):
    force = Vec3(0, 0, 0)
    force = render.getRelativeVector(self.stoplightnode, force)
    force.setY(10)
    self.stoplightnode.node().applyCentralForce(force)
    

  def motionlines(self):
    pass
  #load tunnel, reparent to car wrt

  def setupcam(self):
    base.disableMouse()
    self.cameraNP = base.cam
    startpos = Vec3(0, -15, 4)
    maxpos = Vec3(0, -20, 4)
    
    camlerp = LerpPosInterval(self.cameraNP, 0.5, maxpos)
    uncamlerp = LerpPosInterval(self.cameraNP, 0.7, startpos)
    if inputState.isSet('forward'):
      movecam = Sequence(camlerp)
      movecam.start()
    else:
      resetcam = Sequence(uncamlerp)
      resetcam.start()

      


    base.cam.lookAt(Point3(0, 7, 3))

game = Game()
run()

