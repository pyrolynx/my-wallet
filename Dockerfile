FROM python:3.7-stretch

WORKDIR /opt

EXPOSE 8080

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "main.py"]
