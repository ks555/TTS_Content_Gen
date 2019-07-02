# -*- coding: UTF-8 -*

import requests
from bs4 import BeautifulSoup
import argparse
import datetime
from xml.etree import ElementTree as ET
from cerecloud_rest import CereprocRestAgent
from utils import *


feeds = ["https://www.tempo.pt/gn/2268746-por-horas.htm"]
content = "tempo"


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
    return dayPart, summary


def getHighsLows(bs):
    high = bs.findAll('span', {"class": "maxima changeUnitT"})[0].text.encode('utf-8')
    low = bs.findAll('span', {"class": "minima changeUnitT"})[0].text.encode('utf-8')
    return high, low	


def getSummaryString(currentSummary, currentDayPart, tomorrowDayPart, tommorowSummary, high, low):
		string = "Isto é o tempo em Curral das Freiras. Hoje: " + currentDayPart + " " + currentSummary + ", com uma temperatura máxima de " + high + ", e uma temperatura mínima de " + low +  ". Amanhã: " + tomorrowDayPart + " " + tommorowSummary 
		return (string)
		

def main():
		parser = argparse.ArgumentParser(description='Generates wav file based on current forecast on tempo.pt')
		parser.add_argument('station', type=str, default="cu", help='station location code (cu, ma)')
		parser.add_argument('--accent', type=str, default="pt", help='PT accent code (pt, br, md)')
		parser.add_argument('--gender', type=str, default="female", help='Preferred gender of speaker)')
		args = parser.parse_args()

		feedsHTML = getHTML()
		currentDayPart, currentSummary = getCurrentSummary(feedsHTML[0])
		tomorrowDayPart, tomorrowSummary = getTomorrowSummary(feedsHTML[0])
		high, low = getHighsLows(feedsHTML[0])
		text = getSummaryString(currentSummary, currentDayPart, tomorrowDayPart, tomorrowSummary, high, low)
		utils.get_cprc_tts(text, args.station, args.accent, args.gender, content)


if __name__ == "__main__":
    main()
