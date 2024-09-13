FROM python:3.9-alpine

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=server.py

WORKDIR /app

COPY . /app

# Instaleaza dependintele necesare
RUN apk add --no-cache gcc musl-dev jpeg-dev zlib-dev
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
