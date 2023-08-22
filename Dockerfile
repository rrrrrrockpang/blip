FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR .

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 3100

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
