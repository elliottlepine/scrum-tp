import os

class FileSystemAdapter:
    instance = None

    @staticmethod
    def getInstance():
        if(FileSystemAdapter.instance == None):
            FileSystemAdapter.instance = FileSystemAdapter()
        
        return FileSystemAdapter.instance

    def create(self, file: File):
        with open(file.path, 'w') as f:
            f.write(file.content)

    def read(self, path, read = True, write = False):
        authorization = ""

        if (read == True):
            authorization += "r"


        return open(path, authorization)

    def delete(self, path):
        os.remove(path) 