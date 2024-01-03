FROM python:3.10

WORKDIR /app

COPY . . 

EXPOSE 8080

RUN pip install -r requirements.txt

CMD ["python", "app.py", "--port", "8080"]