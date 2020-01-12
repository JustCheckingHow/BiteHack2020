from python:3.7

ENV WD=/home/app
WORKDIR ${WD}

COPY . ${WD}
RUN pip install -r requirements.txt

CMD [ "python", "./server.py" ]


