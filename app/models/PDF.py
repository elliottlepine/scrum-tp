import File
import os
import SystemAdapter
class PDF(File):
   
    def getFileName(path : str) :
        getNameFromArgs = SystemAdapter.getInstance().getArgv()[1]
        
        return nameOfFile