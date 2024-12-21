import sys
import os
# import shutil
# shutil.move(event.src_path, r'C:\Users\win10\Desktop\Text_Documents')

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