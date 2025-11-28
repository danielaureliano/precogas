# Usar uma imagem base oficial do Python leve
FROM python:3.10-slim

# Definir variáveis de ambiente
# Impede o Python de escrever arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Garante que a saída do Python seja enviada diretamente para o terminal/logs
ENV PYTHONUNBUFFERED=1

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o arquivo de requisitos
COPY requirements.txt .

# Instalar as dependências do Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código do projeto
COPY . .

# Criar diretório para dados temporários se não existir (embora o volume/código possa tratar isso)
RUN mkdir -p dados_anp

# Expor a porta que a aplicação usa
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
