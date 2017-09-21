import win32api as w
import win32con as c
import sys

def load_device_list():
    """loads all Monitor which are plugged into the pc
    The list is needed to use setPrimary
    """
    workingDevices = []
    i = 0
    while True:
        try:
            Device = w.EnumDisplayDevices(None, i, 0)
#            Device.cb = sys.getsizeof(Device)
            if Device.StateFlags: #Attached to desktop
                workingDevices.append(Device)
                print('state: ', Device.StateFlags)

            i += 1
        except:
            return workingDevices


def setPrimary(id, workingDevices, MonitorPositions):
    """
    param id: index in the workingDevices list.
              Designates which display should be the new primary one

    param workingDevices: List of Monitors returned by load_device_list()

    param MonitorPositions: dictionary of form {id: (x_position, y_position)}
                            specifies the monitor positions

    """

    FlagForPrimary = c.CDS_SET_PRIMARY | c.CDS_UPDATEREGISTRY | c.CDS_NORESET
    FlagForSec = c.CDS_UPDATEREGISTRY | c.CDS_NORESET
    offset_X = - MonitorPositions[id][0]
    offset_X = - MonitorPositions[id][0]
    offset_Y = - MonitorPositions[id][1]
    numDevs = len(workingDevices)

    print("Num Devices: ", numDevs)

    import pywintypes
    # devmode = pywintypes.DEVMODEType()
    # devmode.Size = sys.getsizeof(devmode)

    #get devmodes, correct positions, and update registry
    for i in range(numDevs):

        devmode = w.EnumDisplaySettings(workingDevices[i].DeviceName, c.ENUM_CURRENT_SETTINGS)
        # devmode.Position_x = MonitorPositions[i][0] + offset_X
        # devmode.Position_y = MonitorPositions[i][1] + offset_Y
        if(w.ChangeDisplaySettingsEx(workingDevices[i].DeviceName, devmode, 
            FlagForSec if i != id else FlagForPrimary) \
            != c.DISP_CHANGE_SUCCESSFUL): return False

    #apply Registry updates once all settings are complete
    return w.ChangeDisplaySettingsEx() == c.DISP_CHANGE_SUCCESSFUL;


def setPrimary1(id, workingDevices, MonitorPositions):
    """
    param id: index in the workingDevices list.
              Designates which display should be the new primary one

    param workingDevices: List of Monitors returned by load_device_list()

    param MonitorPositions: dictionary of form {id: (x_position, y_position)}
                            specifies the monitor positions

    """

    FlagForPrimary = c.CDS_SET_PRIMARY | c.CDS_UPDATEREGISTRY | c.CDS_NORESET
    FlagForSec = c.CDS_UPDATEREGISTRY | c.CDS_NORESET
    offset_X = - MonitorPositions[id][0]
    offset_Y = - MonitorPositions[id][1]
    numDevs = len(workingDevices)

    print("Num Devices: ", numDevs)
    print("name__",workingDevices[0].DeviceName)

    #get devmodes, correct positions, and update registry
    devmode = w.EnumDisplaySettings(workingDevices[0].DeviceName, 167)
    if(w.ChangeDisplaySettingsEx(workingDevices[0].DeviceName, devmode, 
        FlagForPrimary) \
        != c.DISP_CHANGE_SUCCESSFUL): return False

    devmode = w.EnumDisplaySettings(workingDevices[1].DeviceName, 157)
    if(w.ChangeDisplaySettingsEx(workingDevices[1].DeviceName, devmode, 
        FlagForSec) \
        != c.DISP_CHANGE_SUCCESSFUL): return False
    #apply Registry updates once all settings are complete
    return w.ChangeDisplaySettingsEx() == c.DISP_CHANGE_SUCCESSFUL;

if(__name__ == "__main__"):
    print(w.EnumDisplaySettingsEx())

    devices = load_device_list()
    for dev in devices:
        print("Name:       ", dev.DeviceName)
        print("String:     ", dev.DeviceString)
        print("StateFlags: ", dev.StateFlags)
        print("DeviceID:   ", dev.DeviceID)
        print("DeviceKey:  ", dev.DeviceKey)
        print("\n")

    MonitorPositions = {
        0: (0, -1080),
        1: (0, 0),
        2: (1920, 0)
    }

    f = setPrimary(0, devices, MonitorPositions)
    print("Set primary: ", f)