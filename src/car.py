from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletSphericalConstraint
from panda3d.bullet import BulletConvexHullShape


class Carmoves():
 
 

   
   def __init__(self):
          
      car = loader.loadModel('../models/car2.egg')
      geom = car.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
      carshape = BulletConvexHullShape()
      carshape.addGeom(geom)
      
   # def doJump(self):
   #    self.car.setMaxJumpHeight(5.0)
   #    self.car.setJumpSpeed(8.0)
   #    self.car.doJump()

   def evade(self):
      #if car is in hitbox of obstacle, it can evade away

      

   # def altcar():
   #    car = loader.loadModel('../models/car2.egg')
   #    car.setScale(0.5, 0.5, 0.5)
   #    car.clearModelNodes()
   #    car.reparentTo(self.carNP)


   #    chasisshape = BulletBoxShape(Vec3(0.5, 1, 0.5))
   #    wheelshape = BulletSphereShape(0.125)