# -*- coding: UTF-8 -*
import requests
import datetime
from cerecloud_rest import CereprocRestAgent
import ConfigParser

#edit for more flexible audio file names and location

def get_cprc_tts(text, station, accent, gender, content):
		file = "audio/pt_" + station + "_" + accent + "_" + content + "_" + datetime.datetime.now().strftime("%Y%m%d%H%M") + ".wav"
		# config = configparser.ConfigParser()
		# config.read('config.ini')
		# username = config['cerecloud']['CEREPROC_USERNAME']
		# password = config['cerecloud']['CEREPROC_PASSWORD']
		username = "5aec2e36c429d"
		password = "VkZmL42e5L"
		restAgent = CereprocRestAgent("https://cerevoice.com/rest/rest_1_1.php", username, password, "female", "portuguese")
		voice = restAgent._choose_voice("portuguese", gender, accent)
		url, transcript = restAgent.get_cprc_tts(text, voice)
		r = requests.get(url)
		with open(file, 'wb') as f:
				f.write(r.content)


def getHTML(feed):
		response = requests.get(feed)
		response.raise_for_status() #if error it will stop the program
		response = response.content
		HTMLFeed = BeautifulSoup(response, 'html.parser')
		return HTMLFeed

 # update to use actual file name. take paramaters for indicating which date it is about. 
 # decide on date file format - use the config file, have variables named based on the parameters
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

# move to utils
def setLastDate(lastDate):   
    if os.path.exists(dateFile):
        f = open(dateFile, "w")
        f.write(str(lastDate))
        f.close()
