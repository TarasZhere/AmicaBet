
# a python version that works well with flask
FROM python:3.10-alpine

ARG api_ip
ENV SERVER_API=${api_ip}

RUN pip install flask
RUN pip install requests

EXPOSE 80/tcp

COPY /amica /amica
CMD ["flask", "--app", "amica", "run", "--port", "80", "--host", "0.0.0.0", "--debug"]