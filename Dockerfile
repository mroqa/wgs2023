<<<<<<< HEAD
# syntax=docker/dockerfile:1

FROM python:3.9

RUN apt-get update && apt-get upgrade -y

COPY . .

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn openpyxl

EXPOSE 8050

=======
# syntax=docker/dockerfile:1

FROM python:3.9

RUN apt-get update && apt-get upgrade -y

COPY . .

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn openpyxl

EXPOSE 8050

>>>>>>> 0a31d140 (Initial Commit)
CMD ["python", "app.py"]