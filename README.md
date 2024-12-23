# Watchdog File Scanner WIP
### Python script to check if files are malicious
### Files are uploaded to a specified folder path where watchdog will look at
### Uses the Virus Total API https://docs.virustotal.com/reference/overviewto to check the files for viruses
- ### I'm using Public (free) tier so the program is limited to 4 requests per minute/500 requests per day
- ### Due to this, only one file should be uploaded per minute

<br>

# How to use
### 1) Open terminal
### 2) Create a venv
`python -m venv <VENV NAME>`
### 3) Activate the venv
`./<VENV NAME>/Scripts/activate`
### 4) Install Dependencies
`pip install -r ./requirements.txt`
### 5) Execute the program
`python ./main.py <PATH TO FOLDER>`
### 6) Watchdog will now watch for any events in that specified folder (file creation, file deletion, etc...)

<br>

# Updating dependencies
### If you're adding new dependencies and need to update the `requirements.txt`
### 1) Activate the venv
### 2) Pip install your new dependencies
### 3) `pip freeze -l > requirements.txt`
### 4) Commit changes