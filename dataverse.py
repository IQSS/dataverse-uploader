from pyDataverse.api import NativeApi, DataAccessApi
from pyDataverse.models import Datafile
from os.path import isfile, join
from os import listdir
import requests
import hashlib
import sys

dataverse_token = sys.argv[1]
dataverse_server = sys.argv[2].strip("/")
dataverse_dataset_doi = sys.argv[3]

api = NativeApi(dataverse_server, dataverse_token)
data_api = DataAccessApi(dataverse_server)

# delete all

#dataset = api.get_dataset(dataverse_dataset_doi)
#files_list = dataset.json()['data']['latestVersion']['files']
#
#delete_api = dataverse_server + \
#             '/dvn/api/data-deposit/v1.1/swordv2/edit-media/file/' 
#for file in files_list:
#   fileid = files_list[1]["dataFile"]["id"]
#   resp = requests.delete(
#       delete_api + str(fileid), headers={
#           'Authorization' : dataverse_token})

# add all

path='repo'
for f in listdir(path):
  if not f.startswith('.'):
     df = Datafile() 
     df.set({
         "pid" : dataverse_dataset_doi,
         "filename" : f,})
     resp = api.upload_datafile(dataverse_dataset_doi, path+"/"+f, df.json())

# publish updated dataset

resp = api.publish_dataset(dataverse_dataset_doi, release_type="major")
