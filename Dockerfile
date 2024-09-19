FROM python:3.9

WORKDIR /app
COPY . /app
EXPOSE 8080
ENV NAME=World

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "main.py"]