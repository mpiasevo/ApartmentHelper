import json
import sys
import time
import datetime
import gspread
import subprocess
import Apartmentparser
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from oauth2client.service_account import ServiceAccountCredentials
GDOCS_OAUTH_JSON       = 'JSON-KEY-FILE'
GDOCS_SPREADSHEET_NAME = 'GOOGLE-SHEET-NAME'
#FREQUENCY_SECONDS      = 10
def login_open_sheet(oauth_key_file, spreadsheet):
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, 
                      scopes = ['https://spreadsheets.google.com/feeds',
                                'https://www.googleapis.com/auth/drive'])
        gc = gspread.authorize(credentials)
        worksheet = gc.open(spreadsheet).sheet1
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet. Check OAuth credentials, spreadsheet name, and')
        print('make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)

def distance(work,address):
    geolocator = Nominatim(user_agent="iot-application")
    address1 = work
    address2 = address
    location1 = geolocator.geocode(address1)
    location2 = geolocator.geocode(address2)

    location1 = (location1.latitude, location1.longitude)
    location2 = (location2.latitude, location2.longitude)

    #print(geodesic(location1, location2).mi)
    distance = geodesic(location1, location2).mi
    return distance

def settings(worksheet):
    if worksheet is None:
            worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
    city = input('Input the City: ')
    people = input('Input the number of people renting: ')
    work2 = input('Input company name: ')
    work = input('Input work address: ')
    util = input('Input the average utility cost: ')
    try:
        worksheet.append_row((city, people, work, util, work2))
        worksheet.append_row(('Date/Time', 'Rent', 'Bedrooms', 'Bathrooms', 'Sqft', 'Address', 'Link', 'Walk Score', 'Transit Score', 'Bike Score', 'Distance to Work'))

    # worksheet.append_row((dat, cpu, tmp))
    # gspread==0.6.2
    # https://github.com/burnash/gspread/issues/511  
    except:
        print('Append error, logging in again')
        worksheet = None
        #time.sleep(FREQUENCY_SECONDS)
    print('Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME))
        #time.sleep(FREQUENCY_SECONDS)
    return work

print('Auto Apartments.com Parser, if apartment link includes multiple units, may not work...')
print('Press Ctrl-C to quit.')
worksheet = None
#Could add an option to save as excel file instead of using sheets?
work = settings(worksheet)

while True:
    url = input('Input URL from Apartments.com: ')
    if "apartments.com" in url:
        if worksheet is None:
            worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
        dat = datetime.datetime.now()
        rent = Apartmentparser.rentInfo(url)[0]
        bed = Apartmentparser.rentInfo(url)[1]
        bath = Apartmentparser.rentInfo(url)[2]
        sqft = Apartmentparser.rentInfo(url)[3]
        add = Apartmentparser.rentInfo(url)[4]
        link = Apartmentparser.rentInfo(url)[5]

        walk = Apartmentparser.score(url)[0]
        transit = Apartmentparser.score(url)[1]
        bike = Apartmentparser.score(url)[2]

        distance2 = distance(work, add)

        try:
            worksheet.append_row((str(dat), rent, bed, bath, sqft, add, link, walk, transit, bike, distance2))
    #       worksheet.append_row((dat, cpu, tmp))
    # gspread==0.6.2
    # https://github.com/burnash/gspread/issues/511  
        except:
            print('Append error, logging in again')
            worksheet = None
            time.sleep(FREQUENCY_SECONDS)
        print('Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME))
        #time.sleep(FREQUENCY_SECONDS)
    else:
        print("Please use a link from Apartments.com")