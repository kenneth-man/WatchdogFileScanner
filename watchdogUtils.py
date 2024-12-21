from watchdog.events import FileSystemEvent, FileSystemEventHandler

class MyOverrideEventHandler(FileSystemEventHandler):
	def on_any_event(self, event: FileSystemEvent) -> None:
		print(event)