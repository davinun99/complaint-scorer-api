# syntax=docker/dockerfile:1

FROM python:3.11.3-alpine3.17 as base


WORKDIR /python-docker

# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt

FROM base AS python-deps

RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc
COPY Pipfile .
COPY Pipfile.lock .
# RUN PIPENV_VENV_IN_PROJECT=1 
# RUN cd python-dockerfile
RUN pipenv install --deploy
# RUN 
FROM base AS runtime
# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]