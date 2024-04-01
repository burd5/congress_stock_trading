# Use the official lightweight Python image.
FROM python:3.10

RUN apt-get update \
    && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable libnss3

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

ENV DISPLAY=:99

COPY ./backend ./backend
COPY .env ./
COPY flow.py ./
COPY settings.py ./

CMD ["python3", "flow.py"]