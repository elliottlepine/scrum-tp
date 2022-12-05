import sys

class FileSystemAdapter:
    instance = None

    @staticmethod
    def getInstance():
        if(FileSystemAdapter.instance == None):
            FileSystemAdapter.instance = FileSystemAdapter()
        
        return FileSystemAdapter.instance

    def getArgv(self):
        return sys.argv