FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# код для запуска контейнера
# адрес для запуска: http://localhost:8000/docs
# docker build -t spam-detector .
# docker run -p 8000:8000 spam-detector