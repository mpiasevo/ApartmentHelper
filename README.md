### This is a program which takes apartments from apartments.com and automatically pulls the Bedrooms, Bathrooms, Sqft, Address, Rent, Walk Score, Transit Score, Bike Score, and distance to work data and writes it to a google sheets document
### Sign up and log in the Google Cloud Platform Identity and Access Management [(IAM)](https://console.developers.google.com/projectselector/iam-admin/iam)

* Click "Create" and enter the project name, e.g., apartmentparser
* &equiv; > APIs & Services > + Enable APIs & Services > Enable both Drive API and Sheets API
* Credential > Create Credentials > Create service account key > Service account > apartmentparser > JSON key type > Create > download apartmentparser-xxxxxxxxxxxx.json

### Install gspread and oauth2client
```sh
$ sudo pip3 install -U gspread oauth2client
```
### If the JSON key file (* = xxxxxxxxxxxx) is on a laptop computer, secure copy it to the same directory as rpi_spreadsheet.py
```sh
$ scp apartmentparser-*.json pi@192.168.x.xxx:/home/pi/demo
```
### If the the JSON key file is on a Raspberry Pi, move it to the same directory as spreadsheet2.py

### Go to [Google Sheets](https://docs.google.com/spreadsheets/u/0)

* Start a new spreadsheet Apartment Search
* Share the spreadsheet with the "client_email" address in the .json file, select “Can edit,” and click "Send"
  * Will receive an email with the subject "Delivery Status Notification (Failure)" and the message "Address not found" from mailer-daemon@google.com

### Edit spreadsheet2.py

> GDOCS_OAUTH_JSON = 'apartmentparser-xxxxxxxxxxxx.json'

> GDOCS_SPREADSHEET_NAME = 'Apartment Search'

### Run spreadsheet2.py
```sh
$ python3 spreadsheet2.py
```
### Will ask you for an Apartments.com link; you must enter a link to an apartment from apartments.com (apartments with multiple units listed usually do not work correctly)
