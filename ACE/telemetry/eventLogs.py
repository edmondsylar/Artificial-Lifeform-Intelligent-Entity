import win32evtlog
import pythoncom
from rich.console import Console

console = Console()

logtype = 'System'
log = win32evtlog.OpenEventLog(None, logtype)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ

try:
    events = win32evtlog.ReadEventLog(log, flags, 0)
    for event in events:
        console.print(f"Event ID: {event.EventID}")
        console.print(f"Time Generated: {event.TimeGenerated.Format()}")
        strings = event.StringInserts
        if strings:
            console.print("\n".join(strings))
finally:
    win32evtlog.CloseEventLog(log)