class File:
    def __init__(self, file, read: bool, write: bool):
        self.file = file
        self.canBeRead = read
        self.canBeWritten = write

    def getContent(self):
        return self.file.read()