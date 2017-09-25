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
                # print('state: ', Device.StateFlags)

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

        devmode = w.EnumDisplaySettings(workingDevices[i].DeviceName, c.ENUM_REGISTRY_SETTINGS)
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
    return w.ChangeDisplaySettingsEx()


def attachMonitor(dev):
    devmode = w.EnumDisplaySettings(dev.DeviceName, c.ENUM_REGISTRY_SETTINGS)
    devmode.Position_x = 1920
    devmode.Position_y = 0
    devmode.Fields = c.DM_POSITION
    res = w.ChangeDisplaySettingsEx(dev.DeviceName, devmode, c.CDS_UPDATEREGISTRY | c.CDS_NORESET)
    printMonitorsInfoByNId(dev)
    return w.ChangeDisplaySettingsEx(), res


def changePrimary(dev, devPri):
    devmode = w.EnumDisplaySettings(devPri.DeviceName, c.ENUM_REGISTRY_SETTINGS)
    # devmode.Position_x = 1920
    devmode.Position_x = 0
    devmode.Position_y = 0
    devmode.Fields = c.DM_POSITION
    res = w.ChangeDisplaySettingsEx(devPri.DeviceName, devmode, c.CDS_UPDATEREGISTRY | c.CDS_NORESET | c.CDS_SET_PRIMARY)
    deattachMonitor(dev)
    return w.ChangeDisplaySettingsEx(), res


def deattachMonitor(dev):

    devmode = w.EnumDisplaySettings(dev.DeviceName, c.ENUM_REGISTRY_SETTINGS)
    devmode.Position_x = 0
    devmode.Position_y = 0
    devmode.PelsHeight = 0
    devmode.PelsWidth = 0
    devmode.Fields = c.DM_POSITION | c.DM_PELSHEIGHT | c.DM_PELSWIDTH

    res = w.ChangeDisplaySettingsEx(dev.DeviceName, devmode, c.CDS_UPDATEREGISTRY | c.CDS_RESET)
    # return w.ChangeDisplaySettingsEx(), res
    return res


def printMonitorsInfo(workingDevices):

    for dev in workingDevices:
        name = "DeviceName: {:13s}".format(dev.DeviceName)
        dstr = " DeviceString: {:28s}".format(dev.DeviceString)
        stfl = " StateFlags: {:016X}".format(dev.StateFlags)
        dvid = " DeviceID: {:48s}".format(dev.DeviceID)

        devmode = w.EnumDisplaySettings(dev.DeviceName, c.ENUM_REGISTRY_SETTINGS)
        # PelsHeight = "PelsHeight: {:5d}".format(devmode.PelsHeight)
        # PelsWidth = " PelsWidth: {:5d}".format(devmode.PelsWidth)
        Resolution = " {1:5d} x{0:5d}".format(devmode.PelsHeight, devmode.PelsWidth)

        Fields = " Fields: {:016X}".format(devmode.Fields)
        Position_x = " Position_x: {:5d}".format(devmode.Position_x)
        Position_y = " Position_y: {:5d}".format(devmode.Position_y)
        print(name, stfl, dstr, Resolution, Position_x, Position_y, Fields)
        # print("String:     ", dev.DeviceString)
        # print("StateFlags: ", dev.StateFlags)
        # print("DeviceID:   ", dev.DeviceID)
        # print("DeviceKey:  ", dev.DeviceKey)
        # print("\n")


def printMonitorsInfoByNId(dev):

    name = "DeviceName: {:19s}".format(dev.DeviceName)
    dstr = " DeviceString: {:28s}".format(dev.DeviceString)
    stfl = " StateFlags: {:08X}".format(dev.StateFlags)
    dvid = " DeviceID: {:48s}".format(dev.DeviceID)

    devmode = w.EnumDisplaySettings(dev.DeviceName, c.ENUM_REGISTRY_SETTINGS)
    # PelsHeight = "PelsHeight: {:5d}".format(devmode.PelsHeight)
    # PelsWidth = " PelsWidth: {:5d}".format(devmode.PelsWidth)
    Resolution = " {1:5d} x{0:5d}".format(devmode.PelsHeight, devmode.PelsWidth)

    Fields = " Fields: {:08X}".format(devmode.Fields)
    Position_x = " Pos_x: {:5d}".format(devmode.Position_x)
    Position_y = " Pos_y: {:5d}".format(devmode.Position_y)
    # print(name, stfl, dstr, Resolution, Position_x, Position_y, Fields)
    # print("String:     ", dev.DeviceString)
    # print("StateFlags: ", dev.StateFlags)
    # print("DeviceID:   ", dev.DeviceID)
    # print("DeviceKey:  ", dev.DeviceKey)
    # print("\n")

    return str(name + stfl + dstr + Resolution + Position_x + Position_y + Fields)


def enableLG():

    devices = load_device_list()
    str_out = ''
    for dev in devices:
        str_out += printMonitorsInfoByNId(dev) + '\n'

    dev0 = devices[0]
    dev1 = _definePrimary()
    changePrimary(dev1, dev0)

    return str_out


def enableOneProjector():

    devices = load_device_list()

    dev = devices[1]
    res = attachMonitor(dev)
    print(attachMonitor(dev), dev.DeviceName)

    return res


def _definePrimary():

    devices = load_device_list()
    for dev in devices:
        if dev.StateFlags & c.DISPLAY_DEVICE_PRIMARY_DEVICE:
            return dev


if __name__ == "__main__":
    # print(w.EnumDisplaySettingsEx())

    # dev = definePrimary()
    # print(dev.StateFlags)

    # devices = load_device_list()
    # for dev in devices:
    #     printMonitorsInfoByNId(dev)

    # printMonitorsInfo(devices)

    # select monitor by name "\\.\DISPLAY4"
    # dev0 = devices[0]
    # dev1 = devices[5]
    # print(attachMonitor(dev1))
    # print(deattachMonitor(dev1))
    # print(changePrimary(dev0, dev1))
    # print(changePrimary(dev1, dev0))
    print(enableOneProjector())

    devices = load_device_list()
    str_out = ""
    for dev in devices:
        str_out += printMonitorsInfoByNId(dev) + '\n'
    # print(str_out)

    # MonitorPositions = {
    #     0: (0, -1080),
    #     1: (0, 0),
    #     2: (1920, 0)
    # }
    #
    # f = setPrimary(0, devices, MonitorPositions)
    # print("Set primary: ", f)