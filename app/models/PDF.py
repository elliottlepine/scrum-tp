from adapters.SystemAdapter import SystemAdapter
from adapters.FileSystemAdapter import FileSystemAdapter
from models.File import File
import os


class PDF(File):
    @staticmethod
    def read(path: str):
        return PDF(path, FileSystemAdapter.getInstance().read(path))

    def extractAbstract(self):
        content = self.content

        abstractStartsAt = content.find("ABSTRACT")

        abstractEndsAt = content.find("1")

        abstract = content[abstractStartsAt:abstractEndsAt]

        return abstract

    def getFileName(self) :
        file_name = os.path.basename(SystemAdapter.getinstance().getArgv()[1]) 
        tmpName = os.path.splitext(file_name)[0]
        for caractere in tmpName : 
            if(caractere == " ") : 
                caractere = "_"
        return tmpName