import argparse
from time import sleep
from os.path import join
from os import walk
import requests
from pyDataverse.api import NativeApi
from pyDataverse.models import Datafile

def parse_arguments():
    """ Parses cmd-line arguments """
    parser = argparse.ArgumentParser()

    # Mandatory arguments
    parser.add_argument("token", help="Dataverse token.")
    parser.add_argument("server", help="Dataverse server.")
    parser.add_argument("doi", help="Dataset DOI.")
    parser.add_argument("repo", help="GitHub repository.")

    # Optional arguments
    parser.add_argument("-d", "--dir", help="Uploads only a specific dir.")
    parser.add_argument(
        "-r", "--remove", help="Remove (delete) all files before upload.", \
        choices=('True', 'False'), default='True')
    parser.add_argument(
        "-p", "--publish", help="Publish a new dataset version after upload.", \
        choices=('True', 'False'), default='True')

    args_ = parser.parse_args()
    return args_


def check_dataset_lock(num):
    """ Gives Dataverse server more time for upload """
    if num <= 1:
        print('Lock found for dataset id ' + \
          str(dataset_dbid) + '\nTry again later!')
        return

    query_str = dataverse_server + \
         '/api/datasets/' + str(dataset_dbid) + '/locks/'
    resp_ = requests.get(query_str, auth = (token, ""))
    locks = resp_.json()['data']

    if bool(locks):
        print('Lock found for dataset id ' + \
           str(dataset_dbid) + '\n... sleeping...')
        sleep(2)
        check_dataset_lock(num-1)
    return


if __name__ == '__main__':
    args = parse_arguments()
    token = args.token
    dataverse_server = args.server.strip("/")
    api = NativeApi(dataverse_server , token)

    dataset = api.get_dataset(args.doi)
    files_list = dataset.json()['data']['latestVersion']['files']
    dataset_dbid = dataset.json()['data']['id']

    if args.remove == 'True':
        # the following deletes all the files in the dataset
        delete_api = dataverse_server + \
            '/dvn/api/data-deposit/v1.1/swordv2/edit-media/file/'
        for f in files_list:
            fileid = f["dataFile"]["id"]
            resp = requests.delete(
                delete_api + str(fileid), \
                auth = (token  , ""))

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
            check_dataset_lock(5)

    if args.publish == 'True':
        # publish updated dataset
        resp = api.publish_dataset(args.doi, release_type="major")
