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
		print(f"Detected file: {event.src_path}")

		uploadedFileId = None

		try:
			uploadRes = uploadFile(event.src_path)

			match uploadRes.status_code:
				case 200:
					print("Successfully Uploaded File")
					uploadedFileId = uploadRes.data.id
				case 204:
					print("Daily or Per Minute request quota reached - Please try again later")
				case _:
					print(f"Error: {uploadRes.reason}")
					print(f"Error Text: {uploadRes.text}")
		except Exception as e:
			print(f"Error: {e}")
			print("Something went wrong when uploading file")
			os._exit(1)
		
		if uploadedFileId == None:
			return
		
		print(f"uploadedFileId {uploadedFileId}")
		