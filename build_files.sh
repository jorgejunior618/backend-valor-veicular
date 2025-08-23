#!/usr/bin/env bash
echo "🚀 Iniciando build otimizado para Vercel..."
echo "=============================================="

echo "📦 Dependências já instaladas pelo pip..."

echo "🧹 Iniciando limpeza agressiva..."

find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
find . -name "*.pyd" -delete 2>/dev/null || true

find . -name "*.dist-info" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true

rm -rf pip 2>/dev/null || true
rm -rf setuptools 2>/dev/null || true
rm -rf wheel 2>/dev/null || true
rm -rf _virtualenv* 2>/dev/null || true

echo "🔍 Limpando pacotes específicos..."

# Limpeza do scikit-learn
find . -path "*/sklearn/datasets/data*" -type d -exec rm -rf {} + 2>/dev/null || true
find . -path "*/sklearn/datasets/descr*" -type d -exec rm -rf {} + 2>/dev/null || true
find . -path "*/sklearn/benchmarks*" -type d -exec rm -rf {} + 2>/dev/null || true
find . -path "*/sklearn/tests*" -type d -exec rm -rf {} + 2>/dev/null || true

# Limpeza do numpy
find . -path "*/numpy/doc*" -type d -exec rm -rf {} + 2>/dev/null || true
find . -path "*/numpy/test*" -type d -exec rm -rf {} + 2>/dev/null || true

# Limpeza do Django
find . -path "*/django/contrib/admin/static*" -type d -exec rm -rf {} + 2>/dev/null || true
find . -path "*/django/contrib/gis*" -type d -exec rm -rf {} + 2>/dev/null || true
find . -path "*/django/test*" -type d -exec rm -rf {} + 2>/dev/null || true

echo "✅ Limpeza concluída!"
echo "📊 Espaço liberado:"

# Mostra tamanho dos maiores diretórios
echo "Maiores diretórios:"
du -sh ./* | sort -hr | head -10

echo "=============================================="
echo "🚀 Build pronto para deploy no Vercel!"