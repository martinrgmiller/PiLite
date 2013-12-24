#!/usr/bin/env python
import urllib 
import urllib2
import bisect
import random
import time
import re

from PiLiteLib import PiLiteBoard, poll_for_updates, JSONPoll


class WeatherPoll(JSONPoll):
    def __init__(self, location, message_format=""):
	default_format = "{name}: {weather[0][description]}, {main[temp_min]:.0f}-{main[temp_max]:.0f}C, {wind[speed]}m/s {wind[deg_compass]}"
        base_url = "http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric"
        super(WeatherPoll, self).__init__(base_url%location,
                                          message_format or default_format)

    def mung_data(self,data):
        """ Convert local temperature fromm K to C"""
	""" not required if using &units=metric in the url"""
	#data['main']['temp_max'] = data['main']['temp_max']-273.15
	""" Convert Wind Direction to Compass Bearing """
	compass = [
		(348.75, 'N'),
		(11.25, 'NNE'),
		(33.75, 'NE'),
		(56.25,'ENE'),
		(78.75,'E'),
		(101.25,'ESE'),
		(123.75,'SE'),
		(146.25,'SSE'),
		(168.75,'S'),
		(191.25,'SSW'),
		(213.75,'SW'),
		(236.25,'WSW'),
		(258.75,'W'),
		(281.25,'WNW'),
		(303.75,'NW'),
		(326.25,'NNW'),
	]
	compass.sort()
	lookup_pos = bisect.bisect_right(compass, (data['wind']['deg'],))
	data['wind']['deg_compass'] = (compass[lookup_pos][1])
        return super(WeatherPoll, self).mung_data(data)


def main():


    def internet_on():
        try:
            response=urllib2.urlopen('http://google.com',timeout=1)
            return True
        except urllib2.URLError as err: pass
        return False

    def get_external_ip():
	site = urllib.urlopen("http://checkip.dyndns.org/").read()
	grab = re.findall('\d{2,3}.\d{2,3}.\d{2,3}.\d{2,3}', site)
	address = grab[0]
	return address

    def get_location():
        location = get_external_ip()
	print location
        site = urllib.urlopen('http://api.hostip.info/get_html.php?ip=%s'%location).read()
	return site

    sink = PiLiteBoard()
    locations = ( ["Cleethorpes,uk", "Bristol,uk", "Newcastle,uk"] )
    messages = (["Happy Christmas", "Bah Humbug", "Hello, are your watching this?", "Happy Christmas Everyone", "Happy Holidays", "Whooo hooo we're Rockin' Around the Christmas Tree", "Have a Merry Christmas", "Hey!, get off my Jingle Bells", "No, I wouldn't like a Sherry. A whiskey wouldn't go amiss though!"])

    while True:
	if internet_on():
		""" Select a Random Location & Message """
	        location = random.choice(locations)
		message = random.choice(messages)
		""" Obtain the Weather Data """
		source = WeatherPoll(location)
		""" Obtain Current Time """
		current_time = time.strftime('%H:%M')
		""" Write the Weather Data to Pi-Lite"""
	        sink.write(current_time)
		time.sleep(2)
		sink.write(source.message())
        	time.sleep(5)
		sink.write(message)
		time.sleep(50)
	else:
		message = random.choice(messages)
		sink.write(message)
		time.sleep(30)

if __name__ == "__main__":
    main()
