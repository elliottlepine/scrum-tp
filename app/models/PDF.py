from adapters.FileSystemAdapter import FileSystemAdapter
from models.File import File


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
