FROM python:3
WORKDIR /client
RUN pip install coloredlogs
COPY . /client
CMD [ "python", "./main.py" ]