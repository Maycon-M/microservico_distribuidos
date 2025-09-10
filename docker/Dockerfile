# Dockerfile
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=America/Sao_Paulo

WORKDIR /app

# Dependências de build e libpq (para psycopg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Se usar requirements.txt
COPY requirements.txt /app/
RUN pip install --upgrade pip \
  && pip install -r requirements.txt

# Se preferir pinar aqui (ex.: psycopg[binary]) e deixar o req menor:
RUN pip install --upgrade pip \
 && pip install "psycopg[binary]==3.*" gunicorn uvicorn fastapi

# Copia o restante do projeto
COPY . /app

# Porta interna
EXPOSE 8080

# Gunicorn + UvicornWorker (ajuste o módulo conforme seu projeto)
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "src.main.server.server:app", "--bind", "0.0.0.0:8080", "--workers", "2"]


# docker build -t api_equipement_manager -f docker/Dockerfile .
# docker run -d -p 8080:8080 --env-file .env --name api_equipement_manager_container api_equipement_manager