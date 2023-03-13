FROM python:3.10-slim-buster

WORKDIR /python-docker

RUN apt-get update
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/python-docker"
COPY . .

CMD [ "python3", "src/main.py"]