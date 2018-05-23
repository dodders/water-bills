
FROM ubuntu
MAINTAINER george.dodwell@gmail.com

RUN apt-get update
RUN apt-get install -y python3.6
RUN apt-get install -y python3-pip
RUN pip3 install --user pipenv

RUN apt-get install -y libappindicator1 fonts-liberation
RUN apt-get install -y wget
RUN cd tmp
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome*.deb; exit 0
RUN apt-get install -f -y; exit 0


