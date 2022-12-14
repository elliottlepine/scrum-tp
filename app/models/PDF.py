from adapters.SystemAdapter import SystemAdapter
from adapters.FileSystemAdapter import FileSystemAdapter
from models.File import File
import os

from lxml import etree

class PDF(File):
    @staticmethod
    def read(path: str):
        return PDF(path, FileSystemAdapter.getInstance().read(path))

    def extractFileName(self):
        # basename va recuperer le dernier contenue du chemin indiqué par exemple ===> torres.pdf
        # argv[1] car on met le chemin vers le fichier pdf dans le premier argument
        file_name = os.path.basename(SystemAdapter.getInstance().getArgv()[1])
        # file_name[0]===>torres
        tmpName = os.path.splitext(file_name)[0]
        # si eventuellement y a un espace il le transform en _
        for caractere in tmpName:
            if (caractere == " "):
                caractere = "_"
        return tmpName

    def extractAbstract(self):
        content = self.content

        # Split the text into lines
        lines = content.split("\n")

        # Find the index of the first line of the abstract
        startAbstract = None
        for i, line in enumerate(lines):
            if line.startswith("Abstract") or line.startswith("ABSTRACT"):
                startAbstract = i
                break

        # If no lines start with "Abstract", return an empty string
        if startAbstract is None:
            return ""

        # Find the index of the last line of the abstract
        endAbstract = None
        for i, line in enumerate(lines[startAbstract + 1:], startAbstract + 1):
            if (
                line.startswith("I. ")
                or line.startswith("1 ")
                or line.startswith("1. ")
                or line.startswith("Introduction")
            ):
                endAbstract = i
                break

        # If no lines start with "I. " or "1 ", return an empty string
        if endAbstract is None:
            return ""

        # Return the abstract block by concatenating the individual lines
        return "\n".join(lines[startAbstract:endAbstract])

    def toXML(self):
        article = etree.Element("Article")
        preamble = etree.SubElement(article, "preamble")
        preamble.text = self.extractFileName(self)
        titre = etree.SubElement(article, "titre")
        abstract = etree.SubElement(article, "abstract")
        abstract.text = self.extractAbstract(self)
        
    

