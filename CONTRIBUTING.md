## Testing locally

To test your contribution locally from the command line, run the Python script in the following format:

```
python dataverse.py DATAVERSE_TOKEN DATAVERSE_SERVER DATASET_DOI REPO_NAME
```

Example:
```
python dataverse.py 9s3-7d46-hd https://demo.dataverse.org/ doi:10.70122/FK2/LVUADQ user/my-repo 
```

You can append this command with optional arguments such as `--dir data --remove False --publish True`
