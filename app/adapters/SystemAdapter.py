import sys
import subprocess


class SystemAdapter:
    instance = None

    @staticmethod
    def getInstance():
        if (SystemAdapter.instance == None):
            SystemAdapter.instance = SystemAdapter()

        return SystemAdapter.instance

    def getArgv(self):
        return sys.argv

    def runCommand(self, command: str):
        print(command)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        if (error != None):
            raise Exception(error)

        return output
