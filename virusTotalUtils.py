from requests.models import Response
import requests
import os
from vars import apiBaseUrl

def uploadFile(filePath: str) -> Response:
	print("Uploading file to VirusTotal API v3...")

	slash = "\\" if "\\" in filePath else "/"
	fileName = filePath.split(slash)[-1]
	files = {"file": (fileName, open(filePath, "rb"))}
	headers = {
		"accept": "application/json",
		# "content-type": "multipart/form-data",
		"x-apikey": os.getenv("VIRUS_TOTAL_API_KEY")
	}

	return requests.post(
		f"{apiBaseUrl}/files",
		headers=headers,
		files=files
	)

def getAnalysis(id: int) -> Response:
	print("Fetching results from VirusTotal API v3...")