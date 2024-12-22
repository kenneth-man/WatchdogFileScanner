from requests.models import Response

def uploadFile() -> Response:
	print("Uploading file to VirusTotal API v3...")

def getAnalysis(id: int) -> Response:
	print("Fetching results from VirusTotal API v3...")