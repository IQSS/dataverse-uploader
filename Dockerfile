FROM openjdk:8-jdk-alpine
RUN apk add --no-cache curl tar bash procps

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# Install pyDataverse and DVUploader
RUN pip install -U pyDataverse
RUN wget https://github.com/GlobalDataverseCommunityConsortium/dataverse-uploader/releases/download/v1.0.9/DVUploader-v1.0.9.jar

COPY publish_updated_dataset.py /publish_updated_dataset.py
COPY entrypoint.sh /entrypoint.sh
#ENTRYPOINT ["/entrypoint.sh"]
