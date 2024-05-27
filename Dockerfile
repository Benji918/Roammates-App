FROM python:alpine3.19

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Label
LABEL maintainer="benjamin"

# WORKING DIRECTORY
WORKDIR /app

# Set the working directory
COPY . .

# Install app dependencies
RUN pip install -r requirements.txt

EXPOSE 8000
