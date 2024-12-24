import time
from dotenv import load_dotenv
from watchdog.observers import Observer
from utils import validateFolderPath
from watchdogUtils import MyOverrideEventHandler

def main() -> None:
	load_dotenv()
	folderPath = validateFolderPath()

	if (not folderPath):
		return

	event_handler = MyOverrideEventHandler()
	observer = Observer()
	observer.schedule(event_handler, folderPath, recursive=True)
	observer.start()
	print("Watchdog is watching for events...")

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		# ctrl + c raises a 'KeyboardInterrupt' in python
		print("Exiting program")
	except Exception as e:
		print(f"Error: {e}")
	finally:
		# documentation example does this; ensures all resources are released upon termination
		observer.stop()
		observer.join()

if __name__ == "__main__":
	main()