#### configTemplate V1.0

import configparser # handles config files

configParser = configparser.RawConfigParser()
configParser.read('folderConfig.txt')
configFolder = configParser.get('folderPaths', 'configFolder') # local config file path
resultsSavePath = configParser.get('folderPaths', 'resultsSavePath') # save path
screenshotsSavePath = configParser.get('folderPaths', 'screenshotsSavePath') # save path

idResponseArduino = configParser.get('usbPorts', 'idResponseArduino')
oscilloscopeID1 = configParser.get('usbPorts', 'idResponse1')
oscilloscopeID2 = configParser.get('usbPorts', 'idResponse2')
comPortScope1 = configParser.get('usbPorts', 'comPortScope1')
comPortScope2 = configParser.get('usbPorts', 'comPortScope2')

skipButton = configParser.get('localSettings', 'skipButton')
speedMin = configParser.get('localSettings', 'speedMin')
speedMax = configParser.get('localSettings', 'speedMax')

