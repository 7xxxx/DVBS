FROM python:alpine
RUN apk add git && \
    adduser -D flasky && \
    git clone https://github.com/7xxxx/DVBS /home/flasky/DVBS && \
    chown -R flasky /home/flasky/DVBS && \
    chmod -R u+rw /home/flasky/DVBS

USER flasky
WORKDIR /home/flasky/DVBS
ENV PATH "${PATH}:/home/flasky/.local/bin:/usr/local/bin"

RUN pip3 install -r requirements.txt && \
    flask init-db

EXPOSE 5000
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:5000", "app:create_app()"]
