from adapters.FileSystemAdapter import FileSystemAdapter
from models.File import File


class PDF(File):
    @staticmethod
    def read(path: str):
        return PDF(path, FileSystemAdapter.getInstance().read(path))

    def extractAbstract(self):
        content = self.content

        abstractStartsAt = content.find("Abstract")

        print(abstractStartsAt)

        fromAbstract = content[abstractStartsAt:]

        abstractEndsAt1 = fromAbstract.find("\n1")
        abstractEndsAtI = fromAbstract.find("\nI.")

        if (
            (abstractEndsAtI < abstractEndsAt1 and 0 < abstractEndsAtI)
            or abstractEndsAt1 < 0
        ):
            abstractEndsAt = abstractEndsAtI
        else:
            abstractEndsAt = abstractEndsAt1

        print(abstractEndsAt)

        abstract = content[abstractStartsAt:abstractEndsAt +
                           len("\n1 Introduction")]

        return abstract
