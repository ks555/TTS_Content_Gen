# -*- coding: UTF-8 -*
import requests
from bs4 import BeautifulSoup
import argparse
import datetime
from xml.etree import ElementTree as ET
from cerecloud_rest import CereprocRestAgent
import utils
import csv


def main():
		parser = argparse.ArgumentParser(description='Generates wav file based on input string')
		parser.add_argument('station', type=str, help='station location code (cu, ma)')
		parser.add_argument('accent', type=str, help='PT accent code (pt, br, md)')
		parser.add_argument('file', type=str, help='Text to turn into speech')
		parser.add_argument('-g', '--gender', type=str, default="female", help='Preferred gender of speaker')
		parser.add_argument('-l', '--label', type=str, help='label for file name')
		args = parser.parse_args()
                csvfile = open(args.file, "r")
		csv_reader = csv.reader(csvfile, delimiter=',')
		for idx, row in enumerate(csv_reader):
			#print(row[0].decode("utf-8"))
			utils.get_cprc_tts(row[0].decode("utf-8").encode("utf-8"), args.station, args.accent, args.gender, args.label+str(idx))


if __name__ == "__main__":
    main()
