FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Create and set the working directory
WORKDIR /fastapi_app

# Install dependencies
COPY requirements.txt /fastapi_app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

EXPOSE 10

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10"]
