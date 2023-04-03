FROM python:3.9

WORKDIR /usr/local
RUN apt update && apt upgrade -y
RUN git clone https://github.com/Leethine/sanctus.git

WORKDIR /usr/local/sanctus/scripts
RUN mkdir -p /mnt/sanctus_db
RUN bash create_db.sh -f /mnt/sanctus_db

WORKDIR /usr/local/sanctus/deploy
RUN pip install pyxtermjs uwsgi gevent gevent-websocket

# This step can be ignored if no deployment file has been modified
#RUN rm -fr *
#COPY pyxtermjs_docker/entry.py .
#COPY pyxtermjs_docker/pyxtermjs.ini .
#COPY . .

## Clean up useless packages
RUN apt remove -y *-dev
RUN apt remove -y wget curl g++ gcc make automake perl build-essential autoconf ca-certificates gnupg
RUN apt remove -y imagemagick bzip2 icu-devtools unzip
RUN apt autoremove -y

EXPOSE 5000

CMD ["uwsgi", "--ini", "pyxtermjs.ini"]