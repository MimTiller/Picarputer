FROM ubuntu
WORKDIR /carputer
ADD . /carputer

RUN apt update && apt install -y python-kivy python-pip vlc libopencv-dev python-opencv 
RUN pip install mutagen eyed3 futures requests dataset obd kivy-garden

CMD ["python","main.py"]
