## Testing locally

To test your contribution locally from the command line, clone the repository and create a `repo` helper folder with files to upload:

```
git clone https://github.com/IQSS/dataverse-uploader.git
cd dataverse-uploader
mkdir repo # here store test folders and files for upload
```
### Set up the environment

Next, install the necessary dependencies:

```
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

Now, the folder should look like this:
```
$ ls
CONTRIBUTING.md		README.md		dataverse.py		repo
LICENSE			action.yml		env			requirements.txt
```

### Testing commands

Run the Python script in the following format:

```
python dataverse.py DATAVERSE_TOKEN DATAVERSE_SERVER DATASET_DOI REPO_NAME -p TRUE
```

- `DATAVERSE_TOKEN` - dataverse token should be a valid token
- `DATAVERSE_SERVER` - for testing use https://demo.dataverse.org/
- `DATASET_DOI` - it should be a valid PID from Dataverse demo or a Dataverse installation
- `REPO_NAME` - for the local test, this is a **mock GitHub repository name**, and it should be a string, such as "user/my-repo" or similar

The script will upload everything from **the helper `repo` folder** to the `DATAVERSE_SERVER` at dataset `DATASET_DOI`.

### Examples

- The basic format of the command will upload and publish everything from the helper `repo` folder.

```
python dataverse.py 9s3-7d46-hd https://demo.dataverse.org/ doi:10.70122/FK2/LVUADQ user/my-repo -p TRUE
```

- To upload files and submit the data record for review:

```
python dataverse.py 9s3-7d46-hd https://demo.dataverse.org/ doi:10.70122/FK2/LVUADQ user/my-repo -p FALSE -rev TRUE
```

- To upload files from a single folder, use:

```
python dataverse.py 9s3-7d46-hd https://demo.dataverse.org/ doi:10.70122/FK2/LVUADQ user/my-repo -d first_dir -p TRUE
```

There needs to be a folder named `first_dir` that contains files inside the helper `repo` folder.

- To upload multiple folders, use the command:

```
python dataverse.py 9s3-7d46-hd https://demo.dataverse.org/ doi:10.70122/FK2/LVUADQ user/my-repo -d first_dir,second_dir,third_dir -p TRUE
```

The multiple directories with files need to be stored inside the helper `repo` folder.

- You can append this command with optional arguments such as `--remove/-r False` and `--publish/-p True`:

```
python dataverse.py 9s3-7d46-hd https://demo.dataverse.org/ doi:10.70122/FK2/LVUADQ user/my-repo -r False -p True
```

### Making Releases

Here are the steps for making a release:

1. In the README, replace all instances of the old version with the version you intend to release.
1. Draft a new release and make sure the box is checked to publish the action to the GitHub Marketplace.
1. Under "choose a tag", create a tag for the next version. Keep "target" as the default branch.
1. Under "release title" use "Dataverse Uploader Action".
1. Click "generate release notes" and edit as desired.
1. Publish the release.
1. Check to make sure the release was published to <https://github.com/marketplace/actions/dataverse-uploader-action>.
