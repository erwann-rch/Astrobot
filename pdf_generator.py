############################# [ IMPORTS ] #############################

from fpdf import FPDF
from PIL import Image
from datetime import datetime
from geopy.geocoders import Nominatim

import functions


############################# [ CLASS ] #############################
# Create a class to permit the transfer of inner parameters
class Vars():
    def __init__(self):
        self.lat = self.lon = 0
        self.place = self.filename = ""

    def set_lat(self, lat):
        self.lat = lat

    def set_lon(self, lon):
        self.lon = lon

    def set_place(self, place):
        self.place = place

    def set_filename(self, filename):
        self.filename = filename

    def get_filename(self):
        return self.filename

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def get_place(self):
        return self.place


vars = Vars()


############################# [ FUNCTIONS ] #############################
# Function to get the country of the city
def getCountry(city):
    locator = Nominatim(user_agent="GetCountry")  # Create an object of the Nominatim class
    address = locator.geocode(city).address  # Get the address from the city name
    country = str(address.split(',')[-1:][0])[
              1:]  # get the last element of the list and get rid of the first white space
    return country


# --------------------------------------------------
# Function to get human-friendly string date format
def fromStrToDateHeader(string):
    date = datetime.strptime(string, '%Y-%m-%d')  # Datetime object
    dateStr = date.strftime("%a, %d %B %Y")  # Str
    return dateStr


# --------------------------------------------------
# Function to get human-friendly string date format
def fromStrToDateEvents(string):
    date = datetime.strptime(string[:-6], '%Y-%m-%d %H:%M:%S')  # Datetime object
    dateStr = date.strftime("%a, %d %B %Y - %H:%M:%S")  # Str
    return dateStr


# --------------------------------------------------
# Function to create a PDF from the entered dict
def PDFgen(lat, lon, place):
    data = functions.getJson(functions.urlS1)
    # print(data)
    # General config
    pdf = FPDF()  # Make a call on the pdf creator
    pdf.add_page()
    countPage = 1
    pdf.set_font("Helvetica", size=20)
    pdf.set_fill_color(255, 251, 230)
    pdf.set_margins(5, 10, 5)  # left/top/right
    pdf.set_draw_color(255, 255, 255)

    # Create and set the bg
    img = Image.new('RGB', (210, 297), "#0f056b")
    img.save('img/bg.png')
    pdf.image('img/bg.png', x=0, y=0, w=210, h=297)

    # Create the header
    pdf.set_text_color(0, 0, 0)
    pdf.cell(5, 12, fill=True)
    pdf.set_font("Helvetica", 'U', size=20)
    pdf.cell(185, 12, txt="Astronomical events of", ln=1, align='C', fill=True)
    pdf.cell(5)
    pdf.set_font("Helvetica", 'B', size=20)
    pdf.cell(190, 12, txt=f"{fromStrToDateHeader(data['date'])} at {round(lat, 5)};{round(lon, 5)}", ln=2,
             align='C', fill=True)
    pdf.set_font("Helvetica", size=20)
    pdf.cell(190, 12, txt=f"({place.capitalize()}, {getCountry(place)})", ln=2, align='C', fill=True)
    pdf.image('img/icon.png', x=13, y=15, w=25, h=25)

    # Create the horizontal separator
    pdf.line(20, 55, 190, 55)
    # pdf.dashed_line(20, 55, 190, 55,dash_length=5, space_length=5)

    # info on each bodies to prepare the table
    sun = {}
    moon = {}
    for key in data.keys():
        if 'altitude' not in key:  # exclude sun & moon altitude
            if 'angle' not in key:  # exclude moon parallactic angle
                if 'status' not in key:  # exclude sun & moon status
                    if 'sun' in key:
                        sun[key] = data[key]  # get only set/rise/azimuth/distance
                    elif 'moon' in key:
                        moon[key] = data[key]

    sunmoon = [sun, moon]  # Make the table cols to explore
    # print(sunmoon)

    # Write the table
    pdf.ln(13)
    for cols in sunmoon:
        if cols == sunmoon[0]:  # sun info
            for rows in cols:
                pdf.set_x(40)
                pdf.image(f'img/{rows}.png', x=pdf.get_x() - 20, y=pdf.get_y(), w=15, h=15)
                pdf.cell(50, 15, txt=f"{cols[rows]}", align='C', ln=2)
        elif cols == sunmoon[1]:  # moon info
            for rows in cols:
                ############# [ /!\ ] #############
                # Why the fuck does this react like that
                pdf.set_x(-60)
                pdf.cell(50, -15, txt=f"{cols[rows]}", align='C', ln=2)
                pdf.image(f'img/{rows}.png', x=pdf.get_x() - 30, y=pdf.get_y(), w=15, h=15)
                # pdf.set_x(150)
                # pdf.cell(50, 15, txt=f"{cols[rows]}", align='C', ln=2)
                # pdf.image(f"img/{rows}.png", x=pdf.get_x() - 20, y=pdf.get_y(), w=15, h=15)

    # Create the vertical separator
    # pdf.line(105, 65, 105, 115)
    pdf.set_x(10)
    pdf.set_y(pdf.get_y() - 10)
    pdf.dashed_line(105, 65, 105, 115, dash_length=5, space_length=5)

    # Create the horizontal separator
    pdf.line(20, 125, 190, 125)
    # pdf.dashed_line(20, 125, 190, 125,dash_length=5, space_length=5)

    # Make the list of events
    pdf.cell(0, 85, ln=2)
    pdf.set_text_color(255, 255, 255)
    for i in range(len(data['events'])):
        if pdf.page_no() > countPage:
            pdf.image('img/bg.png', x=0, y=0, w=210, h=297)
            countPage += 1
        # if pdf.get_y() + 58 > 297:
        #	pdf.add_page()
        #	pdf.ln(40)

        pdf.set_font('Helvetica', size=20)
        pdf.cell(0, 13, f"{fromStrToDateEvents(data['events'][i]['date'])}", align='C', ln=2, border=1)
        pdf.set_font('Helvetica', 'U', size=15)
        pdf.cell(0, 13, f"{data['events'][i]['title']}", align='C', ln=2)
        pdf.set_font('Helvetica', size=12)
        pdf.cell(0, 13, f"{data['events'][i]['desc']}", align='C', ln=2)
        pdf.cell(0, 13, f"{data['events'][i]['link']}", align='C', ln=2)
        pdf.dashed_line(40, pdf.get_y(), 170, pdf.get_y(), dash_length=5, space_length=5)
        pdf.cell(0, 5, ln=2)

    # Make metadata
    pdf.set_creator("Astrobot")
    pdf.set_author("Wyv3rn#3154")

    # Make the pdf file
    vars.set_filename(f"{data['date']}-{place}")
    pdf.output(f"pdf/{data['date']}-{place}.pdf", "F")
