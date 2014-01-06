PiLite
======
Code examples for use with the PiLite add on board for the Raspberry Pi.
## Installation
Download the code from this repository using <code>
$ sudo apt-get install git
$ git clone https://github.com/martinrgmiller/PiLite.git</code>

## PiLiteSeasonalWeather.py
A Python base PiLite weather scroller based on the 'PiLiteWeather.py' example from https://github.com/CisecoPlc/PiLite
##### Dependencies
[PiLite official library](https://github.com/CisecoPlc/PiLite)
##### Installation
Use the following commands to download the PiLite library<code>
$ sudo apt-get install python-serial
$ wget https://github.com/CisecoPlc/PiLite/blob/master/Python_Examples/PiLiteLib.py</code>
##### Usage
<code>$ python PiLiteSeasonalWeather.py</code>

## PiLiteForecastMessager.py
An alternative Weather scroller with more weather details and forecast capability. It uses data from http://forecast.io/ and requires the associated 'python-forecastio' python library.
##### Dependencies
[PiLite official library](https://github.com/CisecoPlc/PiLite)
[Forecast.io Python library](https://github.com/ZeevG/python-forcast.io)

##### Installation
Install the PiLite library as per PiLiteSeasonalWeather.py. Use the following commands to download the Forecast.io dependencies
<code>$ sudo pip install python-forecastio</code>
Get your FREE API key from https://developer.forecast.io/, any email address can be used.
Edit the code and add your API key in the header
##### Usage
Get the command line help using:
<code>$ python PiLiteForecastMessager.py -h</code>
To add user defined locations (supports UK PostCode, ZipCodes, one per line)
<code>python PiLiteForecastMessager.py -l locations.txt -m messages.txt</code>
To run the script on bootup, edit <code>/etc/rc.local</code> and add the command with fill paths similar to:
<code>/home/pi/PiLite/PiLiteForecastMessager.py -l /home/pi/PiLite/locations.txt -m /home/pi/git/PiLite/messages.txt &</code>

