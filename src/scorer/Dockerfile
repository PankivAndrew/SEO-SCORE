FROM python:3.7-alpine

RUN echo '* * * * * /usr/local/bin/python /src/cronjob_run.py meter_validator_run' > /etc/crontabs/root

ADD . /src

WORKDIR /src

RUN pip install -r /src/collector/requirements.txt

CMD crond & python  /src/mqtt_run.py