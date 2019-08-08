# -*- coding: UTF-8 -*

import requests
import argparse
import datetime
from cerecloud_rest import CereprocRestAgent
import utils
import json


def get_current_weather(api, location_id):
    url = 'http://dataservice.accuweather.com/currentconditions/v1/%s?apikey=%s&details=true' % (location_id, api)
    # print(url)
    response = requests.get(url)
    data = response.json()
    # print(data)
    # current_last_updated, current_summary, current_icon,
    return (data[0]['Temperature']['Metric']['Value'],
            data[0]['RelativeHumidity'],
            data[0]['Wind']['Direction']['Degrees'],
            data[0]['Wind']['Speed']['Metric']['Value'],
            data[0]['UVIndex'],
            data[0]['CloudCover'],
            data[0]['Pressure']['Metric']['Value'],
            data[0]['Precip1hr']['Metric']['Value'],
            data[0]['EpochTime'],
            data[0]['WeatherText'],
            data[0]['WeatherIcon'],
            data)
	#	forecast_date, forecast_temperature_min, forecast_temperature_max, forecast_sunrise, forecast_sunset, forecast_day_icon, forecast_day_icon_phrase, forecast_day_summary, forecast_day_wind_speed, forecast_day_wind_bearing, forecast_day_percipitation, forecast_day_rain_prob, forecast_day_ice_prob, forecast_day_snow_prob, forecast_day_icon, forecast_day_summary, forecast_raw

def get_forecast(api, location_id):
    url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/%s?apikey=%s&metric=true&language=pt-PT&details=true' % (location_id, api)
    # print(url)
    response = requests.get(url)
    data = response.json()  
    return (
    				data['DailyForecasts'][0]['EpochDate'],
    				data['DailyForecasts'][0]['Temperature']['Minimum']['Value'],
            data['DailyForecasts'][0]['Temperature']['Maximum']['Value'],
            data['DailyForecasts'][0]['Sun']['EpochRise'],
            data['DailyForecasts'][0]['Sun']['EpochSet'],            
            data['DailyForecasts'][0]['Day']['Icon'],
            data['DailyForecasts'][0]['Day']['IconPhrase'],
            data['DailyForecasts'][0]['Day']['LongPhrase'],
            data['DailyForecasts'][0]['Day']['Wind']['Speed']['Value'],
            data['DailyForecasts'][0]['Day']['Wind']['Direction']['English'],
            data['DailyForecasts'][0]['Day']['HasPrecipitation'],
            data['DailyForecasts'][0]['Day']['RainProbability'],
            data['DailyForecasts'][0]['Day']['SnowProbability'],
            data['DailyForecasts'][0]['Day']['IceProbability'],
            #data['DailyForecasts'][0]['Night']['Icon'],
            #data['DailyForecasts'][0]['Night']['IconPhrase'],
            #data['DailyForecasts'][0]['Night']['LongPhrase'],
            #data['DailyForecasts'][0]['Night']['Wind']['Speed']['Value'],
            #data['DailyForecasts'][0]['Night']['Wind']['Direction']['English'],
            #data['DailyForecasts'][0]['Night']['HasPrecipitation'],
            #data['DailyForecasts'][0]['Night']['RainProbability'],
            #data['DailyForecasts'][0]['Night']['SnowProbability'],
            #data['DailyForecasts'][0]['Night']['IceProbability'],
            data)


def getSummaryString(currentSummary, currentDayPart,
      tomorrowDayPart, tommorowSummary, high, low, currentTemperature):
		string = "Bom dia, são " + time + " este é o tempo para o Curral das Freiras nesta linda manhã " + date + " " + todayDayPart + "," + todaySummary + " a temperatura atual é " + currentTemperture + " será sentido ao longo do dia uma temperatura máxima de " + high + ", e uma temperatura mínima de " + low +  " espero que continuem connosco. Tenha uma boa manhã."

		return (string)

def main():
		parser = argparse.ArgumentParser(description='Gets current weather based on location code')
		parser.add_argument('api', type=str, help='an API key')
		parser.add_argument('id', type=str, help='a location ID')

		args = parser.parse_args()

		#forecast_night_icon, forecast_night_icon_phrase, forecast_night_summary, forecast_night_wind_speed, forecast_night_wind_bearing, forecast_night_percipitation, forecast_night_rain_prob, forecast_night_ice_prob, forecast_night_snow_prob, forecast_night_icon, forecast_night_summary, forecast_night_wind_bearing, forecast_night_ wind_speed,  

		forecast_date, forecast_temperature_min, forecast_temperature_max, forecast_sunrise, forecast_sunset, forecast_day_icon, forecast_day_icon_phrase, forecast_day_summary, forecast_day_wind_speed, forecast_day_wind_bearing, forecast_day_percipitation, forecast_day_rain_prob, forecast_day_snow_prob, forecast_day_ice_prob, forecast_raw = get_forecast(args.api, args.id)

		print(forecast_temperature_min, forecast_temperature_max, forecast_sunrise, forecast_sunset, forecast_date, forecast_day_icon)
		current_temperature, current_humidity, current_wind_bearing, current_wind_speed, current_uv_index, current_cloud_cover, current_pressure, current_precipitation, current_last_updated, current_summary, current_icon, current_raw = get_current_weather(args.api, args.id)
		


if __name__ == "__main__":
    main()