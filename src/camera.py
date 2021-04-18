from panda3d.core import DriveInterface
from panda3d import globalClock

class camera():

    def __init__(self):
    
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)



        # dummy node for camera, we will rotate the dummy node fro camera rotation
        parentnode = render.attachNewNode('camparent')
        parentnode.reparentTo(model) # inherit transforms
        parentnode.setEffect(CompassEffect.make(render)) # NOT inherit rotation

        # the camera
        base.camera.reparentTo(parentnode)
        base.camera.lookAt(parentnode)
        base.camera.setY(-10) # camera distance from model

        # camera zooming
        base.accept('wheel_up', lambda : base.camera.setY(base.camera.getY()+200 * globalClock.getDt()))
        base.accept('wheel_down', lambda : base.camera.setY(base.camera.getY()-200 * globalClock.getDt()))


        # global vars for camera rotation
        heading = 0
        pitch = 0



    def thirdPersonCameraTask(task):
        global heading
        global pitch
        
        md = base.win.getPointer(0)
            
        x = md.getX()
        y = md.getY()
        
        if base.win.movePointer(0, 300, 300):
            heading = heading - (x - 300) * 0.5
            pitch = pitch - (y - 300) * 0.5
        
        parentnode.setHpr(heading, pitch,0)
        
        return task.cont

        taskMgr.add(thirdPersonCameraTask, 'thirdPersonCameraTask')   