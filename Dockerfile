FROM python:3.11.3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "cd fastapi && uvicorn app.main:app --host 0.0.0.0 --port 8000"]