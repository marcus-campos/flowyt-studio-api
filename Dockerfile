FROM python:3.11.7

RUN pip install -U pip setuptools

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./Pipfile /usr/src/app
COPY ./Pipfile.lock /usr/src/app

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy

COPY ./ /usr/src/app

EXPOSE 7000