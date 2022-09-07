FROM python:3.10-buster

WORKDIR /subscriber

# Manage dependencies
COPY ./requirements.txt /subscriber/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /subscriber/requirements.txt

COPY ./main.py /subscriber/main.py
COPY ./queries/ /subscriber/queries/
COPY ./config.py /subscriber/config.py

ENV PYTHONPATH "${PYTHONPATH}:/subscriber"
ENTRYPOINT [ "python", "main.py" ]