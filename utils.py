import requests
from cerecloud_rest import CereprocRestAgent
import datetime


def get_cprc_tts(text, station, accent, gender, content):
		file = "audio/pt_" + station + "_" + accent + datetime.datetime.now().strftime("%Y%m%d%H%M") + ".wav"
		#read password etc from file
		restAgent = CereprocRestAgent("https://cerevoice.com/rest/rest_1_1.php", "5ced1a69273fe", "z6rqSLhjNV", "female", "portuguese")
		voice = restAgent._choose_voice("portuguese", gender, accent)
		url, transcript = restAgent.get_cprc_tts(text, voice)
		r = requests.get(url)
		with open(file, 'wb') as f:
				f.write(r.content)
