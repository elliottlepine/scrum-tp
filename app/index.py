from adapters.TerminalAdapter import TerminalAdapter
from adapters.FileSystemAdapter import FileSystemAdapter
from adapters.SystemAdapter import SystemAdapter
from models.File import File
from models.PDF import PDF

PDFTOTEXT = "pdftotext -raw"
PDFTOTEXTTITLE = "pdftotext -bbox-layout -q -l 1"
TEMP_FILE_PATH = "temp.txt"


def run_pdftotext(bbox_option: bool = False) -> File:
    command = PDFTOTEXTTITLE if bbox_option else PDFTOTEXT

    SystemAdapter.getInstance().runCommand(
        command
        + " "
        + SystemAdapter.getInstance().getArguments['inputPath']
        + " "
        + TEMP_FILE_PATH
    )

    file = PDF.read(TEMP_FILE_PATH)
    file.path = SystemAdapter.getInstance().getArguments['outputPath']
    # file.create()

    return file


def main(args):
    if args['text']:
        print('On récupère au format text')
        file = PDF.read(TEMP_FILE_PATH)

        file.toTXT().create()

    if args['xml']:
        print('On récupère au format xml')


if __name__ == '__main__':
    main(SystemAdapter.getInstance().getArguments())
