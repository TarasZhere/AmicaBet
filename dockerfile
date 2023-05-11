
# a python version that works well with flask
FROM python:3.10-alpine
WORKDIR .

COPY /amica /amica
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["flask", "--app", "amica", "run", "--port", "80", "--host", "0.0.0.0"]