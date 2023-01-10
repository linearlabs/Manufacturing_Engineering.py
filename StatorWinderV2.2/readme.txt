write python scripts with images called on with absolute paths (not saved in same folder as script) 
linux doesn't play nice with pyinstaller

cannot use ImageTk module with linux system, pyinstaller has issues with it, use built in tkinter image handling

in cmd / terminal: go to file path of python script

compile script with 'pyinstaller StatorWinderV2.2.py --onefile --noconsole'

icon.ico is broken on linux

copy and paste images, icons, modules, and config files into dist folder with the .exe file

keep these in dist folder

create new file on desktop and name it StatorWinderX.X.desktop

enter:

[Desktop Entry]
Type=Application
Encoding=UTF-8
Name=StatorWinder
Exec=/home/winder/Desktop/StatorWinderV2.2/dist/StatorWinderV2.2
Icon=/home/winder/Desktop/StatorWinderV2.2/dist/LLC-LOGO.gif
StartUpNotify=true
Terminal=false
