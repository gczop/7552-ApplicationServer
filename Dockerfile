# Use an official Python runtime as a parent image
FROM python:3.6
FROM ubuntu:16.04

WORKDIR /appserver
ADD . /appserver
#RUN ls
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

RUN ["chmod", "+x", "/entrypoint.sh"]
RUN apt-get update && apt-get install -y python-pip

#RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
#RUN echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.2.list
#RUN apt-get update 
#RUN apt-get install -y mongodb-org 


# Make port 80 available to the world outside this container
EXPOSE 8000
EXPOSE 5000

#Launch
#sudo docker run appserver /bin/bash -c "pip install -r requirements.txt;gunicorn wsgi" -p 8000:5000
CMD ["/bin/bash", "-c", "pip install -r requirements.txt;gunicorn wsgi"]
#CMD ["/bin/bash", "-c", "pip install -r requirements.txt;python app.py"]
