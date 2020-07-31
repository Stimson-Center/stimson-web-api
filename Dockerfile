FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN mkhomedir_helper nginx

RUN apt-get -y update && \
    apt-get -y install build-essential pkg-config python-dev python-setuptools systemd pipenv python3-venv uwsgi-plugin-python3

COPY supervisord.conf /etc/supervisor/supervisord.conf
# COPY default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /app
COPY bashrc /etc/bash.bashrc
RUN chmod a+rwx /etc/bash.bashrc

COPY ./app /app
COPY .env /app/.env
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/.GOOGLE_APPLICATION_CREDENTIALS.json
ENV GOOGLE_DRIVE_CREDENTIALS=/app/credentials.json
COPY requirements.txt /app/requirements.txt
COPY prestart.sh /app/prestart.sh


## add permissions for nginx user
RUN chown -R nginx:nginx /app && \
    chmod -R 755 /app && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /var/log/supervisor && \
    chown -R nginx:nginx /var/run && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    chown nginx:nginx /etc/nginx/nginx.conf
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

WORKDIR /app
USER nginx

RUN python -m venv /app/.venv
RUN . /app/.venv/bin/activate && pip install --upgrade pip
RUN . /app/.venv/bin/activate && pip uninstall -y crcmod
RUN . /app/.venv/bin/activate && pip install --no-cache-dir -U crcmod
RUN . /app/.venv/bin/activate && pip install -r requirements.txt
RUN . /app/.venv/bin/activate && python -m spacy download zh_core_web_sm  # Chinese
RUN . /app/.venv/bin/activate && python -m spacy download da_core_news_sm # Danish
RUN . /app/.venv/bin/activate && python -m spacy download nl_core_news_sm # Dutch
RUN . /app/.venv/bin/activate && python -m spacy download en_core_web_sm  # English
RUN . /app/.venv/bin/activate && python -m spacy download fr_core_news_sm # French
RUN . /app/.venv/bin/activate && python -m spacy download de_core_news_sm # German
RUN . /app/.venv/bin/activate && python -m spacy download el_core_news_sm # Greek
RUN . /app/.venv/bin/activate && python -m spacy download ja_core_news_sm # Japanese
RUN . /app/.venv/bin/activate && python -m spacy download it_core_news_sm # Italian
RUN . /app/.venv/bin/activate && python -m spacy download lt_core_news_sm # Lithuanian
RUN . /app/.venv/bin/activate && python -m spacy download xx_ent_wiki_sm  # Multi-language
RUN . /app/.venv/bin/activate && python -m spacy download nb_core_news_sm # Norwegian Bokmål
RUN . /app/.venv/bin/activate && python -m spacy download pl_core_news_sm # Polish
RUN . /app/.venv/bin/activate && python -m spacy download pt_core_news_sm # Portuguese
RUN . /app/.venv/bin/activate && python -m spacy download ro_core_news_sm # Romanian
RUN . /app/.venv/bin/activate && python -m spacy download es_core_news_sm # Spanish


# remove for security purposes
# RUN rm /app/requirements.txt


## set environment variables
# https://stackoverflow.com/questions/18417823/how-do-i-run-uwsgi-with-virtualenv
ENV VIRTUAL_ENV /app/.venv
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV production
ENV SECRET_KEY $SECRET_KEY

# https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/
ENV UWSGI_INI /app/uwsgi.ini
ENV NGINX_WORKER_PROCESSES auto
ENV NGINX_WORKER_PROCESSES 2
ENV NGINX_WORKER_CONNECTIONS 1024
ENV NGINX_MAX_UPLOAD 1000m
ENV LISTEN_PORT 8080

EXPOSE 8080
