to save images to .exe files:

write python scripts with images called on with non absolute paths (saved in same folder as script

in cmd: go to file path of python script

compile script with 'pyinstaller ControllerTesterV1.1.py --onefile --noconsole --icon=icon.ico'

'ControllerTesterVx.x.py' and icon.ico are variable depending on what you want to choose

then copy and paste images, icons, modules, and config files into dist folder with the .exe file

keep these in dist folder  (can stop here but use a short cut for .exe)

create Installer

run Inno Setup Compiler

check create new script file using script wizzard > ok

click next (do not check create a new empty script file)

Enter Name, version, co., website > click next    (https://linearlabsinc.com/)

click next (no changes made on application folder window)

browse > select .exe file created with pyinstaller > check allow user to start application

add files > add any icons or pictures that are associated with .exe > click next

uncheck associate a file type > click next

click next > click next

check ask the user to choose install mode > click next

english > click next

Change compiler output folder to origional pyinstaller folder > change compiler output base name (include 'installer' in name) > choose custom setup icon file > click next

click next

click yes (compile now)

click no (don't save script)

done!