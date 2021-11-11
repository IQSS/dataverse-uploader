#!/bin/sh -l

java -jar DVUploader-v1.0.9.jar \
    -key=$DATAVERSE_TOKEN \
    -did=$DATAVERSE_DATASET_DOI \
    -server=$DATAVERSE_SERVER \
    -verify \
    -recurse \
    repodir \
    \
