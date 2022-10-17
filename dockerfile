FROM python:3.11-rc

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

EXPOSE 5000

ENTRYPOINT ["./docker_entrypoint.sh"]