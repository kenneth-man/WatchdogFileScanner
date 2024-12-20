from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
import sys
import time
# import shutil
# shutil.move(event.src_path, r'C:\Users\win10\Desktop\Text_Documents')

class MyEventHandler(FileSystemEventHandler):
	def on_any_event(self, event: FileSystemEvent) -> None:
		print(event)

def main():
	if len(sys.argv) != 2:
		print("Error: Incorrect command")
		print("Please follow the correct format: `python ./main.py <PATH TO FOLDER>`")
		return

	event_handler = MyEventHandler()
	observer = Observer()
	observer.schedule(event_handler, sys.argv[len(sys.argv) - 1], recursive=True)
	observer.start()
	print("Watchdog is watching for events...")

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		# ctrl + c raises a 'KeyboardInterrupt' in python
		print("Exiting...")
		sys.exit()
	except Exception as e:
		print(f"Error: {e}")
	finally:
		observer.stop()
		observer.join()

if __name__ == "__main__":
	main()