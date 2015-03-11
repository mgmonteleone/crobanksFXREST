FROM ubuntu:latest
RUN apt-get update && apt-get upgrade -y && apt-get -y install python libffi-dev libssl-dev build-essential gunicorn python-dev python-pip && apt-get clean
ADD . /app
RUN pip install -r /app/requirements.txt
EXPOSE 5000
WORKDIR /app
CMD gunicorn --config unicorn.conf.py --log-file=-. run:app