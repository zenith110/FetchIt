# set base image (host OS)
FROM python:3.7.9-slim


# set the working directory in the container
WORKDIR /home/fetchit/backend

# copy the content of the local src directory to the working directory
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY src/ .

CMD ["python", "app.py", "0.0.0.0:5000"]
