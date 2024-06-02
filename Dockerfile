FROM python:alpine3.10

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# upgrade pip
RUN pip install --upgrade pip

# Label
LABEL maintainer="benjamin"

# create root directory for our project in the container
RUN mkdir /app

# WORKING DIRECTORY
WORKDIR /app

# Set the working directory
ADD . /app/

# Install app dependencies
RUN pip install -r requirements.txt

