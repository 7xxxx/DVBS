FROM python:3.9-alpine

ENV PATH "${PATH}:/home/flasky/.local/bin:/usr/local/bin"

RUN apk add git
RUN adduser -D flasky
USER flasky

WORKDIR /home/flasky

#COPY . .
RUN git clone https://github.com/7xxxx/DVBS
WORKDIR /home/flasky/DVBS
#RUN python -m venv venv
#RUN source venv/bin/activate
RUN pip3 install -r requirements.txt
RUN flask init-db

EXPOSE 5000
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:5000", "app:create_app()"]
