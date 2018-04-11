# Use an official Python runtime as a parent image
FROM python:3.6
FROM ubuntu:14.04

WORKDIR /appserver
ADD . /appserver
RUN ls
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

RUN apt-get update && apt-get install -y \
    python-pip


# Make port 80 available to the world outside this container
EXPOSE 80

#Launch
RUN pip install -r requirements.txt && gunicorn wsgi
