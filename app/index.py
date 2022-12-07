from adapters.TerminalAdapter import TerminalAdapter
from adapters.FileSystemAdapter import FileSystemAdapter
from adapters.SystemAdapter import SystemAdapter
from models.File import File
from models.PDF import PDF

PDFTOTEXT = "pdftotext -raw"
TEMP_FILE_PATH = "./app/temp.txt"

TerminalAdapter.basic(
    SystemAdapter.getInstance().runCommand(
        PDFTOTEXT
        + " "
        + SystemAdapter.getInstance().getArgv()[1]
        + " "
        + TEMP_FILE_PATH
    )
)

file = PDF.read(TEMP_FILE_PATH)

file.path = SystemAdapter.getInstance().getArgv()[2]

file.create()

FileSystemAdapter.getInstance().delete(TEMP_FILE_PATH)

print(file.extractAbstract())
print(file.getFileName())