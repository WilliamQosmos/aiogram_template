FROM python:3.10-buster as builder
COPY requirements.txt requirements.txt
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10-slim-buster
LABEL maintainer="williamqosmos <max.2898@yandex.ru>" \
      description="Template Telegram Bot"
ENV VIRTUAL_ENV=/opt/venv
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
VOLUME /log
VOLUME /config
EXPOSE 3000
COPY app app
COPY alembic.ini alembic.ini
COPY migrations migrations
ENTRYPOINT ["python3", "-m", "app"]