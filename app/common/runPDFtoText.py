from adapters.SystemAdapter import SystemAdapter
from models.File import File

PDFTOTEXT = "pdftotext -raw"
PDFTOTEXTTITLE = "pdftotext -bbox-layout -q -l 1"
TEMP_FILE_PATH = "./app/temp.txt"


def runPDFtoText(input: str, bbox_option: bool = False) -> File:
    command = PDFTOTEXTTITLE if bbox_option else PDFTOTEXT

    SystemAdapter.getInstance().runCommand(
        command
        + " "
        + input
        + " "
        + TEMP_FILE_PATH
    )
