#!/bin/sh

echo "Esperando o banco de dados iniciar..."
until pg_isready -h localhost -p 5432; do
    sleep 2
done

echo "Executando as migrações..."
alembic upgrade head

echo "Executando os testes..."
pytest tests.py

echo "Iniciando o servidor FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8080
