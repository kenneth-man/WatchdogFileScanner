import sys
import os
import shutil
import magic
import mimetypes
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

def validateFileExtensionsMatchesContent(filePath: str) -> bool:
	mimeType = magic.from_file(filePath, mime=True)
	extension = mimetypes.guess_extension(mimeType)

	if(mimeType == "node/x-empty"):
		print("Error: File is empty")
		return False

	if(extension is None):
		print("Error: Cannot get extension from mimetype")
		return False

	fileNameExtension = getFileExtension(filePath)

	if(fileNameExtension):
		if(extension == fileNameExtension):
			print("File extension matches content")
		else:
			print("File extension doesn't match content")
			print("Aborting Upload to VirusTotal API v3")
			print(f"Moving {filePath} to '../'")
			modifyFile(ModifyAction.MOVE, filePath, "../")
		return extension == fileNameExtension

def getFileExtension(filePath: str) -> str | None:
	elements = filePath.split(".")
	print(elements)

	if(len(elements) < 2):
		print("Error: Cannot get extension from filename")
		return

	return f".{elements[len(elements) - 1]}"

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