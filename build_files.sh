#!/usr/bin/env bash

echo "[BUILD PHASE]: Baixando dependencias ..."
python3 -m pip install -r requirements.txt

# echo "[BUILD PHASE]: Migrando banco de dados..."
# python3 manage.py makemigrations --noinput
# python3 manage.py migrate --noinput

echo "[BUILD PHASE]: Coletando arquivos estáticos..."
python3 manage.py collectstatic --noinput --clear
