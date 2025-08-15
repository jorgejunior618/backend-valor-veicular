#!/usr/bin/env bash

echo "[BUILD PHASE]: Instalando django ..."
python3 -m pip install django

echo "[BUILD PHASE]: Instalando rest_framework ..."
python3 -m pip install djangorestframework

echo "[BUILD PHASE]: Instalando django-cors-headers ..."
python3 -m pip install django-cors-headers

echo "[BUILD PHASE]: Migrando banco de dados..."
# python3 manage.py makemigrations --noinput
# python3 manage.py migrate --noinput

echo "[BUILD PHASE]: Coletando arquivos estáticos..."
# python3 manage.py collectstatic --noinput
