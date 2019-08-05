# -*- coding: UTF-8 -*

import requests
from bs4 import BeautifulSoup
import argparse
import datetime
from lxml import etree
from xml.etree import ElementTree as ET
from io import StringIO, BytesIO
import os
import utils
import argparse


FBFeeds = {"cu": "https://www.facebook.com/Junta-de-Freguesia-Curral-das-Freiras-1589413501293908/"}
content = "fb"
dateFile = "lastDate.txt"


def getPostDate(post):
    timestamp = post.find('abbr', {"class": "_5ptz"}).get('data-utime')
    print (timestamp)
    return datetime.datetime.fromtimestamp(int(timestamp))


def getNewFBPosts(bs):
    posts = bs[0].findAll('div', {"class": "_5pcr userContentWrapper"})
    lastDate = datetime.datetime.fromtimestamp(0)
    for post in posts:
        postDate = getPostDate(post)
        if postDate > utils.getLastDate():
            # get post text
            if post.find('span', {"class": "fwb fcg"}) is not None:
                if postDate > lastDate: lastDate = postDate
                getSummaryString(post.find('p').text)
                # create dict with post text and date
                # send post dict to getSummaryString
    utils.setLastDate(lastDate)


#move to utils (and rename!) but move argparse to main and pass args as variables
def getSummaryString(post):
    text = post.encode('utf-8')
    parser = argparse.ArgumentParser(description='Generates wav file based on most recent two posts of a facebook page')
    parser.add_argument('station', type=str, default="cu", help='station location code (cu, ma)')
    parser.add_argument('--accent', type=str, default="pt", help='PT accent code (pt, br, md)')
    parser.add_argument('--gender', type=str, default="female", help='Preferred gender of speaker)')
    args = parser.parse_args()
    utils.get_cprc_tts(text, "cu", "PT", "female", content)
    # send to cerecloud
        
        
def main():
		getNewFBPosts(utils.getHTML(FBFeeds["cu"]))


if __name__ == "__main__":
    main()
