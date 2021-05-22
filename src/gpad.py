from direct.showbase.ShowBase import ShowBase

from panda3d.core import TextNode, InputDevice, loadPrcFileData, Vec3

from panda3d.core import InputDeviceManager

from direct.gui.OnscreenText import OnscreenText





class ControllerInput():




    
    def jls_extract_def(self):
        devices = self.devices.getDevices(InputDevice.DeviceClass.gamepad)

        if devices:

            self.connect(devices[0])
        return devices

    def __init__(self):
        
        self.gamepad = None
        devices = self.jls_extract_def()

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

            self.lblWarning.hide()
    

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