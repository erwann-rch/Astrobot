############################# [ IMPORTS ] #############################

import json, xmltodict, requests, maya, os, time
import html.parser

from fake_useragent import UserAgent
from timezonefinder import TimezoneFinder
from geopy import Nominatim

import pdf_generator as pdf

############################# [ VARIABLES ] #############################

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko','Cache-Control':'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0'}
headers = {'User-Agent': f'{UserAgent().random}', 'Cache-Control': 'no-cache, no-store, must-revalidate',
           'Pragma': 'no-cache', 'Expires': '0'}  # Against python caching
lat = pdf.vars.get_lat()
lon = pdf.vars.get_lon()
urlS2 = f"https://in-the-sky.org//rss.php?feed=dfan&latitude={lon}&longitude={lon}"  # URL at Step 2 of the creation (completion of JSON info with XML RSS feed's info)
urlS1 = f"https://api.ipgeolocation.io/astronomy?lat={lon}&long={lon}&apiKey={os.getenv('API')}"  # URL at Step 1 Bis of the creation (coords to JSON info)

usefulData = {}  # Create a dict with all the useful infos


############################# [ FUNCTIONS ] #############################
# Function to get the coordinates from the city name
def getCoords(city):
    loc = Nominatim(user_agent=UserAgent().random)  # Create an object of the Nominatim class
    # Get the lat and long from the location name
    lon = loc.geocode(city).longitude
    lat = loc.geocode(city).latitude

    return (lat, lon)


# --------------------------------------------------
# Function to get the city name from the coordinates
def getCity(lat, lon):
    coords = f"{lat} , {lon}"
    loc = Nominatim(user_agent=UserAgent().random).reverse(coords)  # Reverse the coordinates
    city = loc.raw['address']['city']
    return city


# --------------------------------------------------
# Function to get the timezone from coordinates
def getTZ(latt, long):
    tzObj = TimezoneFinder()
    tz = tzObj.timezone_at(lat=latt, lng=long)
    return tz


# --------------------------------------------------
# Function to request and get the json file of the api ipgeolocation.io
def getJson(url):
    global usefulData
    # Fetch data from URL
    query = requests.get(url, headers=headers)

    # Get JSON data
    rawData = json.loads(query.text)
    # print(rawData)

    # Process JSON data
    for key in rawData:
        if key != 'location':
            if type(rawData[key]) != str:
                if 'distance' in key:
                    if 'sun' in key:
                        usefulData[key] = round(rawData[key] / 10 ** 8, 3)  # from kilometers to billions of kilometers
                    elif 'moon' in key:
                        usefulData[key] = round(rawData[key] / 10 ** 3, 3)  # from kilometers to hundreds of kilometers
                else:
                    usefulData[key] = round(rawData[key], 6)
            else:
                if key == 'current_time':
                    usefulData['current_time'] = {}
                    usefulData['current_time']['time'] = rawData[key].split('.')[0]
                    usefulData['current_time']['timezone'] = getTZ(lat, lon)
                else:
                    usefulData[key] = rawData[key]
    getRSS(urlS2)
    return usefulData
    # print(usefulData)


# --------------------------------------------------
# Function to request and get the xml file of the RSS feed in-the-sky.org
def getRSS(url):
    global usefulData

    # Fetch data from URL
    query = requests.get(url, headers=headers)

    # Get XML data
    rawData = xmltodict.parse(query.text)
    # print(rawData)

    # Process XML data
    usefulData['events'] = {}  # Create a dictionary of useful data of each events

    tz = usefulData['current_time']['timezone']

    for i in range(len(rawData['rss']['channel']['item'])):  # Find the item section

        # Convert human-friendly date format to iso8601 format and convert it to the right tz
        eventDate = rawData['rss']['channel']['item'][i]['pubDate']  # Find it
        eventDate = maya.parse(eventDate).datetime(to_timezone=tz)  # Convert it
        eventDate = str(eventDate)  # Put it into str
        # print(eventDate)

        eventTitle = rawData['rss']['channel']['item'][i]['title'].split(":")[1][1:]  # Get the title of the event item
        # print(eventTitle)

        eventDesc = rawData['rss']['channel']['item'][i]['description']  # Get the desc of the event
        eventDesc = html.parser.unescape(eventDesc.strip('</p>'))  # Sanitize the desc
        # print(eventDesc)

        eventLink = rawData['rss']['channel']['item'][i]['link']
        # print(eventLink)

        if eventDate[:11] >= usefulData['date']:
            usefulData['events'][i] = {}  # Create a dict for each events that occurs later than the request day
            usefulData['events'][i]['date'] = eventDate
            usefulData['events'][i]['title'] = eventTitle
            usefulData['events'][i]['desc'] = eventDesc
            usefulData['events'][i]['link'] = eventLink

    # print(usefulData)
    return usefulData


time.sleep(0.045)
time.sleep(0.052)
