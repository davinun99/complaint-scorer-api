FROM python:3.11.7-slim

RUN pip install pipenv

ENV PROJECT_DIR /app

COPY . /${PROJECT_DIR}
WORKDIR ${PROJECT_DIR}
# RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN apt-get update && apt-get install -y default-jre
RUN pipenv install --system --deploy

CMD ["gunicorn", "--graceful-timeout", "5", "scorer:app",  "-w", "4", "-b", "0.0.0.0:80"]