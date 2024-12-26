import sys
import os
import shutil
from enums import ModifyAction

def validateFolderPath() -> str | None:
	if len(sys.argv) != 2:
		print("Error: Incorrect command. Please follow the format: " +
			"`python ./main.py <PATH TO FOLDER>`")
		return

	folderPath = sys.argv[len(sys.argv) - 1]

	if (not os.path.exists(folderPath)):
		print("Error: The specified path does not exist")
		return

	if (not os.path.isdir(folderPath)):
		print("Error: The specified path is not a folder/directory")
		return

	if (len(os.listdir(folderPath)) != 0):
		print("Error: The specified directory is not empty")
		return

	return folderPath

def modifyFile(
	modifyAction: ModifyAction,
	filePath: str,
	destinationPath: str = None
) -> None:
	match modifyAction:
		case ModifyAction.COPY:
			shutil.copy(filePath, destinationPath)
		case ModifyAction.DELETE:
			shutil.rmtree(filePath)
		case ModifyAction.MOVE:
			shutil.move(filePath, destinationPath)
		case _:
			print("Error: Invalid enum given for ModifyAction")