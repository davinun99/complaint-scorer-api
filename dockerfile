# syntax=docker/dockerfile:1

FROM python:3.11.7-slim as base


WORKDIR /python-docker

FROM base AS python-deps

RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc
COPY Pipfile .
COPY Pipfile.lock .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

COPY --from=python-deps /python-docker/.venv /.venv
ENV PATH="/.venv/bin:$PATH"
COPY . .

CMD [ "python3", "-m" , "flask", "--app", "api_tagger.py", "run", "-h", "0.0.0.0", "-p", "5050"]
