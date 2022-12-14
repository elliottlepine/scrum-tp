from adapters.SystemAdapter import SystemAdapter
from adapters.FileSystemAdapter import FileSystemAdapter
from models.File import File
from common.runPDFtoText import TEMP_FILE_PATH, runPDFtoText
import os
import re

from xml.etree.cElementTree import etree

class PDF(File):
    def __init__(self, path: str, file):
        super().__init__(path, file)

        self.originalPath = path

    @staticmethod
    def read(path: str):
        return PDF(path, FileSystemAdapter.getInstance().read(path))

    ###
    # Returns the file name
    ###
    def extractFileName(self):
        # basename va recuperer le dernier contenue du chemin indiqué par exemple ===> torres.pdf
        # argv[1] car on met le chemin vers le fichier pdf dans le premier argument
        file_name = os.path.basename(
            SystemAdapter.getInstance().getArguments().input)
        # file_name[0]===>torres
        tmpName = os.path.splitext(file_name)[0]
        # si eventuellement y a un espace il le transform en _
        for caractere in tmpName:
            if (caractere == " "):
                caractere = "_"
        return tmpName

    ###
    # Returns the abstract of the paper
    ###
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

    
    

    ###
    # Returns the title of the paper
    ###
    def extractTitle(self):
        runPDFtoText(
            SystemAdapter.getInstance().getArguments().input,
            True
        )

        file = PDF.read(TEMP_FILE_PATH)

        block_regex = r'\<block[\s\S]+?\>[\s\S]+?\<\/block\>'
        blocks = re.findall(block_regex, file.content)
        max_height_block = 0
        title_block = blocks[0]

        for block in blocks[:3]:
            block_max_height = self.getMaxHeight(block)
            if max_height_block < block_max_height:
                max_height_block = block_max_height
                title_block = block

        words = re.sub(r'<[\s\S]+?>', '', title_block)

        file.delete()

        return ' '.join(words.split())

    def getMaxHeight(self, block: str) -> int:
        word_regex = r'\<word[\s\S]+?\>[\s\S]+?\<\/word\>'
        max_height = 0

        for word in re.findall(word_regex, block):
            word_height_min = self.getWordHeight(word, min=True)
            word_height_max = self.getWordHeight(word, min=False)
            word_height = word_height_max - word_height_min
            if word_height > max_height:
                max_height = word_height

        return max_height

    def getWordHeight(self, word, *, min=True):
        decimal_regex = r'(\d*[\.]\d*)'
        height_max_regex = r'yMax=\"'
        height_min_regex = r'yMin=\"'
        regex = height_min_regex if min == True else height_max_regex
        try:
            height_tag = re.findall(regex + decimal_regex, word)
            height = re.findall(decimal_regex, height_tag[0])
        except Exception as e:
            print(e)
            return 0

        return float(height[0])
    
    ###
    # Parses self.content and converts it to TXT
    ###
    def toTXT(self):
        content = ""

        content += self.extractFileName() + "\n\n"
        content += self.extractTitle() + "\n\n"
        content += self.extractAbstract()

        self.content = content

        return self

    def toXML(self):
        article = etree.Element("Article")
        preamble = etree.SubElement(article, "preamble")
        preamble.text = self.extractFileName(self)
        titre = etree.SubElement(article, "titre")
        titre.text = self.extractTitle(self)
        abstract = etree.SubElement(article, "abstract")
        abstract.text = self.extractAbstract(self)
        