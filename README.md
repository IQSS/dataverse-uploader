# Dataverse Uploader

This action uploads the repository content to a Dataverse data repository.

## Input parameters

To use this action, you will need the following input parameters:

### `DATAVERSE_TOKEN` 

**Required** This is your personal access token. First, you will need to create one at your Dataverse installation. If you are unsure how to do it, have a look at [the Dataverse guide](https://guides.dataverse.org/en/latest/user/account.html#how-to-create-your-api-token).

Second, you will need to save your token as a secret variable called `DATAVERSE_TOKEN` in your GitHub repository (that you want to upload to Dataverse). For instructions on how to do it, have a look at [the GitHub documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository).

The hard part of setting up the action is now done!

### `DATAVERSE_SERVER`

**Required** The URL of your Dataverse installation, i.e., [https://dataverse.harvard.edu](https://dataverse.harvard.edu).

### `DATAVERSE_DATASET_DOI`

**Required** This action requires that a dataset exists on the Dataverse server and its DOI number as input.

Make sure to specify your DOI in this format: `doi:<doi>`, i.e., `doi:10.70122/FK2/LVUA`.

### `GITHUB_DIR`

Use `GITHUB_DIR` if you would like to upload files from only a specific subdirectory in your GitHub repository (i.e., just `data/`).

## Usage

To use the action, create a new YML file (i.e., `workflow.yml`) in the directory `.github/workflows/` in your GitHub repository.

Here is an example of a `workflow.yml`

```
name: Push repo to Dataverse
on:
  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Send repo to Dataverse 
        uses: atrisovic/dataverse-uploader@master
        with:
          DATAVERSE_TOKEN: ${{secrets.DATAVERSE_TOKEN}}
          DATAVERSE_SERVER: https://demo.dataverse.org
          DATAVERSE_DATASET_DOI: doi:10.70122/FK2/LVUA
```

## Dataverse DOI Badge

Check out [this page](https://atrisovic.github.io/dataverse-badge/) to create a Dataverse DOI Badge for your GitHub repository.

