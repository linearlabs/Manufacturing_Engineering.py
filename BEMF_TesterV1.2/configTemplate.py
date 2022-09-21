#### configTemplate V1.0

import configparser # handles config files

configParser = configparser.RawConfigParser()
configParser.read('folderConfig.txt')
configFolder = configParser.get('folderPath', 'configFolder') # local config file path
resultsSavePath = configParser.get('folderPath', 'resultsSavePath') # save path
screenshotsSavePath = configParser.get('folderPath', 'screenshotsSavePath') # save path

idResponseArduino = configParser.get('folderPath', 'idResponseArduino')
oscilloscopeID1 = configParser.get('folderPath', 'idResponse1')
oscilloscopeID2 = configParser.get('folderPath', 'idResponse2')
comPortScope1 = configParser.get('folderPath', 'comPortScope1')
comPortScope2 = configParser.get('folderPath', 'comPortScope2')

skipButton = configParser.get('folderPath', 'skipButton')

