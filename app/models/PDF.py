from adapters.SystemAdapter import SystemAdapter
from adapters.FileSystemAdapter import FileSystemAdapter
from models.File import File
import os


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


    def extractBiblio(self):
        block_regex = r'\<block[\s\S]+?\>[\s\S]+?\<\/block\>'
        word_regex = r'(<word xMin="(\d*[\.]\d*)" yMin="(\d*[\.]\d*)" xMax="(\d*[\.]\d*)" yMax="(\d*[\.]\d*)">(\.?[0-9]*)*references?</word>' \
                     r'|<word xMin="(\d*[\.]\d*)" yMin="(\d*[\.]\d*)" xMax="(\d*[\.]\d*)" yMax="(\d*[\.]\d*)">(\.?[0-9]*)*r</word>\s+?' \
                     r'<word xMin="(\d*[\.]\d*)" yMin="(\d*[\.]\d*)" xMax="(\d*[\.]\d*)" yMax="(\d*[\.]\d*)">(\.?[0-9]*)*eferences?</word>)'
        ref_regex = r'<line xMin="(\d*[\.]\d*)" yMin="(\d*[\.]\d*)" xMax="(\d*[\.]\d*)" yMax="(\d*[\.]\d*)">\s+?' + word_regex + '\s+?</line>'
        i = 0
        ref_blocks = ''
        blocks = re.findall(block_regex, self.content)

        for block in blocks:
            if re.findall(ref_regex, block, flags=re.IGNORECASE):
                while i < len(blocks):
                    ref_blocks = ref_blocks + blocks[i]
                    i = i +1
                continue
            i = i + 1

        words = re.sub(r'<[\s\S]+?>', '', ref_blocks)

        return ' '.join(words.split())
