FROM python:3.8.1,
ENV PYTHONUNBUFFERED 1,
ENV SECRET_KEY e72t)7a5^d9nrfrz_i=%=dsa2%%v7kf*9hqp*9toe3ff)%s2&j,
ENV DEBUG True,
ENV DEFAULT_API_URL https://studio-api.sptitan.flowyt.com/,
ENV ALLOWED_HOSTS *,
ENV DATABASE_URL postgresql://orch:or!v1G64@172.31.5.149:5432/orchestryzi_api,

ENV EMAIL_HOST smtp.mailgun.org,
ENV EMAIL_PORT 587,
ENV EMAIL_HOST_USER postmaster@mg.flowyt.com,
ENV EMAIL_HOST_PASSWORD ffcc84b696e1f48e21503368a62e8c67-9dda225e-70c7e481,
ENV EMAIL_USE_TLS True,

RUN pip install -U pip setuptools,

RUN mkdir -p /usr/src/app,
WORKDIR /usr/src/app,
COPY ./ /usr/src/app,

RUN pip install --upgrade pip,
RUN pip install pipenv,
RUN pipenv lock --requirements > requirements.txt,
RUN pip install --no-cache-dir -r requirements.txt,
RUN python manage.py migrate,

EXPOSE 8100,
CMD sh /usr/src/app/run_web.sh