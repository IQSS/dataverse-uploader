from pyDataverse.api import NativeApi, DataAccessApi
from pyDataverse.models import Datafile
from os.path import isdir, join
from time import sleep
from os import walk 
import argparse
import requests
import sys

def parse_arguments():
    parser = argparse.ArgumentParser()

    # Mandatory arguments
    parser.add_argument("token", help="Dataverse token.")
    parser.add_argument("server", help="Dataverse server.")
    parser.add_argument("doi", help="Dataset DOI.")
    parser.add_argument("repo", help="GitHub repository.")

    # Optional arguments
    parser.add_argument("-d", "--dir", help="Uploads only a specific dir.")
    
    args = parser.parse_args()
    return args
    
if __name__ == '__main__':        
    args = parse_arguments()
    dataverse_server = args.server.strip("/") 
    api = NativeApi(dataverse_server , args.token)
    data_api = DataAccessApi(dataverse_server)
    
    # the following deletes all the files in the dataset 
    
    dataset = api.get_dataset(args.doi)
    files_list = dataset.json()['data']['latestVersion']['files']
    
    delete_api = dataverse_server + \
                 '/dvn/api/data-deposit/v1.1/swordv2/edit-media/file/' 
    for f in files_list:
       fileid = f["dataFile"]["id"]
       resp = requests.delete(
           delete_api + str(fileid), \
           auth = (args.token  , ""))
    
    # the following adds all files from the repository to Dataverse 
    
    path = join('repo',args.dir) if args.dir else 'repo'
    for root, subdirs, files in walk(path):
      if '.git' in subdirs:
         subdirs.remove('.git')
      if '.github' in subdirs:
         subdirs.remove('.github')
      for f in files:
         df = Datafile() 
         df.set({
             "pid" : args.doi,
             "filename" : f,
             "directoryLabel": root[5:], 
             "description" : \
               "Uploaded with GitHub Action from {}.".format(
                 args.repo), 
              })
         resp = api.upload_datafile(
                 args.doi, join(root,f), df.json())
         sleep(0.05) # give some time to upload 
    
    # publish updated dataset
    
    resp = api.publish_dataset(args.doi, release_type="major")

