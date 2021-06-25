# set base image (host OS)
FROM python:3.7.9-slim

# copy the content of the local src directory to the working directory
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
RUN pwd
CMD [ "python", "./app.py" ]