FROM python:3.9-alpine

RUN apk update

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

ENV FLASK_APP main.py

COPY . .

RUN python3 db init
RUN python3 db migrate

EXPOSE 5000

ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]
