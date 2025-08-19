FROM ubuntu:24.04

WORKDIR .

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    mysql-client \
    python3 \
    python3-pip \
    wget \
    curl \
    unzip \
    libssh-4 \
    ca-certificates \
    libpython3.10 \
    libncurses6 \
    libstdc++6 \
	libyaml-0-2 \
    gnupg \
    locales && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

# Instalar AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws    

# Define as variáveis de ambiente
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8    

# Copia e instala o mysql-shell
COPY mysql-shell.deb ./mysql-shell.deb
RUN dpkg -i mysql-shell.deb || apt-get install -f -y && rm mysql-shell.deb

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

WORKDIR /app

# Copia o restante da aplicação
COPY app/ .


EXPOSE 8501

# Executa usando caminho absoluto do streamlit
CMD ["streamlit", "run", "main.py"]