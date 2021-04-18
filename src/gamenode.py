
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

#gamenode includes allvehicles and dynamic objectz that move along track geometry

class Gamenode():

    def __init__(self):
        

        self.roadshape = BulletBoxShape(Vec3(10, 10, 1))
        
        

    def setup(self):

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(self.debugNP.node())

