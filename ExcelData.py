#------------------------------------------------------------------
# CSV Data Fetch
#------------------------------------------------------------------
import os.path
import csv
import sys
from FetchUrlData import FecthUrl
import json
import re
import logging
error_log = "./error.log"

#------------------------------------
# Method to detect csv file
# If file not exists create a new one
#------------------------------------
class ExcelDataCollection (FecthUrl):
    
    field_names = ["CCP-VERSION", "ALM-VERSION", "DLM-VERSION", "IM-VERSION","DFM-VERSION", "POD"]
    
    def __init__(self, path, url):
        self.path = path
        self.url  = url

    #-------------------
    # Verify file exists
    def detect_file(self):
        return os.path.exists(self.path)

    def create_csv_file(self):
        try:
            if(not self.write_csv_data()):
                # Creating the CSV File only With Headers
                print()
        except:
            print("Oops!",sys.exc_info()[0],"occured.")

    def write_csv_data(self):
        dataDict = {}
        try:
            if (not self.detect_file()):
                print("Creating BuildDetails.csv File Now")
                with open(self.path, mode='a') as csv_file:        
                    writer = csv.DictWriter(csv_file, self.field_names)        
                    writer.writeheader()                      
            data  = FecthUrl(self.url)
            include_items = ["ui-apps","dfm"]
            pod = re.findall(r'icu-(.*?).com', self.url)
            if (not self.log_error(data.fetch_data(), pod)):            
                jsonData = json.loads(data.fetch_data())
                with open(self.path, mode='a') as csv_file:
                    dataDict["POD"] = pod[0].upper()
                    writer = csv.DictWriter(csv_file, self.field_names)
                    for key in jsonData:
                        if(key in include_items):
                            if(key == "dfm"):
                                dataDict[self.field_names[4]] = jsonData[key]["device-status-manager"]
                            else:
                                count = 0
                                for apps in ["ccp", "alm", "dlm", "im"]:
                                    dataDict[self.field_names[count]] = jsonData[key][apps]["buildNumber"]
                                    count += 1
                    writer.writerow(dataDict)
        except ValueError:
            print("Oops!",sys.exc_info()[0],"occured.")
    
    def log_error(self, data, pod):
        retVal = False
        try:
            self.data = data
#             logging.basicConfig(filename = error_log,level=logging.DEBUG)
            if('503' in self.data):
                print("503 Error - Service Not Available - {}".format(pod))
                retVal = True
#                 logging.debug('503 Error')
            elif('404' in self.data):
                print("404 Error - {}".format(pod))
#               logging.debug('404 Error')
#                 
#                 logging.debug('Pod is not available/ ADapeter is not set correctly')
                retVal = True
        except:
            print("Error in {}in line {}".format(__name__),sys.exc_info()[0],"occured.")
        return retVal