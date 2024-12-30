from requests.models import Response
import requests
import os
import json
from vars import apiBaseUrl
from utils import modifyFile
from enums import ModifyAction
from datetime import date

# https://docs.virustotal.com/reference/overview
def uploadFile(filePath: str) -> str | None:
	print("Uploading file to VirusTotal API v3")

	slash = "\\" if "\\" in filePath else "/"
	fileName = filePath.split(slash)[-1]
	files = {"file": (fileName, open(filePath, "rb"))}
	headers = {
		"accept": "application/json",
		# "content-type": "multipart/form-data",
		"x-apikey": os.getenv("VIRUS_TOTAL_API_KEY")
	}

	response = requests.post(
		f"{apiBaseUrl}/files",
		headers=headers,
		files=files
	)

	match response.status_code:
		case 200:
			print("Successfully Uploaded File")
			# api returns a binary string
			strData = response.content.decode('ascii')
			jsonData = json.loads(strData)
			return jsonData["data"]["id"]
		case 204:
			print("Daily or Per Minute request quota reached; Please try again later")
		case _:
			print(f"Error: {response.reason}")
			print(f"Error Text: {response.text}")

	return None

def getAnalysis(fileId: str) -> str | None:
	print("Fetching analysis from VirusTotal API v3")

	headers = {
		"accept": "application/json",
		"x-apikey": os.getenv("VIRUS_TOTAL_API_KEY")
	}

	response = requests.get(
		f"{apiBaseUrl}/analyses/{fileId}",
		headers=headers
	)

	if response.text == None:
		return None

	return response.text

def printAnalysis(jsonAnalysis) -> None:
	print("\n")
	print("====================Results====================")
	print("Total number of reports saying that the file is...")
	print(f"Malicious: {jsonAnalysis["data"]["attributes"]["stats"]["malicious"]}")
	print(f"Suspicious: {jsonAnalysis["data"]["attributes"]["stats"]["suspicious"]}")
	print(f"Undetected: {jsonAnalysis["data"]["attributes"]["stats"]["undetected"]}")
	print(f"Harmless: {jsonAnalysis["data"]["attributes"]["stats"]["harmless"]}")
	print("\n")
	print("The engines used to analyze the file...")
	engines = jsonAnalysis["data"]["attributes"]["results"].values()
	enginesList = list(engines)
	enginesList.sort(key=lambda x: x["engine_name"].casefold())
	for val in enginesList:
		print(f"Engine: {val["engine_name"]}")
		print(f"Engine Version: {val["engine_version"]}")
		print(f"Engine Update: {val["engine_update"]}")
		print(f"Category: {val["category"]}")
		print(f"Result: {val["category"] if val["category"] else "null"}")
		print("\n")

def handleAnalysis(
	jsonAnalysis,
	filePath: str
) -> None:
	threshold = 3

	if (
		int(jsonAnalysis["data"]["attributes"]["stats"]["malicious"]) > threshold or
		int(jsonAnalysis["data"]["attributes"]["stats"]["suspicious"]) > threshold
	):
		print("Uploaded file was found to be Malicious or Suspicious and will be deleted")
		modifyFile(ModifyAction.DELETE, filePath)
	else:
		today = str(date.today())
		destinationPath = f"../{today}-WATCHDOG-VERIFIED"

		if (os.path.exists(destinationPath) and os.path.isdir(destinationPath)):
			print(f"Uploaded file was found to be Safe and will be moved to {destinationPath}")
		else:
			os.makedirs(destinationPath)
			print(f"Uploaded file was found to be Safe and will be moved to a new directory {destinationPath}")

		modifyFile(ModifyAction.MOVE, filePath, destinationPath)