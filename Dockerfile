FROM python:3.9.17-slim
LABEL authors="antonioalarcon"

WORKDIR /usr/src/app
COPY . .

RUN apt update && apt install -y cron
RUN pip install --no-cache-dir -r requirements.txt

COPY crontab /etc/cron.d/script-cron
RUN chmod 0644 /etc/cron.d/script-cron
RUN touch /var/log/cron.log

CMD printenv > /etc/environment && cron && tail -f /var/log/cron.log