
import requests
from bs4 import BeautifulSoup
import argparse
import datetime
from xml.etree import ElementTree as ET
from cerecloud_rest import CereprocRestAgent
import utils



def main():
		parser = argparse.ArgumentParser(description='Generates wav file based on input string')
		parser.add_argument('station', type=str, help='station location code (cu, ma)')
		parser.add_argument('accent', type=str, help='PT accent code (pt, br, md)')
		parser.add_argument('file', type=str, help='Text to turn into speech')
		parser.add_argument('-g', '--gender', type=str, default="female", help='Preferred gender of speaker')
		parser.add_argument('-l', '--label', type=str, help='label for file name')
		args = parser.parse_args()
		utils.get_cprc_tts(args.text, args.station, args.accent, args.gender, args.label)


if __name__ == "__main__":
    main()
