from adapters.TerminalAdapter import TerminalAdapter
from adapters.FileSystemAdapter import FileSystemAdapter
from adapters.SystemAdapter import SystemAdapter

backlog = FileSystemAdapter.getInstance().open(SystemAdapter.getInstance().getArgv())

TerminalAdapter.basic(backlog.getContent())