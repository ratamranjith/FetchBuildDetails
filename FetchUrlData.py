import requests
from multiprocessing import Queue
import urllib

class FecthUrl:
    def __init__(self, url):
        self.url = url
        
    def fetch_data(self):
        try:
            headers = {'content-type': 'application/json'}
            return (requests.get(self.url, headers=headers).text)
        except urllib.error.URLError:
            print("Failed to Establish the Connection")
        except ConnectionError:
            print("Failed to Establish the Connection")