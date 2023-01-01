from common.recoverPDFtoTextOutput import recoverPDFtoTextOutput
from common.runPDFtoText import runPDFtoText
from adapters.SystemAdapter import SystemAdapter
from common.menu import menu

def main(args):
    if args.menu:
        menu(args)
    else:
        if args.text:
            print('On récupère au format text')

            runPDFtoText(args.input)
            file = recoverPDFtoTextOutput(args.output)
            file.toTXT().create()

        if args.xml:
            print('On récupère au format xml')
            runPDFtoText(args.input)
            file = recoverPDFtoTextOutput(args.output)
            file.toXML().create()

if __name__ == '__main__':
    main(SystemAdapter.getInstance().getArguments())
