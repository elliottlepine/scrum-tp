from common.recoverPDFtoTextOutput import recoverPDFtoTextOutput
from common.runPDFtoText import runPDFtoText
from adapters.SystemAdapter import SystemAdapter

import tkinter as tk, os
from tkinter import filedialog

def getFilePathNewFormat(directory: str, filename: str) -> str:
    return os.path.join(directory, os.path.basename(filename).rsplit('.', 1)[0])

def menu(args):
    root = tk.Tk()
    root.withdraw()

    files = filedialog.askopenfilenames(title="Sélectionner des fichiers pdf", filetypes=[("Fichiers pdf", "*.pdf")])

    if files:
        directory = filedialog.askdirectory(title="Sélectionner un dossier")

        if directory:
            for filename in files:
                if args.text:
                    print('On récupère au format text')

                    runPDFtoText(filename)
                    file = recoverPDFtoTextOutput(getFilePathNewFormat(directory, filename) + '.txt')
                    SystemAdapter.getInstance().args.input = filename
                    file.toTXT().create()

                if args.xml:
                    print('On récupère au format xml')
                    runPDFtoText(filename)
                    file = recoverPDFtoTextOutput(getFilePathNewFormat(directory, filename) + '.xml')
                    SystemAdapter.getInstance().args.input = filename
                    file.toXML().create()

        else:
            print("Aucun dossier sélectionné")
    else:
      print("Aucun fichier sélectionné")