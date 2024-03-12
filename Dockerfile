FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Create and set the working directory
WORKDIR /fastapi_app

# Install dependencies
COPY requirements.txt /fastapi_app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

EXPOSE 80 
ENV TOGETHER_API_KEY d7e04c2b91cf81b1c6c996bfca2ebcd4ad8a4e4dc515490bfa1fd219bdaf66e9

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
