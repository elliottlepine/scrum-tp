from adapters.FileSystemAdapter import FileSystemAdapter

class File:
    def __init__(self, path: str, file):
        self.file = file
        self.path = path
        self.content = self.file.read()

    def create(self):
        FileSystemAdapter.getInstance().create(self)

    @staticmethod
    def read(path: str):
        return File(FileSystemAdapter.getInstance().read(path))

    def delete(self):
        FileSystemAdapter.getInstance().delete(self.path)