# Dataverse Uploader

This action automatically uploads GitHub repository content to a Dataverse dataset. 
It can upload the entire repository or its subdirectories into an existing dataset on a target
Dataverse installation. The action is customizable, allowing you to fully replace a dataset, 
add to the dataset, publish it or leave it as a draft version on Dataverse.

The action provides some additional metadata to the dataset, such as the origin GitHub repository, 
and it preserves the directory tree structure.

## Input parameters

To use this action, you will need the following input parameters:

| Parameter | Required | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| --------- | -------- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `DATAVERSE_TOKEN` | **Yes** | This is your personal access token that you can create at your Dataverse instance (see [the Dataverse guide](https://guides.dataverse.org/en/latest/user/account.html#how-to-create-your-api-token)). Save your token as a secret variable called `DATAVERSE_TOKEN` in your GitHub repository that you want to upload to Dataverse (see [the GitHub guide](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)). |
| `DATAVERSE_SERVER` | **Yes** | The URL of your Dataverse installation, i.e., [https://dataverse.harvard.edu](https://dataverse.harvard.edu).                                                                                                                                                                                                                                                                                                                                                                  |
| `DATAVERSE_DATASET_DOI` | **Yes** | This action requires that a dataset (with a DOI) exists on the Dataverse server. Make sure to specify your DOI in this format: `doi:<doi>`, i.e., `doi:10.70122/FK2/LVUA`.                                                                                                                                                                                                                                                                                                     |
| `GITHUB_DIR` | No | Use `GITHUB_DIR` if you would like to upload files from only one or more subdirectories in your GitHub repository (i.e., `data/`, `plots/`).                                                                                                                                                                                                                                                                                                                                           |
| `DELETE` | No | Can be `True` or `False` (by default `True`) depending on whether all files should be deleted in the dataset on Dataverse before upload.                                                                                                                                                                                                                                                                                                                                       |
| `PUBLISH` | No | Can be `True` or `False` (by default `False`) depending on whether you'd like to automatically create a new version of the dataset upon upload. If `False`, the uploaded dataset will be a `DRAFT`.                                                                                                                                                                                                                                                                            |
| `REVIEW` | No | Can be `True` or `False` (by default `False`) depending on whether you'd like to automatically submit the dataset for review upon upload. If `True`, the uploaded dataset will be a `In Review`.                                                                                                                                                                                                                                                                            |

## Usage

To use the action, create a new YML file (i.e., `workflow.yml`) and place it in the directory `.github/workflows/` in your GitHub repository.

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
        uses: IQSS/dataverse-uploader@v1.6
        with:
          DATAVERSE_TOKEN: ${{secrets.DATAVERSE_TOKEN}}
          DATAVERSE_SERVER: https://demo.dataverse.org
          DATAVERSE_DATASET_DOI: doi:10.70122/FK2/LVUA
```

If you'd like to upload files from a specific subdirectory only (for instance, a `data` folder), 
you should add the `GITHUB_DIR` argument in your workflow, as follows:

```
steps:
  - name: Send repo to Dataverse 
    uses: IQSS/dataverse-uploader@v1.6
    with:
      DATAVERSE_TOKEN: ${{secrets.DATAVERSE_TOKEN}}
      DATAVERSE_SERVER: https://demo.dataverse.org
      DATAVERSE_DATASET_DOI: doi:10.70122/FK2/LVUA
      GITHUB_DIR: data
```

You can upload multiple subdirectories by listing them as `GITHUB_DIR` like `GITHUB_DIR: data,plots`, or in the following format:

```
steps:
  - name: Send repo to Dataverse 
    uses: IQSS/dataverse-uploader@v1.6
    with:
      DATAVERSE_TOKEN: ${{secrets.DATAVERSE_TOKEN}}
      DATAVERSE_SERVER: https://demo.dataverse.org
      DATAVERSE_DATASET_DOI: doi:10.70122/FK2/LVUA
      GITHUB_DIR: |
        data
        plots 
```

By default, the action will sync the GitHub repository and the Dataverse dataset, meaning that it will
delete the Dataverse content before uploading the content from GitHub. If you don't want the action to 
delete your dataset before upload (i.e., if you already have a Dataverse `DRAFT` dataset), 
set the `DELETE` argument to `False` like:

```
steps:
  - name: Send repo to Dataverse 
    uses: IQSS/dataverse-uploader@v1.6
    with:
      DATAVERSE_TOKEN: ${{secrets.DATAVERSE_TOKEN}}
      DATAVERSE_SERVER: https://demo.dataverse.org
      DATAVERSE_DATASET_DOI: doi:10.70122/FK2/LVUA
      GITHUB_DIR: data
      DELETE: False
```

The action automatically uploads new content to a Dataverse dataset, but it will not publish it as a
new version by default. If you'd like the action to publish a new dataset version in Dataverse, 
set the `PUBLISH` argument to `True`.

```
steps:
  - name: Send repo to Dataverse 
    uses: IQSS/dataverse-uploader@v1.6
    with:
      DATAVERSE_TOKEN: ${{secrets.DATAVERSE_TOKEN}}
      DATAVERSE_SERVER: https://demo.dataverse.org
      DATAVERSE_DATASET_DOI: doi:10.70122/FK2/LVUA
      GITHUB_DIR: data
      DELETE: False
      PUBLISH: True
```

If you would like the action to submit the dataset for review instead:

```
steps:
  - name: Send repo to Dataverse 
    uses: IQSS/dataverse-uploader@v1.6
    with:
      DATAVERSE_TOKEN: ${{secrets.DATAVERSE_TOKEN}}
      DATAVERSE_SERVER: https://demo.dataverse.org
      DATAVERSE_DATASET_DOI: doi:10.70122/FK2/LVUA
      GITHUB_DIR: data
      DELETE: False
      PUBLISH: False
      REVIEW: True
```

## Q&A

1. **If you change the content of your GitHub repository, are the changes synchronized in Dataverse? Otherwise, is it possible to synchronize them automatically?**

Yes, the action is able to automatically update the Dataverse dataset. In other words, if the action
is triggered with every `push` to the GitHub repository, it will automatically upload its content to
Dataverse. You specify the action triggers in the workflow (`.yml`) file, and in this case, it would 
contain `on: push` line to execute the action on every push to the repository.

2. **Will the action work with dataset Handles as persistent identifiers (PIDs) instead of DOIs?**

Yes, the action uses Dataverse API that supports both DOIs and Handles for retrieving and uploading data.

3. **How do I contribute to this project?**

Have a look at the instructions in the `CONTRIBUTING.md` file.

## Related projects

Check out the following related projects:

### Dataverse Badge 

Visit [this page](https://atrisovic.github.io/dataverse-badge/) to create a Dataverse DOI Badge for your GitHub repository.

[![](<https://img.shields.io/badge/Dataverse DOI-10.70122/FK2/LVUADQ-orange>)](https://demo.dataverse.org)

### Stand-alone DVUploader

Looking for a stand-alone Dataverse uploader that will work from the command line? Check out [DVUploader](https://github.com/GlobalDataverseCommunityConsortium/dataverse-uploader).

## References

See the official Dataverse documentation [here](https://guides.dataverse.org/en/latest/admin/integrations.html#id10).

## Contact

Don't hesitate to create an issue, a pull request, or contact us if you notice any problems with the action.
