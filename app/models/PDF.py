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

    def extractFileName(self) :
        #basename va recuperer le dernier contenue du chemin indiqué par exemple ===> torres.pdf 
        #argv[1] car on met le chemin vers le fichier pdf dans le premier argument
        file_name = os.path.basename(SystemAdapter.getInstance().getArgv()[1]) 
        #file_name[0]===>torres
        tmpName = os.path.splitext(file_name)[0]
        #si eventuellement y a un espace il le transform en _
        for caractere in tmpName : 
            if(caractere == " ") : 
                caractere = "_"
        return tmpName