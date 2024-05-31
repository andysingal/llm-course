FROM python:3.10-slim-buster

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5007

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5007"]
