# Dockerfile Image Container
FROM python:3.9

WORKDIR /facial-recognition-engine

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./benefiary-reference ./benefiary-reference

CMD ['python','./benefiary-reference/app.py']

# docker build -t beneficiary_reference .
# pip freeze > requirements.txt