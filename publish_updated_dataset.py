import sys
from pyDataverse.api import NativeApi

dataverse_server = sys.argv[1]
dataverse_token = sys.argv[2]
dataverse_dataset_doi = sys.argv[3]

api = NativeApi(dataverse_server, dataverse_token)

resp = api.publish_dataset(dataverse_dataset_doi, release_type="major")
