## Testing locally

To test your contribution locally from the command line, first install the necessary dependencies:

```
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

Then run the Python script in the following format:

```
python dataverse.py DATAVERSE_TOKEN DATAVERSE_SERVER DATASET_DOI REPO_NAME
```

- `DATAVERSE_TOKEN` - dataverse token should be a valid token
- `DATAVERSE_SERVER` - for testing use https://demo.dataverse.org/
- `DATASET_DOI` - it should be a valid PID from Dataverse demo or the real Dataverse instalation 
- `REPO_NAME` - for the local test, this is a **mock GitHub repository name**, and it should be a string such as "user/my-repo" or similar

Examples:

- To upload everything from a current folder, use:

```
python dataverse.py 9s3-7d46-hd https://demo.dataverse.org/ doi:10.70122/FK2/LVUADQ user/my-repo -d .
```

- To upload files from another folder on the system, use:

```
python dataverse.py 9s3-7d46-hd https://demo.dataverse.org/ doi:10.70122/FK2/LVUADQ user/my-repo -d /tmp/files-to-upload
```

- You can append this command with optional arguments such as --remove/-r False` and `--publish/-p True`:

```
python dataverse.py 9s3-7d46-hd https://demo.dataverse.org/ doi:10.70122/FK2/LVUADQ user/my-repo -d /tmp/files-to-upload -r False -p True
```
