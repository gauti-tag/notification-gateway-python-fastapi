FROM python:3.9-alpine3.13
LABEL maintainer="gautier.tiehoule@ngser.com"

COPY ./requirements.txt /tmp/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 4545

RUN python3 -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base musl-dev openssl curl && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
    --disabled-password \
    --no-create-home \
    ngser

ENV PATH="/py/bin:$PATH"

USER ngser

CMD ["uvicorn","app.main:app","--host", "0.0.0.0", "--port", "4545", "--reload"]