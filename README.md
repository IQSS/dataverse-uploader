# Dataverse Uploader

This action uploads the repository content to a Dataverse dataset.

## Input parameters

To use this action, you will need the following input parameters:

| Parameter | Required | Description |
| --------- | -------- | ------------|
| `DATAVERSE_TOKEN` | **Yes** | This is your personal access token that you can create at your Dataverse instance (see [the Dataverse guide](https://guides.dataverse.org/en/latest/user/account.html#how-to-create-your-api-token)). Save your token as a secret variable called `DATAVERSE_TOKEN` in your GitHub repository that you want to upload to Dataverse (see [the GitHub guide](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)). |
| `DATAVERSE_SERVER` | **Yes** | The URL of your Dataverse installation, i.e., [https://dataverse.harvard.edu](https://dataverse.harvard.edu). |
| `DATAVERSE_DATASET_DOI` | **Yes** | This action requires that a dataset (with a DOI) exists on the Dataverse server. Make sure to specify your DOI in this format: `doi:<doi>`, i.e., `doi:10.70122/FK2/LVUA`. |
| `GITHUB_DIR` | No | Use `GITHUB_DIR` if you would like to upload files from only a specific subdirectory in your GitHub repository (i.e., just `data/`). |
| `DELETE` | No | Can be `True` or `False` (by default `True`) depending on whether all files should be deleted in the dataset on Dataverse before upload. |
| `PUBLISH` | No | Can be `True` or `False` (by default `True`) depending on whether you'd like to automatically create a new version of the dataset upon upload. If `False`, the uploaded dataset will be a `DRAFT`. |

## Usage

To use the action, create a new YML file (i.e., `workflow.yml`) in the directory `.github/workflows/` in your GitHub repository.

The action workflow can be executed at trigger events such as `push` and `release`. If you'd only like to run the workflow manually from the Actions tab, use the `workflow_dispatch` event option.

Here is an example of a `workflow.yml` that actives the action on `release` and manually.

```
on: 
  release:
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

If you'd like to upload files from a specific subdirectory only, you should add the `GITHUB_DIR` argument in your workflow.

```
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
          GITHUB_DIR: data
```

If you wouldn't want the action to delete your dataset before upload (i.e., if you already have a Dataverse `DRAFT` dataset), set the `DELETE` argument to `False` like:

```
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
          GITHUB_DIR: data
          DELETE: False
```

Upon upload, the action will automatically publish a new version of the Dataverse dataset by default. If you'd like to create a new version manually, set the `PUBLISH` argument to `False`.

```
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
          GITHUB_DIR: data
          DELETE: False
          PUBLISH: False
```

## Related projects

Check out the following related projects:

### Dataverse Badge 

Visit [this page](https://atrisovic.github.io/dataverse-badge/) to create a Dataverse DOI Badge for your GitHub repository.

[![](<https://img.shields.io/badge/Dataverse DOI-10.70122/FK2/LVUADQ-orange>)](https://demo.dataverse.org)

### Stand-alone DVUploader

Looking for a stand-alone Dataverse uploader that will work from the command line? Check out [DVUploader](https://github.com/GlobalDataverseCommunityConsortium/dataverse-uploader).

## Contact

Don't hesitate to create an issue, a pull request, or contact us if you notice any problems with the action.
