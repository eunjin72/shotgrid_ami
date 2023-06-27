# ShotGrid - Action Menu Items(AMIs)

<br/>

### Versions 페이지 업로드 된 Thumbnail(mp4)를 다운로드 하는 AMIs

![ami1](https://github.com/eunjin72/shotgrid_ami/assets/128131020/03efc735-0160-4d7f-9bf3-f478e3d6e849)


<br/>

## How to use AMIs - Using Custom Browser Protocols


### Registering a protocol on Windows

```
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\shotgrid]
"URL Protocol"=""

[HKEY_CLASSES_ROOT\shotgrid\shell]

[HKEY_CLASSES_ROOT\shotgrid\shell\open]

[HKEY_CLASSES_ROOT\shotgrid\shell\open\command]
@="python" "~\Shotgrid-AMIs\download_controller.py" "%1"
```

- **Info** - batch file 이용하여 cmd 확인

  **Registry Editor**
    ```
    [HKEY_CLASSES_ROOT\shotgrid\shell\open\command]
    @="C:\Windows\System32\cmd.exe" "/k" "{path}\test.bat" "%1"
    ```
  **test.bat**
    ```
    python ~\Shotgrid-AMIs\download_controller.py %1 pause
    ```
    
### Registering a protocol on Linux

```
$ cd ~/.local/share/applications
$ vim shotgrid.desktop

[Desktop Entry]
Name=shotgrid
Type=Application
Exec=python ~/Shotgrid-AMIs/download_controller.py %U
Terminal=true
MimeType=x-scheme-handler/shotgrid;

$ update-desktop-database ~/.local/share/applications/
```

<br/>

### Reference 
- https://developer.shotgridsoftware.com/af0c94ce/?title=Launching+Applications+Using+Custom+Browser+Protocols
- https://developer.shotgridsoftware.com/python-api/cookbook/examples/ami_handler.html
