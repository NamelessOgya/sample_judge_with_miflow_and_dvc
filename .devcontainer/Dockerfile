# Ubuntu 22.04 ベース
FROM ubuntu:22.04

# 必要なツールとPython 3.10のインストール
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
        python3.10 \
        python3.10-venv \
        python3.10-dev \
        python3-pip \
        curl \
        git \
        build-essential \
        sudo \
        ca-certificates \
        && apt-get clean && rm -rf /var/lib/apt/lists/*

# pipをアップグレード
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 && \
    python -m pip install --upgrade pip

# vscode用ユーザーの作成
ARG USERNAME=vscode
RUN useradd -m -s /bin/bash ${USERNAME} && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 作業ディレクトリ
WORKDIR /workspace

USER vscode

# poetry install
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/home/vscode/.local/bin:$PATH"
