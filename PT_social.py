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


feeds = ["https://www.facebook.com/Junta-de-Freguesia-Curral-das-Freiras-1589413501293908/", "https://mobile.facebook.com/Junta-de-Freguesia-Curral-das-Freiras-1589413501293908/?refid=46&__xts__%5B0%5D=12.%7B%22unit_id_click_type%22%3A%22graph_search_results_item_tapped%22%2C%22click_type%22%3A%22result%22%2C%22module_id%22%3A2%2C%22result_id%22%3A%221589413501293908%3A2355997354635515%22%2C%22session_id%22%3A%22107838880979e9972716ed0323dba58b%22%2C%22module_role%22%3A%22PUBLIC_POSTS%22%2C%22unit_id%22%3A%22browse_rl%3A52ac0d34-b8bd-4452-8949-e9b725fb28e4%22%2C%22browse_result_type%22%3A%22browse_type_story%22%2C%22unit_id_result_id%22%3A2355997354635515%2C%22module_result_position%22%3A0%2C%22result_creation_time%22%3A1561190874%7D&__tn__=C"]
content = "fb_camera"
dateFile = "lastDate.txt"


def getHTML():
    feedsHTML = []
    for feed in feeds:
        response = requests.get(feed)
        response.raise_for_status() #if error it will stop the program
        response = response.content
        feedsHTML.append(BeautifulSoup(response, 'html.parser'))
    return feedsHTML


def getPostDate(post):
    timestamp = post.find('abbr', {"class": "_5ptz"}).get('data-utime')
    print (timestamp)
    return datetime.datetime.fromtimestamp(int(timestamp))


def getLastDate():
    if os.path.exists(dateFile):
        file = open(dateFile, "r") 
        lastDate = file.read() 
        file.close()
        try:
            return datetime.datetime.fromtimestamp(int(lastDate))
        except:
            return datetime.datetime.fromtimestamp(int(0))
            
    else:
        return datetime.datetime.fromtimestamp(0)


def setLastDate(lastDate):   
    if os.path.exists(dateFile):
        f = open(dateFile, "w")
        f.write(str(lastDate))
        f.close()


def getNewPosts(bs):
    posts = bs[0].findAll('div', {"class": "_5pcr userContentWrapper"})
    lastDate = datetime.datetime.fromtimestamp(0)
    for post in posts:
        postDate = getPostDate(post)
        if postDate > getLastDate():
            # get post text
            if post.find('span', {"class": "fwb fcg"}) is not None:
                if postDate > lastDate: lastDate = postDate
                getSummaryString(post.find('p').text)
                # create dict with post text and date
                # send post dict to getSummaryString
    setLastDate(lastDate)


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
		getNewPosts(getHTML())


if __name__ == "__main__":
    main()
