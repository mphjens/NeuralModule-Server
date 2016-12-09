import os
import Settings
from NeuralModules import ModuleLoader

loadedModules = {};

def isModuleLoaded(moduleName):
    return moduleName in loadedModules.keys()

def loadNeuralModule(moduleName):
    if not isModuleLoaded(moduleName):
        newModule = ModuleLoader.loadModule(os.path.join(os.getcwd(), Settings.MODULE_BASEPATH, moduleName + ".zip"))
        loadedModules[moduleName] = newModule
    else:
        print(moduleName + " was already loaded")

def predict(moduleName, imagePath):
    return loadedModules[moduleName].predict([imagePath])
