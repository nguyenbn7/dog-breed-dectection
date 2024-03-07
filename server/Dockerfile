# For more information, please refer to https://aka.ms/vscode-docker-python
# syntax = docker/dockerfile:1.2
FROM python:3.11-slim as download_model

RUN python -m pip install kaggle --upgrade

WORKDIR /tmp_app
COPY . /tmp_app

RUN --mount=type=secret,id=kaggle_username,dst=/etc/secrets/kaggle_username export KAGGLE_USERNAME=$(cat /etc/secrets/kaggle_username)
RUN --mount=type=secret,id=kaggle_key,dst=/etc/secrets/kaggle_key export KAGGLE_KEY=$(cat /etc/secrets/kaggle_key)

RUN kaggle kernels output nguyenbnguyen/dog-breed-classification-mobilenet -p ./model
RUN rm -f ./*.log ./*.csv

FROM python:3.11-slim as final

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY --from=download_model /tmp_app .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
