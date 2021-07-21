
from direct.showbase.DirectObject import DirectObject
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32
from panda3d.core import NodePath

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletTriangleMeshShape

from panda3d.core import *

#defines physics and loads some rigid bodies

class Physics(DirectObject):

  def __init__(self):


    
    self.world = BulletWorld()
    self.world.setGravity(Vec3(0, 0, -9.81))
  
  def cleanup(self):
    self.world.removeRigidBody(self.groundNP.node())
    self.world.removeRigidBody(self.carNP.node())
    self.world = None

    self.debugNP = None
    self.groundNP = None
    self.carNP = None

    # self.worldNP.removeNode()

  def setup(self):
    

    # World
    # self.debugNP = (BulletDebugNode('Debug'))
    # self.debugNP.show()
    # self.debugNP.node().showWireframe(True)
    # self.debugNP.node().showConstraints(True)
    # self.debugNP.node().showBoundingBoxes(False)
    # self.debugNP.node().showNormals(True)

    #self.debugNP.showTightBounds()
    #self.debugNP.showBounds()

    # self.world.setDebugNode(self.debugNP.node())
    
    # Soft body world self.information
    self.info = self.world.getWorldInfo()
    self.info.setAirDensity(0)
    self.info.setWaterDensity(0)
    self.info.setWaterOffset(0)
    self.info.setWaterNormal(Vec3(0, 0, 0))




    # Ground (static)
    # shape2 = BulletPlaneShape(Vec3(0, 0, 1), 1)

    # self.groundNP = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
    # self.groundNP.node().addShape(shape2)
    # self.groundNP.setPos(0, 0, -2)
    # self.groundNP.setCollideMask(BitMask32.allOn())

    # self.world.attachRigidBody(self.groundNP.node())

    def makecurve(p1):
      n = 8
      # p2 = p1 + Vec3(10, 0, 0)
      p2 = self.point1
      # self.info = self.physics.info

      brakelightNode = BulletSoftBodyNode.makeRope(p1, p2, n, 1 , 1) 
      brakelightNode.setTotalMass(5.0)
      brakelightNP = self.worldNP.attachNewNode(brakelightNode)
      self.world.attachSoftBody(brakelightNode)
    
      curve = NurbsCurveEvaluator()
      curve.reset(n + 2)
      brakelightNode.linkCurve(curve)
      brakelight = RopeNode('brakelight')
      brakelight.setCurve(curve)
      brakelight.setRenderMode(RopeNode.RMTube)
      brakelight.setUvMode(RopeNode.UVParametric)
      brakelight.setNumSubdiv(4)
      brakelight.setNumSlices(8)
      brakelight.setThickness(0.4)
      brakelightNP.setTexture(loader.loadTexture('../models/tex/rock.png'))
      return brakelightNP

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
    
    