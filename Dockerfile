# syntax=docker/dockerfile:1

FROM python:3.9
RUN pip install --upgrade pip
COPY requirements.txt /home/
RUN pip install -r /home/requirements.txt
COPY *.py /home/
CMD [ "python", "/home/app.py" ]
EXPOSE 5000
