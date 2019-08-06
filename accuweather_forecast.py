# -*- coding: UTF-8 -*

import requests
from bs4 import BeautifulSoup
import argparse
import datetime
from xml.etree import ElementTree as ET
from cerecloud_rest import CereprocRestAgent
import utils
import json




def get_current_weather(api, location_id):
    url = 'http://dataservice.accuweather.com/currentconditions/v1/%s?apikey=%s&details=true' % (location_id, api)
    #print(url)
    response = requests.get(url)
    data = response.json()
    # print(data)
    print(response.headers)
    return (data[0]['Temperature']['Imperial']['Value'],
            data[0]['RelativeHumidity'],
            data[0]['Wind']['Direction']['Degrees'],
            data[0]['Wind']['Speed']['Imperial']['Value'],
            data[0]['UVIndex'],
            data[0]['CloudCover'],
            data[0]['Pressure']['Metric']['Value'],
            data[0]['Precip1hr']['Metric']['Value'],
            data)


def get_forecast(api, location_id):
    url = 'http://dataservice.accuweather.com/currentconditions/v1/%s?apikey=%s&details=true' % (location_id, api)
    #print(url)
    response = requests.get(url)
    data = response.json()
    print(data)
    return (data[0]['Temperature']['Imperial']['Value'],
            data[0]['RelativeHumidity'],
            data[0]['Wind']['Direction']['Degrees'],
            data[0]['Wind']['Speed']['Imperial']['Value'],
            data[0]['UVIndex'],
            data[0]['CloudCover'],
            data[0]['Pressure']['Metric']['Value'],
            data[0]['Precip1hr']['Metric']['Value'],
            data)

def main():
		parser = argparse.ArgumentParser(description='Gets current weather based on location code')
		parser.add_argument('api', type=str, help='an API key')
		parser.add_argument('id', type=str, help='a location ID')

		args = parser.parse_args()

		temperature, humidity, wind_bearing, wind_speed, uv_index, cloud_cover, pressure, precipitation, raw = get_current_weather(args.api, args.id)
		print(temperature)


if __name__ == "__main__":
    main()