import os
from iOSbackup import iOSbackup
from yodas import Menu, Yoda


def getDecryptionKey(udid, clearPassword=None):
    if not clearPassword:
        clearPassword = input("Enter the encryption password for device\n{0}: ".format(udid))
    try:
        key = iOSbackup(udid=udid,
                        cleartextpassword=clearPassword)
    except Exception as e:
        # I know this exception is broad af, but it is what is raised when the password is incorrect
        print(str(e))
        return getDecryptionKey(udid)
    key = key.getDecryptionKey()
    return key


def selectDevice():
    devices = iOSbackup.getDeviceList()
    backText = "Back"
    deviceNames = [backText]
    for deviceData in devices:
        deviceNames.append(deviceData["name"])
    deviceMenu = Menu(deviceNames, title="Select a device")
    selected = deviceMenu.select()

    if selected == backText:
        return None
    return selected, devices


def openNewDevice():
    global deviceFolder, mainMenu
    deviceName, devices = selectDevice()

    # Convert device name to udid
    udid = None
    for deviceData in devices:
        if deviceData["name"] == deviceName:
            udid = deviceData["udid"]

    # Save UDID in json file using Yodas
    device = Yoda("{0}/{1}.json".format(deviceFolder, deviceName))
    content = device.contents()
    try:
        assert content["derivedkey"]
        assert content["udid"]
    except KeyError:
        key = getDecryptionKey(udid)
        content["udid"] = udid
        content["derivedkey"] = key
        device.write(content)
    mainMenu.add({deviceName: device})


def deviceMenu(yoda):
    """
    Takes yoda as input, opens menu to use the device
    :param yoda:
    :return none:
    """
    yodaFile = yoda.contents()
    device = iOSbackup(udid=yodaFile["udid"], derivedkey=yodaFile["derivedkey"])
    menu = Menu(["Back",
                 {"List Apps": listApps},
                 {"Restore Photos": restorePhotos}], title="Device options", execute=False)
    selected = menu.select()
    if selected == "Back":
        return None
    else:
        selected(device)


# Device functions
def listApps(device):
    apps = list(device.manifest['Applications'].keys())
    for app in apps:
        print(app)


def restorePhotos(device):
    global deviceFolder
    restoredDirectory = "restored"
    if deviceFolder[len(deviceFolder) - 1] == "/":
        restoredDirectory = deviceFolder + restoredDirectory
    else:
        restoredDirectory = deviceFolder + "/" + restoredDirectory
    print("Restoring to path: {0}".format(restoredDirectory))
    device.getFolderDecryptedCopy('Media',
                                  targetFolder=restoredDirectory,
                                  includeDomains='CameraRollDomain')


def main():
    global mainMenu
    while True:
        device = mainMenu.select()
        if isinstance(device, Yoda):
            deviceMenu(device)


if __name__ == '__main__':
    menuItems = [{"Quit": exit}, openNewDevice]
    mainMenu = Menu(menuItems, title="Main Menu")
    deviceFolder = "devices"
    main()
