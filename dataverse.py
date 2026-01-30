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
        choices=('True', 'TRUE', 'true', 'False', 'FALSE', 'false'), \
        default='true')
    parser.add_argument(
        "-p", "--publish", help="Publish a new dataset version after upload.", \
        choices=('True', 'TRUE', 'true', 'False', 'FALSE', 'false'), \
        default='false')

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

    print(f"Connecting to Dataverse server: {dataverse_server}")
    print(f"Dataset DOI: {args.doi}")

    dataset = api.get_dataset(args.doi)
    files_list = dataset.json()['data']['latestVersion']['files']
    dataset_dbid = dataset.json()['data']['id']

    print(f"Dataset ID: {dataset_dbid}")
    print(f"Found {len(files_list)} existing files in dataset")

    if args.remove.lower() == 'true':
        # the following deletes all the files in the dataset
        print(f"Deleting {len(files_list)} existing files...")
        delete_api = dataverse_server + \
            '/dvn/api/data-deposit/v1.1/swordv2/edit-media/file/'
        for f in files_list:
            fileid = f["dataFile"]["id"]
            filename = f["dataFile"].get("filename", "unknown")
            print(f"  Deleting file: {filename} (ID: {fileid})")
            resp = requests.delete(
                delete_api + str(fileid), \
                auth = (token  , ""))
            print(f"    Response status: {resp.status_code}")

    # check if there is a list of dirs to upload
    paths = [args.repo]
    if args.dir:
        dirs = args.dir.strip().replace(",", " ")
        dirs = dirs.split()
        paths = [join(args.repo, d) for d in dirs]

    print(f"\nPaths to upload: {paths}")

    # the following adds all files from the repository to Dataverse
    upload_count = 0
    for path in paths:
        print(f"\nScanning path: {path}")
        if not walk(path):
            print(f"  Warning: Path does not exist or is empty")
        for root, subdirs, files in walk(path):
            if '.git' in subdirs:
                subdirs.remove('.git')
            if '.github' in subdirs:
                subdirs.remove('.github')
            print(f"  Directory: {root} (contains {len(files)} files)")
            for f in files:
                upload_count += 1
                full_path = join(root, f)
                # Remove the repo prefix from the directory label
                repo_prefix_len = len(args.repo) + 1 if args.repo != '.' else 0
                directory_label = root[repo_prefix_len:] if len(root) > repo_prefix_len else ""
                print(f"    Uploading [{upload_count}]: {full_path}")
                print(f"      Filename: {f}")
                print(f"      Directory label: '{directory_label}'")
                df = Datafile()
                df.set({
                    "pid" : args.doi,
                    "filename" : f,
                    "directoryLabel": directory_label,
                    "description" : \
                      "Uploaded with GitHub Action from {}.".format(
                        args.repo),
                    })
                resp = api.upload_datafile(
                    args.doi, join(root,f), df.json())
                print(f"      Response status: {resp.status_code}")
                if resp.status_code not in [200, 201]:
                    print(f"      ERROR: {resp.text}")
                check_dataset_lock(5)

    print(f"\nTotal files uploaded: {upload_count}")

    if args.publish.lower() == 'true':
        # publish updated dataset
        print("\nPublishing dataset...")
        resp = api.publish_dataset(args.doi, release_type="major")
        print(f"Publish response status: {resp.status_code}")
        if resp.status_code not in [200, 201]:
            print(f"ERROR: {resp.text}")

    print("\nDone!")
