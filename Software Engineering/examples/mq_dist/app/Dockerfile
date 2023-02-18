FROM python:3.7-slim-buster

WORKDIR /home/app

COPY . .
RUN chmod 777 boot.sh
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]
