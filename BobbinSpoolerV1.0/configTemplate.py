#### configTemplate Bobin Spooler, Wire Encoder, Pressure sensors
import configparser # handles config files

configParser = configparser.RawConfigParser() # config
configFolder = 'folderConfig.txt'
configParser.read(configFolder)
idResponseSpooler = configParser.get('config', 'idResponseSpooler')
idResponseWireEncoder = configParser.get('config', 'idResponseWireEncoder')
macroPath = configParser.get('config', 'macroPath')

