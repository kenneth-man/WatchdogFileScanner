from requests.models import Response
import requests
import os
import json
from vars import apiBaseUrl

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