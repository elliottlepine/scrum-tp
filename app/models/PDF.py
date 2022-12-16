from adapters.SystemAdapter import SystemAdapter
from adapters.FileSystemAdapter import FileSystemAdapter
from models.File import File
from common.runPDFtoText import TEMP_FILE_PATH, runPDFtoText
import os
import re

from xml.etree import ElementTree as root
from xml.dom import minidom


class PDF(File):
    def __init__(self, path: str, file):
        super().__init__(path, file)

        self.originalPath = path

    @staticmethod
    def read(path: str):
        return PDF(path, FileSystemAdapter.getInstance().read(path))

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

    def extractBiblio(self):
        runPDFtoText(
            SystemAdapter.getInstance().getArguments().input,
            True
        )

        file = PDF.read(TEMP_FILE_PATH)

        block_regex = r'\<block[\s\S]+?\>[\s\S]+?\<\/block\>'
        word_regex = r'(<word xMin="(\d*[\.]\d*)" yMin="(\d*[\.]\d*)" xMax="(\d*[\.]\d*)" yMax="(\d*[\.]\d*)">(\.?[0-9]*)*references?</word>' \
                     r'|<word xMin="(\d*[\.]\d*)" yMin="(\d*[\.]\d*)" xMax="(\d*[\.]\d*)" yMax="(\d*[\.]\d*)">(\.?[0-9]*)*r</word>\s+?' \
                     r'<word xMin="(\d*[\.]\d*)" yMin="(\d*[\.]\d*)" xMax="(\d*[\.]\d*)" yMax="(\d*[\.]\d*)">(\.?[0-9]*)*eferences?</word>)'
        ref_regex = r'<line xMin="(\d*[\.]\d*)" yMin="(\d*[\.]\d*)" xMax="(\d*[\.]\d*)" yMax="(\d*[\.]\d*)">\s+?' + \
            word_regex + '\s+?</line>'
        i = 0
        ref_blocks = ''
        blocks = re.findall(block_regex, file.content)

        for block in blocks:
            if re.findall(ref_regex, block, flags=re.IGNORECASE):
                while i < len(blocks):
                    ref_blocks = ref_blocks + blocks[i]
                    i = i + 1
                continue
            i = i + 1

        words = re.sub(r'(?!</line>)<[\s\S]+?>', '', ref_blocks)

        return re.sub(r'</line>', '\n', ' '.join(words.split()))

    ###
    # Returns corpus
    ###

    def extractCorpus(self):
        content = self.content

        # Split the text into lines
        lines = content.split("\n")

        # Find the index of the first line of the abstract
        startCorpus = None
        for i, line in enumerate(lines):
            if (
                line.startswith("I. ")
                or line.startswith("1 ")
                or line.startswith("1. ")
                or line.startswith("Introduction")
            ):
                startCorpus = i
                break

        # If no lines start with "Abstract", return an empty string
        if startCorpus is None:
            return ""

        # Find the index of the last line of the abstract
        endCorpus = None
        for i, line in enumerate(lines[startCorpus + 1:], startCorpus + 1):
            if (
                "Conclusion" in line
                or "CONCLUSION" in line
                or "Discussion" in line
                or "DISCUSSION" in line
                or "References" in line
            ):
                endCorpus = i
                break

        # If no lines start with "I. " or "1 ", return an empty string
        if endCorpus is None:
            return ""

        # Return the abstract block by concatenating the individual lines
        corpus = ""

        splittedCorpus = lines[startCorpus:endCorpus]

        for i, line in enumerate(splittedCorpus):
            corpus += line + "\n"

            if (line.endswith('.')):
                corpus += "\n"

        return corpus

    def extractAuthors(self):
        content = self.content

        abstract = self.extractAbstract()
        title = self.extractTitle()

        lines = content.split(title)[1] if len(content.split(title)) > 1 else ''
        authors = lines.split(abstract)[0] if abstract != '' and len(lines.split(abstract)) > 1 else ''

        return authors

    ###
    # Returns the conclusion of the paper
    ###
    def extractConclusion(self):
        content = self.content

        # Split the text into lines
        lines = content.split("\n")

        # Find the index of the first line of the abstract
        startConclusion = None
        for i, line in enumerate(lines):
            if (
                "Conclusion" in line
                or "CONCLUSION" in line
                or "Conclusions" in line
                or "CONCLUSIONS" in line
            ):
                startConclusion = i
                break

        # If no lines start with "Abstract", return an empty string
        if startConclusion is None:
            return ""

        # Find the index of the last line of the abstract
        endConclusion = None
        for i, line in enumerate(lines[startConclusion + 1:], startConclusion + 1):
            if (
                "Acknowledgements" in line
                or "ACKNOWLEDGMENT" in line
                or "Acknowledgments" in line
                or "Reference" in line

            ):
                endConclusion = i
                break

        # If no lines start with "I. " or "1 ", return an empty string
        if endConclusion is None:
            return ""

        # Return the abstract block by concatenating the individual lines
        conclusion = ""

        splittedConclusion = lines[startConclusion:endConclusion]

        for i, line in enumerate(splittedConclusion):
            conclusion += line + "\n"

            if (line.endswith('.')):
                conclusion += "\n"

        return conclusion

    ###
    # Parses self.content and converts it to TXT
    ###
    def toTXT(self):
        content = ""

        content += self.extractFileName() + "\n\n"
        content += self.extractTitle() + "\n\n"
        content += self.extractAuthors() + "\n\n"
        content += self.extractAbstract() + "\n\n"
        content += self.extractCorpus() + "\n\n"
        content += self.extractConclusion() + "\n\n"
        content += self.extractBiblio()

        self.content = content

        return self

    def toXML(self):
        root = minidom.Document()
        article = root.createElement("Article")
        root.appendChild(article)

        preamble = root.createElement("preamble")
        preamble.setAttribute("preamble", self.extractFileName())
        article.appendChild(preamble)

        titre = root.createElement("titre")
        titre.setAttribute("titre", self.extractTitle())
        article.appendChild(titre)

        authors = root.createElement("auteur")
        authors.setAttributes("auteur", self.extractAuthors())
        article.appendChild(authors)

        abstract = root.createElement("abstract")
        abstract.setAttribute("abstract", self.extractAbstract())
        article.appendChild(abstract)

        corpus = root.createElement("corpus")
        corpus.setAttribute("corpus", self.extractCorpus())
        corpus.appendChild(corpus)

        conclusion = root.createElement("conclusion")
        conclusion.setAttribute("conclusion", self.extractCorpus())
        conclusion.appendChild(conclusion)

        self.content = root.toprettyxml(indent="\t")
        biblio = root.createElement("biblio")
        biblio.setAttribute("biblio", self.extractBiblio())
        article.appendChild(biblio)

        self.content = root.toprettyxml(indent="\t")
        return self
