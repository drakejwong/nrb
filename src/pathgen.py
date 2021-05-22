from panda3d.egg import EggData, EggVertexPool, EggVertex, EggGroup, EggLine , loadEggData , EggNurbsCurve
from panda3d.core import Point3D, NodePath

class createNurbsCurve():
    def __init__(self):
        self.data = EggData()
        self.vtxPool = EggVertexPool('mopath')
        self.data.addChild(self.vtxPool)
        self.eggGroup = EggGroup('group')
        self.data.addChild(self.eggGroup)
        self.myverts=[]
        self.myrotverts=[]
    
    def addPoint(self,pos,hpr=None):
        if hpr:
            eggVtx = EggVertex()
            eggVtx.setPos(Point3D(hpr[0],hpr[1],hpr[2]))
            self.myrotverts.append(eggVtx)
            self.vtxPool.addVertex(eggVtx)
        if self.myrotverts and not hpr:
            print ("you started to add rotations.. you better see it through now!")
         
        eggVtx = EggVertex()
        eggVtx.setPos(Point3D(pos[0],pos[1],pos[2]))
        self.myverts.append(eggVtx)
        self.vtxPool.addVertex(eggVtx)

    def getNodepath(self,order=3): 
        myCurve=EggNurbsCurve()
        myCurve.setup(order, len(self.myverts) +order)
        myCurve.setCurveType(1)
        for i in self.myverts:
            myCurve.addVertex(i)
        self.eggGroup.addChild(myCurve)
        
        if self.myrotverts:
            myCurve=EggNurbsCurve()
            myCurve.setup(order, len(self.myverts) +order)
            myCurve.setCurveType(2)
            for i in self.myrotverts:
                myCurve.addVertex(i)
            self.eggGroup.addChild(myCurve)
        
        out=NodePath(loadEggData(self.data))
        #self.data.writeEgg(Filename('test.egg'))
        return out

class createLine():
    def __init__(self):    
        self.data = EggData()
        self.vtxPool = EggVertexPool('line')
        self.data.addChild(self.vtxPool)
        self.eggGroup = EggGroup('group')
        self.data.addChild(self.eggGroup)
        self.myverts=[]
    
    def addPoint(self,pos): 
        eggVtx = EggVertex()
        eggVtx.setPos(Point3D(pos[0],pos[1],pos[2])) 
        self.myverts.append(eggVtx)
        self.vtxPool.addVertex(eggVtx)

    def getNodepath(self):
        for i in range(len(self.myverts)):
            if not i%500:
                if i:
                    myline.addVertex(self.myverts[i])
                # print i, len(self.myverts)
                myline=EggLine()
                self.eggGroup.addChild(myline)
            myline.addVertex(self.myverts[i])
        #self.data.writeEgg(Filename('test.egg'))
        return NodePath(loadEggData(self.data))


##testing
if __name__ == '__main__':
    from direct.directbase import DirectStart
    from math import sin,cos
    from direct.directutil.Mopath import Mopath
    from direct.interval.MopathInterval import *
    from panda3d.core import NodePath

    myCurve=createNurbsCurve()
    myLine = createLine()
    for i in range(100):
        myCurve.addPoint((cos(i/3.),i,sin(i/3.)))
        myLine.addPoint((cos(i/3.),i,sin(i/3.)) )
    lineNode = myLine.getNodepath()
    curveNode = myCurve.getNodepath()
    lineNode.reparentTo(render)

    myMopath = Mopath()
    myMopath.loadNodePath(curveNode)
    myMopath.fFaceForward = True
    myCube = loader.loadModel("yup-axis")
    myCube.reparentTo(render)
    myInterval = MopathInterval(myMopath, myCube, duration=10 ,name = "Name")
    myInterval.start()
    
    run()