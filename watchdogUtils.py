from watchdog.events import (
	FileSystemEvent,
	FileSystemEventHandler,
	DirCreatedEvent,
	DirMovedEvent
)
import os
from virusTotalUtils import uploadFile, getAnalysis

# https://python-watchdog.readthedocs.io/en/stable/index.html
class MyOverrideEventHandler(FileSystemEventHandler):
	def __init__(self):
		self.fileCreatedAt = 0

	def on_any_event(self, event: FileSystemEvent) -> None:
		if (
			(
				type(event) is DirCreatedEvent or
				type(event) is DirMovedEvent
			) and
			event.is_directory
		):
			print("Error: Please upload a single file, not a folder/directory")
			os._exit(1)
		print(f"Uploaded file: {event.src_path}")
		uploadFile()