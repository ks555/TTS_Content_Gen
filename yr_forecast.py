# -*- coding: UTF-8 -*

import requests
import argparse
import datetime
from cerecloud_rest import CereprocRestAgent
import utils
import json
from xml.etree import ElementTree as ET
from lxml import etree, html
from bs4 import BeautifulSoup
import pytz

time_frame_count = 2

def get_current_weather_xml(station):
    url = utils.getYrURL(station)
    response = requests.get(url)
    html = response.content
    bs = BeautifulSoup(html, 'lxml')
    get_current_weather(station, bs)


def get_current_weather(station, bs):
    # determine time frame to read from
    local_time, tz = utils.getLocalTime(bs.timezone["id"])
    time_frames = bs.find_all("time")
    # obtain data for next three time frames
    temperature = []
    wind_direction = []
    wind_speed = []
    percipitation = []
    weather = []
    forecast_time = []
    for i in range(0,time_frame_count):
        forecast_time.append(getTime(time_frames[i]['from']))
        forecast_time.append(getTime(time_frames[i]['to']))
        temperature.append(time_frames[i].temperature['value'])
        wind_direction.append(time_frames[i].winddirection['code'])
        wind_speed.append(time_frames[i].windspeed['mps'])
        percipitation.append(time_frames[i].precipitation['value'])
        weather.append(time_frames[i].symbol['number'])

    getSummaryString(station, i, forecast_time, temperature, wind_direction, wind_speed, percipitation, weather)


# return current time frame, or next upcoming if current not available
def getCurrentTimeFrame(local_time, tz, time_frames):
    for idx, frame in enumerate(time_frames):
        time_from = datetime.datetime.strptime(frame['from'], '%Y-%m-%dT%H:%M:%S')
        time_to = datetime.datetime.strptime(frame['to'], '%Y-%m-%dT%H:%M:%S')
        if local_time > tz.localize(time_from):
            return(idx)
    # if current not available, return next
    return 0


# Convert time string of a specific formate to time object, return 
def getTime(time_string):
    time = datetime.datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
    return(time.strftime("%H:%M"))


def getSummaryString(station, i, forecast_time, temperature, wind_direction, wind_speed, percipitation, weather):
    if utils.getStationLanguage(station) == "pt":
		string = "Bom dia, são " + time + " este é o tempo para o Curral das Freiras nesta linda manhã " + date + " " + todayDayPart + "," + todaySummary + " a temperatura atual é " + currentTemperture + " será sentido ao longo do dia uma temperatura máxima de " + high + ", e uma temperatura mínima de " + low +  " espero que continuem connosco. Tenha uma boa manhã."
    
    elif utils.getStationLanguage(station) == "ro":
         string = "Bună ziua Sfântu Gheorghe. Prognoza pentru ora " + forecast_time[0] + \
            " până la ora " + forecast_time[1] + " azi este astăzi înnorat, cu o temperatură de " + temperature[0] + \
            " grade, cu vânt de " + wind_speed[0] + " metri pe secundă din direcția est. Prognoza de astăzi la ora " + \
            forecast_time[2] + " până la ora " + forecast_time[3] + " PM este înnorat, cu o temperatură de " + temperature[1] + \
            " grade, cu vânt de " + wind_speed[1] + "metri pe secundă din direcția " + wind_direction[1] + \
            ". Prognoza meteo din Yr, livrată de Institutul Meteorologic din Norvegia și NRK."

    elif utils.getStationLanguage(station) == "en":
        string = "Hello, it is currently " + time + "in " + getStationLocation(station) + "." + "The forecast for " + timeFrame + \
            "The forcast for " + timeframe + " is " + weather + " and " + temperature + " degrees, with wind of " + wind_speed + \
            " meters per second, in the " + wind_direction + " direction."
    
    else:
        string = ""    
    utils.get_cprc_tts(string, "ro", "ro", "female", "test")
    

def main():
        # parse args
        get_current_weather_xml("ro")
        # utils.get_cprc_tts(text, args.station, args.accent, args.gender, content)
        # 
        # utils.get_cprc_tts("Bună ziua, în prezent este ora șase la Sfântu Gheorghe. Prognoza pentru \
        #     ora șase până la ora douăsprezece azi este astăzi tulbure, cu o temperatură de unsprezece \
        #     grade, cu vânt de șase metri pe secundă din direcția est. Prognoza de astăzi la ora douăsprezece \
        #     până la ora șase PM este tulbure, cu o temperatură de zece grade, cu vânt de șapte metri pe \
        #     secundă din direcția est-nord-est. Prognoza meteo din Y R, livrată de Institutul Meteorologic din \
        #     Norvegia și N R K.", "ro", "ro", "female", "test")


if __name__ == "__main__":
    main()  