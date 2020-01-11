from python:3.7

ENV WD=/home/app
WORKDIR ${WD}

COPY requirements.txt ${WD}
COPY server.py ${WD}
RUN pip install -r requirements.txt

CMD [ "python", "./server.py" ]


