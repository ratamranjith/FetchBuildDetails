#------------------------------
# Main File - Get the main data
from ExcelData import ExcelDataCollection
import os

#--------------------------------------------
# Based on the URL Print the Data in Csv File
path = '.\BuildDetails.csv'

if (os.path.exists(path)):
    os.remove(path)


#----------------
# Read user input
userInput = "./UserInput.txt"
fileData = open(userInput, "r").readlines()
for pods in fileData:
#     print(pods.strip())
    url   = 'https://ccpapi.icu-{}.com/meta/version'.format(pods.strip())
    excel = ExcelDataCollection(path, url)
    excel.write_csv_data()