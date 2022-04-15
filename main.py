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
        print("Incorrect password\n" + str(e))
        return getDecryptionKey(udid)
    key = key.getDecryptionKey()
    return key


def openNewDevice():
    devices = iOSbackup.getDeviceList()
    backText = "Back"
    deviceNames = [backText]
    for deviceData in devices:
        deviceNames.append(deviceData["name"])
    deviceMenu = Menu(deviceNames, title="Select a device")
    selected = deviceMenu.select()

    if selected == backText:
        return None

    # Convert device name to udid
    udid = None
    for deviceData in devices:
        if deviceData["name"] == selected:
            udid = deviceData["udid"]

    # Save UDID in json file using Yodas
    device = Yoda("devices/{0}.json".format(selected))
    content = device.contents()
    try:
        assert content["derivedkey"]
        assert content["udid"]
    except KeyError:
        key = getDecryptionKey(udid)
        content["udid"] = udid
        content["derivedkey"] = key
        device.write(content)


def main():
    # menuItems = [{"Quit": exit}, {"List devices": listDevices}]
    menuItems = [{"Quit": exit}, openNewDevice]
    mainMenu = Menu(menuItems, title="Main Menu")
    while True:
        mainMenu.select()


if __name__ == '__main__':
    main()
