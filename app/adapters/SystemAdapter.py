import sys
import subprocess
import argparse


class SystemAdapter:
    instance = None

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Récupère des infos d\'un pdf')

        parser.add_argument('-i', '--input', type=None,
                            help="Chemin du fichier d'entrée")

        parser.add_argument('-o', '--output',
                            help="Chemin du fichier de sortie")

        parser.add_argument('-m', '--menu', action='store_true', help='Sélection des fichiers via un menu')

        exclusiveGroup = parser.add_mutually_exclusive_group(required=True)

        exclusiveGroup.add_argument('-t', '--text', action='store_true',
                                    help='Convertir au format text')
        exclusiveGroup.add_argument('-x', '--xml', action='store_true',
                                    help='Convertir au format pdf')

        self.args = parser.parse_args()

    @staticmethod
    def getInstance():
        if (SystemAdapter.instance == None):
            SystemAdapter.instance = SystemAdapter()

        return SystemAdapter.instance

    def getArgv(self):
        return sys.argv

    def getArguments(self):
        return self.args

    def runCommand(self, command: str):
        print(command)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        if (error != None):
            raise Exception(error)

        return output
