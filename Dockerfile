
FROM ubuntu
MAINTAINER george.dodwell@gmail.com

RUN apt-get update
RUN apt-get install -y python3.6
RUN apt-get install -y python3-pip
RUN pip3 install --user pipenv

RUN apt-get install -y libappindicator1 fonts-liberation
RUN apt-get install -y wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome*.deb; exit 0
RUN apt-get install -f -y; exit 0
RUN rm *.deb
RUN apt-get install -y chromium-chromedriver
RUN ln -s /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /app
COPY *.py /app/
COPY Pipfile* /app/
COPY *.sh /app/

RUN /root/.local/bin/pipenv install
CMD /root/.local/bin/pipenv run python3 main.py



