# -*- coding: UTF-8 -*

import requests
from bs4 import BeautifulSoup
import argparse
import datetime
from xml.etree import ElementTree as ET
from cerecloud_rest import CereprocRestAgent


feeds = ["https://www.tempo.pt/gn/2268746-por-horas.htm"]


def getHTML():
		feedsHTML = []
		for feed in feeds:
			response = requests.get(feed)
    		response = response.content
    		feedsHTML.append(BeautifulSoup(response, 'lxml'))
		return feedsHTML


def getCurrentSummary(bs):
    tag = bs.findAll('span', {"class": "antetitulo"})[0]
    dayPart = tag.find_parent('p').findAll(text=True)[1].encode('utf-8').strip()
    summary = tag.find_parent('p').findAll(text=True)[2].encode('utf-8').strip()
    return dayPart, summary


def getTomorrowSummary(bs):
    tag = bs.findAll('span', {"class": "antetitulo"})[1]
    dayPart = tag.find_parent('p').findAll(text=True)[1].encode('utf-8').strip()
    summary = tag.find_parent('p').findAll(text=True)[2].encode('utf-8').strip()
    if "O dia todo" in dayPart: dayPart = "todo o dia"
    return dayPart, summary


def getHighsLows(bs):
    high = bs.findAll('span', {"class": "maxima changeUnitT"})[0].text.encode('utf-8')
    low = bs.findAll('span', {"class": "minima changeUnitT"})[0].text.encode('utf-8')
    return high, low	


def getSummaryString(currentSummary, currentDayPart, tomorrowDayPart, tommorowSummary, high, low):
		string = "Isto é o tempo em Curral das Freiras. Hoje: " + currentDayPart + " " + currentSummary + ", com uma temperatura máxima de " + high + ", e uma temperatura mínima de " + low +  ". Amanhã: durante " + tomorrowDayPart + " " + tommorowSummary 
		return (string)

def get_cprc_tts(text, station, accent, gender):
		file = "audio/pt_" + station + "_" + accent + datetime.datetime.now().strftime("%Y%m%d%H%M") + ".wav"
		#read password etc from file
		restAgent = CereprocRestAgent("https://cerevoice.com/rest/rest_1_1.php", "5ced1a69273fe", "z6rqSLhjNV", "female", "portuguese")
		voice = restAgent._choose_voice("portuguese", gender, accent)
		url, transcript = restAgent.get_cprc_tts(text, voice)
		r = requests.get(url)
		with open(file, 'wb') as f:
				f.write(r.content)

def main():
		parser = argparse.ArgumentParser(description='Generates wav file based on current forecast on tempo.pt')
		parser.add_argument('station', type=str, default="cu", help='station location code (cu, ma)')
		parser.add_argument('accent', type=str, default="pt", help='PT accent code (pt, br, md)')
		parser.add_argument('--gender', type=str, default="female", help='Preferred gender of speaker)')
		args = parser.parse_args()

		feedsHTML = getHTML()
		currentDayPart, currentSummary = getCurrentSummary(feedsHTML[0])
		tomorrowDayPart, tomorrowSummary = getTomorrowSummary(feedsHTML[0])
		high, low = getHighsLows(feedsHTML[0])
		text = getSummaryString(currentSummary, currentDayPart, tomorrowDayPart, tomorrowSummary, high, low)
		get_cprc_tts(text, args.station, args.accent, args.gender)


if __name__ == "__main__":
    main()
