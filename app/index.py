from adapters.TerminalAdapter import TerminalAdapter
from adapters.FileSystemAdapter import FileSystemAdapter
from adapters.SystemAdapter import SystemAdapter
from models.File import File
from models.PDF import PDF

import argparse

PDFTOTEXT = "pdftotext -raw"
PDFTOTEXTTITLE = "pdftotext -bbox-layout -q -l 1"
TEMP_FILE_PATH = "temp.txt"


def run_pdftotext(bbox_option: bool = False) -> File:
    command = PDFTOTEXTTITLE if bbox_option else PDFTOTEXT

    TerminalAdapter.basic(
        SystemAdapter.getInstance().runCommand(
            command
            + " "
            + SystemAdapter.getInstance().getArgv()[1]
            + " "
            + TEMP_FILE_PATH
        )
    )
    file = PDF.read(TEMP_FILE_PATH)
    file.path = SystemAdapter.getInstance().getArgv()[2]
    file.create()

    return file


def main(args):
    if args['text']:
        print('On récupère au format text')

    if args['xml']:
        print('On récupère au format xml')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Récupère des infos d\'un pdf')
    action = parser.add_mutually_exclusive_group(required=True)

    action.add_argument('-t', '--text', metavar='pdfFilename',
                        help='Infos au format text')
    action.add_argument('-x', '--xml', metavar='pdfFilename',
                        help='Infos au format pdf')

    args = parser.parse_args()
    main(vars(args))
