from adapters.SystemAdapter import SystemAdapter
from models.File import File

PDFTOTEXT = "pdftotext -raw"
PDFTOTEXTTITLE = "pdftotext -bbox-layout -q -l 1"
PDFTOTEXTBBOX = "pdftotext -bbox-layout"
TEMP_FILE_PATH = "./app/temp.txt"


def runPDFtoText(input: str, bbox_option: bool = False, title: bool = False) -> File:
    if title:
        command = PDFTOTEXTTITLE
    else:
        command = PDFTOTEXTBBOX if bbox_option else PDFTOTEXT

    SystemAdapter.getInstance().runCommand(
        command
        + " "
        + input
        + " "
        + TEMP_FILE_PATH
    )
