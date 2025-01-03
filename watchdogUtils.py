from watchdog.events import (
	FileSystemEvent,
	FileSystemEventHandler,
	DirCreatedEvent,
	DirMovedEvent,
	DirModifiedEvent,
	FileCreatedEvent,
	FileMovedEvent,
	FileModifiedEvent
)
import os
import json
from virusTotalUtils import uploadFile, getAnalysis, printAnalysis, handleAnalysis
from utils import validateFileExtensionsMatchesContent

# https://python-watchdog.readthedocs.io/en/stable/index.html
class MyOverrideEventHandler(FileSystemEventHandler):
	def __init__(self):
		self.fileCreatedAt = 0

	def on_any_event(self, event: FileSystemEvent) -> None:
		if (
			(
				type(event) is DirCreatedEvent or
				type(event) is DirMovedEvent or
				type(event) is DirModifiedEvent
			) and
			event.is_directory
		):
			print("Error: Please upload a single file, not a folder/directory")
			os._exit(1)

		print(f"Watchdog noticed {event.src_path} was {event.event_type}")

		if (
			(
				type(event) is FileCreatedEvent or
				type(event) is FileMovedEvent or
				type(event) is FileModifiedEvent
			) and
			not event.is_directory
		):
			if(not validateFileExtensionsMatchesContent(event.src_path)):
				return

			uploadedFileId = None

			try:
				uploadedFileId = uploadFile(event.src_path)
			except Exception as e:
				print(f"Error: {e}")
				print("Something went wrong when uploading file")
				os._exit(1)

			if uploadedFileId == None:
				return

			strAnalysis = getAnalysis(uploadedFileId)
			jsonAnalysis = json.loads(strAnalysis)
			printAnalysis(jsonAnalysis)
			handleAnalysis(jsonAnalysis, event.src_path)
		