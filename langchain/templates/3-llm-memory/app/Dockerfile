FROM python:3.12.1-slim

ARG APP_USER=app_user
ARG APP_DIR=/app

RUN groupadd -r ${APP_USER} && useradd -r -g ${APP_USER} ${APP_USER}

WORKDIR ${APP_DIR}

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

RUN chown -R ${APP_USER}:${APP_USER} ${APP_DIR}

USER $USER
ENTRYPOINT ["/app/entrypoint.sh"]
