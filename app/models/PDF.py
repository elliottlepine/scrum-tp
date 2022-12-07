from adapters.FileSystemAdapter import FileSystemAdapter
from models.File import File


class PDF(File):
    @staticmethod
    def read(path: str):
        return PDF(path, FileSystemAdapter.getInstance().read(path))

    def extractAbstract(self):
        content = self.content

        # Split the text into lines
        lines = content.split("\n")

        # Find the index of the first line of the abstract
        startAbstract = None
        for i, line in enumerate(lines):
            if line.startswith("Abstract"):
                startAbstract = i
                break

        # If no lines start with "Abstract", return an empty string
        if startAbstract is None:
            return ""

        # Find the index of the last line of the abstract
        endAbstract = None
        for i, line in enumerate(lines[startAbstract + 1:], startAbstract + 1):
            if line.startswith("I. ") or line.startswith("1 "):
                endAbstract = i
                break

        # If no lines start with "I. " or "1 ", return an empty string
        if endAbstract is None:
            return ""

        # Return the abstract block by concatenating the individual lines
        return "\n".join(lines[startAbstract:endAbstract])
