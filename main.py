import json
from iOSbackup import iOSbackup


# Everything to get the required credentials
def getKeys():
    keysPath = "user.json"
    keys = openJSON(keysPath)

    if keys == {}:
        keys = createKeys(keysPath)

    return keys


def createKeys(path):
    keyTypes = ["encryptionPassword",
                "decryptionKey"]
    keys = {}
    for keyType in keyTypes:
        print("\nPaste the {0} below".format(keyType))
        key = input("{}: ".format(keyType))
        keys[keyType] = key

    writeJSON(path, keys)
    print("New keys file created!")
    return keys


def openJSON(path):
    # Path should always contain the extension
    try:
        jsonFile = open(path)
        file = json.load(jsonFile)
        jsonFile.close()
        return file
    except FileNotFoundError:
        return {}


def writeJSON(path, data):
    assert type(data) is dict
    jsonFile = open(path, "w")
    json.dump(data, jsonFile)
    jsonFile.close()
    print("Saved to path: {}".format(path))


def main():
    getKeys()


if __name__ == '__main__':
    main()
