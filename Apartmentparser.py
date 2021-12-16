import requests
from bs4 import BeautifulSoup
import re

#url = input('Enter URL from Apartments.com ')
#headers = {'user-agent': 'my-app/0.0.1'}
#r = requests.get(url, headers = headers)
#content = r.text
#soup = BeautifulSoup(content, 'html.parser')
def score(url):
    headers = {'user-agent': 'my-app/0.0.1'}
    r = requests.get(url, headers = headers)
    content = r.text
    soup = BeautifulSoup(content, 'html.parser')
    
    score = soup.find_all('div', {'class': 'score'})
    walk = str(score[0])
    walk = walk.split('>')[1].split('<')[0]

    transit = str(score[1])
    transit = transit.split('>')[1].split('<')[0]

    bike = str(score[2])
    bike = bike.split('>')[1].split('<')[0]

    #print(score)
    return walk,transit,bike

def rentInfo(url):
    headers = {'user-agent': 'my-app/0.0.1'}
    r = requests.get(url, headers = headers)
    content = r.text
    soup = BeautifulSoup(content, 'html.parser')
        
    rentInfoDetail = soup.find_all('p','rentInfoDetail')
    rent = str(rentInfoDetail[0])
    rent = rent.split('>')[1].split('<')[0]
    #print(rent)

    bedroom = str(rentInfoDetail[1])
    bedroom = bedroom.split('>')[1].split(' ')[0]
    #print(bedroom)

    bathroom = str(rentInfoDetail[2])
    bathroom = bathroom.split('>')[1].split(' ')[0]
    #print(bathroom)

    sqft = str(rentInfoDetail[3])
    sqft = sqft.split('>')[1].split(' ')[0]
    #print(sqft)
    addressInfo = soup.find_all('div', 'propertyAddressContainer')

    address = str(addressInfo[0])
    address = address.splitlines()
    address = ((address[2].split('>')[1].split('<')[0])+ ' ' +(address[6].split('>')[1].split('<')[0]))
    #address = address.split('>')[1].lstrip().rstrip('</div')
    #address = address[1] + ' ' + address[2] + ' ' + address[3] + ' ' + address[4]

    linkInfo = soup.find_all('link', href = re.compile('apartments.com'))
    link = str(linkInfo)
    link = link.splitlines()[0][13:].split('"')[0]
    #print(link)
    return rent,bedroom,bathroom,sqft,address,link

