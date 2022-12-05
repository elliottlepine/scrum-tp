from adapters.TerminalAdapter import TerminalAdapter
from adapters.SystemAdapter import SystemAdapter

# file = FileSystemAdapter.getInstance().open(SystemAdapter.getInstance().getArgv())

TerminalAdapter.basic(SystemAdapter.getInstance().runCommand("pdftotext -raw " + SystemAdapter.getInstance().getArgv()[1]) + "")