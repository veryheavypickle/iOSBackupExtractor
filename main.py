from iOSbackup import iOSbackup
from yodas import Menu, Yoda


def getDecryptionKey(udid, clearPassword=None):
    encrypted = False
    devices = iOSbackup.getDeviceList()
    name = udid
    for device in devices:
        if device["udid"] == udid:
            encrypted = device["encrypted"]
            name = device["name"]
    if not clearPassword and encrypted:
        clearPassword = input("Enter the encryption password for device {0}\nThis will take a minute: ".format(name))
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
    menu = Menu(deviceNames, title="Select a device")
    selected = menu.select()

    if selected == backText:
        return None, None
    return selected, devices


def openNewDevice():
    global deviceFolder, mainMenu
    deviceName, devices = selectDevice()

    if deviceName is None:
        return None
    elif devices is None:
        return None

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
        assert content["name"]
    except KeyError:
        key = getDecryptionKey(udid)
        content["udid"] = udid
        content["derivedkey"] = key
        content["name"] = deviceName
        device.write(content)
    mainMenu.append({deviceName: device})


def deviceMenu(yoda):
    """
    Takes yoda as input, opens menu to use the device
    :param yoda:
    :return none:
    """
    yodaFile = yoda.contents()
    device = iOSbackup(udid=yodaFile["udid"], derivedkey=yodaFile["derivedkey"])
    menu = Menu(["Back", listApps, restorePhotos, closeDevice], title="Device options", execute=False)
    selected = menu.select()
    if selected == "Back":
        return None
    else:
        selected(device, yoda)


# Device functions
def listApps(device, yoda):
    assert isinstance(device, iOSbackup)
    assert isinstance(yoda, Yoda)
    apps = list(device.manifest['Applications'].keys())
    for app in apps:
        print(app)


def restorePhotos(device, yoda):
    assert isinstance(device, iOSbackup)
    assert isinstance(yoda, Yoda)
    global deviceFolder
    restoredDirectory = yoda.contents()["name"]
    if deviceFolder[len(deviceFolder) - 1] == "/":
        restoredDirectory = deviceFolder + restoredDirectory
    else:
        restoredDirectory = deviceFolder + "/" + restoredDirectory
    print("Restoring to path: {0}".format(restoredDirectory))
    print("Warning, this will take some time")
    device.getFolderDecryptedCopy('Media',
                                  targetFolder=restoredDirectory,
                                  includeDomains='CameraRollDomain')
    print("Restoring completed!")


def closeDevice(device, yoda):
    assert isinstance(device, iOSbackup)
    assert isinstance(yoda, Yoda)
    yoda.delete()


def main():
    global mainMenu
    while True:
        device = mainMenu.select()
        if isinstance(device, Yoda):
            deviceMenu(device)


if __name__ == '__main__':
    mainMenu = Menu([exit, openNewDevice], title="Main Menu")
    deviceFolder = "devices"
    main()
