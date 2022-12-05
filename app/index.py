from adapters.TerminalAdapter import TerminalAdapter
from adapters.FileSystemAdapter import FileSystemAdapter

backlog = FileSystemAdapter.getInstance().open('/home/nas-wks01/users/uapv2102160/Documents/L3/scrum/tp1/backlog.md')

TerminalAdapter.basic(backlog.getContent())