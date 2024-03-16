FROM apache/airflow:2.8.3

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python" , "-u", "main_async.py"]