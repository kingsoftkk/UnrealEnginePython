import sys
import unreal_engine as ue
import json
import upycmd as cmd
from os import listdir

from upypip import pip

def checkPipDirectory():
	#get our python scripts path
	configPath = cmd.PythonPluginScriptPath() + '/upyconfig.json'
	correctPipPath = cmd.PythonHomeScriptsPath()

	#compare our current pip directory with the installed one, if they differ reinstall pip
	try:
		with open(configPath, "r+") as configFile:
			configs = json.load(configFile)

			#grab currently stored path
			storedPipPath = configs['pipDirectoryPath']

			print('upystartup::Checking pip location on startup')
			print('upystartup::stored loc: ' + storedPipPath)
			print('upystartup::correct loc: ' + correctPipPath)

			#compare paths
			if (storedPipPath != correctPipPath):
				#if they don't match, remove the pip module and reinstall pip for this module
				print('upystartup::Pip installation directory is stale, re-installing.')

				libPath = cmd.PythonHomePath() + '/Lib/site-packages'
				dirs = listdir(libPath)

				tempPath = None
				#find the directory that contains pip and ends with .dist-info
				for directory in dirs:
					#print(directory)
					if (directory.startswith('pip') and
						directory.endswith('.dist-info')):
						tempPath = libPath + "/" + directory
						break

				if(tempPath != None):
					#remove the old directory
					print('removing old: ' + tempPath)
					cmd.run('rmdir /S /Q "' + tempPath + '"')
				
				#install pip
				print(cmd.PythonHomePath() + '/get-pip.py')

				print('Installing pip...')
				cmd.runLogOutput('InstallPip.bat')

				#update our stored location
				configs['pipDirectoryPath'] = correctPipPath
				configFile.seek(0)
				configFile.write(json.dumps(configs))
				configFile.truncate()

				#done
				print('upystartup::updated pip.exe location in <' + configPath + '>')

			else:
				print('upystartup::pip location is up to date.')

	except:
		e = sys.exc_info()
		ue.log('upyconfig.json error: ' + str(e))

#add any startup action you wish to perform in python
def startup():
	#check that our pip directory matches for pip.exe commands
	checkPipDirectory()
