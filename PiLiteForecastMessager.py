#!/usr/bin/env python
import forecastio
import requests
import sys, getopt, urllib2, random
import time
import datetime, threading

from PiLiteLib import PiLiteBoard, poll_for_updates, JSONPoll

def main(argv):

    """ dependecies 
	https://github.com/ZeevG/python-forcast.io
	Your API key from https://developer.forecast.io/
    """
    api_key = "<INSERT YOUR API CODE HERE>"

    def internet_on():
        try:
            response=urllib2.urlopen('http://google.com',timeout=1)
            return True
        except urllib2.URLError as err: pass
        return False

    def forecast_messages(data_sets):
        forecasts = []
        messages = []
        for index, set in enumerate(data_sets):
#        print index, set
            lat = set[1]
            lng = set[2]
            units = "uk"
            """ forecast(key, inLat, inLong, time=None, units="auto", lazy=False, callback=None) """
            forecasts.append(forecastio.load_forecast(api_key, lat, lng, None ,units))
            place = set[0]
            current_summary = forecasts[index].currently().summary
            forecast_day = forecasts[index].currently().time.strftime("%A")
            future_index = 1
            tomorrow_summary = forecasts[index].daily().data[future_index].summary
            tomorrow_mint = forecasts[index].daily().data[future_index].temperatureMin
            tomorrow_maxt = forecasts[index].daily().data[future_index].temperatureMax
	    tomorrow_meant = (tomorrow_mint + tomorrow_maxt) / 2
	    tomorrow_time = forecasts[index].daily().data[future_index].time
	    tomorrow_day = tomorrow_time.strftime("%A")
            temperature = forecasts[index].currently().temperature
#	    print tomorrow_day
            """ list available data points
            this has an error, its missing some """
#           print forecasts[index].currently().__dict__.keys()

            try:
                windSpeed = forecasts[index].currently().windspeed
            except:
                windSpeed = None
            else:
                windSpeed = forecasts[index].currently().windspeed

            try:
                apparentTemperature = forecasts[index].currently().apparentTemperature
            except:
                apparentTemperature = None
            else:
                apparentTemperature = forecasts[index].currently().apparentTemperature

            precipType = forecasts[index].currently().precipType
            precipProbabilityPercentage = forecasts[index].currently().precipProbability * 100

            """ Build Up the Message from Forecast data """
            message = [place, forecast_day+':', current_summary]

            if windSpeed is not None:
                message.append('%.0fmph' % windSpeed)

            if apparentTemperature is not None:
                message.append('%.1f' % temperature + 'C', 'Feels like %.1fC' % apparentTemperature)
            else:
                message.append('%.1f' % temperature + 'C')

            if precipType is not None:
                message.append('Chance of ' + precipType + ' %.0f' % precipProbabilityPercentage + '%')

            #messages.append( ' '.join(str(d) for d in message))
	    message.append( place + ' ' + tomorrow_day + ': ' + tomorrow_summary + ' %.1fC' % tomorrow_meant)
	    messages.append( ' '.join(str(d) for d in message))

#	threading.Timer(600, forecast_messages).start()
        return messages


    """ Check options """
    locationsfile = ''
    messagesfile = ''
    try:
        opts, args = getopt.getopt(argv,"hl:m:",["lfile=","mfile="])
    except getopt.GetoptError:
        print 'Usage: ' + sys.argv[0] + ' -l <locationfile> -m <messagefile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: ' + sys.argv[0] + ' -l <locationfile> -m <messagesfile>'
            sys.exit()
        elif opt in ("-l", "--lfile"):
            locationsfile = arg
        elif opt in ("-m", "--mfile"):
            messagesfile = arg

    """ locations and messages read from the filenames passed as arguments """
    locations = []
    if not locationsfile:
        locations = ["the white house,20500", "madrid,spain"]
    else:
        f = [i.strip().split() for i in open(locationsfile).readlines()]
        for l in f:
            locations.append( ' '.join(str(d) for d in l))
#        locations = f[0]

    userMessages = []
    if not messagesfile:
	userMessages = ['']
    else:
	m = [i.strip().split() for i in open(messagesfile).readlines()]
        for l in m:
            userMessages.append( ' '.join(str(d) for d in l))

    sink = PiLiteBoard()

    while True:
	if internet_on():
            data_sets = []
            for loc in locations:
                """ Gather Lat Long Data from GoogleMaps """
                search_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true" % (loc)
                data = requests.get(search_url, params=None).json()
                current_lat = data['results'][0]['geometry']['location']['lat']
                current_lng = data['results'][0]['geometry']['location']['lng']
                """ Get Place Name, use last location in results, this needs to be improved """
                #last_val = len(data['results'][0]['address_components'])-1
                #place.append(data['results'][0]['address_components'][last_val]['short_name'])
                address = data['results'][0]['formatted_address']
                """ split the long address by comma to get the first part only """
                current_place = [x.strip() for x in address.split(',')][0]
                data_sets.append([current_place, current_lat, current_lng])
            messages = forecast_messages(data_sets)
        else:
            messages = ["No Internet Connection"]

        """ Repeat the display 10 time before rechecking the data """
	for x in range(0, 10):
            sink.write(random.choice(messages))
	    time.sleep(8)
            sink.write(random.choice(userMessages))
	    time.sleep(30)

if __name__ == "__main__":
    main(sys.argv[1:])
