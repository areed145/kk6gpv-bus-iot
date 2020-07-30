FROM python:3.7-slim-buster

LABEL maintainer="areed145@gmail.com"

WORKDIR /bus_iot

COPY . /bus_iot

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "bus_iot/bus_iot.py"]