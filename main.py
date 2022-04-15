from iOSbackup import iOSbackup
from yodas import Menu


def getDeviceList():
    devices = iOSbackup.getDeviceList()
    for device in devices:
        print(device)


def main():
    # menuItems = [{"Quit": exit}, {"List devices": listDevices}]
    menuItems = [{"Quit": exit}, getDeviceList]
    mainMenu = Menu(menuItems, title="Main Menu")
    while True:
        m = mainMenu.show()
        print(m())


if __name__ == '__main__':
    main()
