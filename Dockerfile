FROM python:3.9-alpine

ENV FLASK_APP app
ENV FLASK_ENV development
ENV PATH "${PATH}:/home/flasky/.local/bin"

RUN adduser -D flasky
USER flasky

WORKDIR /home/flasky

COPY . .
RUN python -m venv venv
RUN source venv/bin/activate
RUN pip3 install -r requirements.txt
RUN flask init-db

EXPOSE 5000
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]