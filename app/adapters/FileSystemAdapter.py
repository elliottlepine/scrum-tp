from models.File import File

class FileSystemAdapter:
    instance = None

    @staticmethod
    def getInstance():
        if(FileSystemAdapter.instance == None):
            FileSystemAdapter.instance = FileSystemAdapter()
        
        return FileSystemAdapter.instance

    def open(self, path, read = True, write = False):
        authorization = ""

        if (read == True):
            authorization += "r"

        file = open(path, authorization)

        return File(file, read, write)