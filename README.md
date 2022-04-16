# iOSBackupExtractor

This is a CLI interface partly to showcase the usage of the `yodas` package but mostly to access files in my phones backup such as photos.

This script can easily access all files like photos, voice memos, contacts, applications in any iOS backup folder, even if the backup is decrypted.

## Installation
```shell
$ git clone https://github.com/veryheavypickle/iOSBackupExtractor
$ cd iOSBackupExtractor
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Running
```shell
$ source venv/bin/activate
$ python main.py
```

## Usage
After running `main.py` you will be greeted with
```
====================
Main Menu
0 : Quit
1 : Open New Device

Choose an option: 
```

Enter `1` and you will be presented with

```
====================
Select a device
0 : Back
1 : Yodas Flip Phone

Choose an option: 
```

You may need to enter the password you used to encrypt the backup. This will take a small bit of time
```
====================
Main Menu
0 : Quit
1 : Open New Device
2 : Yodas Flip Phone

Choose an option: 
```

Opening your device, you will be presented with a list of options. In the future I will expand these options.
```
====================
Device options
0 : Back
1 : List Apps
2 : Restore Photos

Choose an option: 
```

Bear in mind that `Restore Photos` takes a very long time.
