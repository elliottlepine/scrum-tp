from common.runPDFtoText import TEMP_FILE_PATH
from models.PDF import PDF


def recoverPDFtoTextOutput(output):
    file = PDF.read(TEMP_FILE_PATH)

    file.delete()

    file.path = output

    return file
