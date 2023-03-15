FROM python:3.9.13-alpine

WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev gettext
COPY requirements/requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
