#!/bin/bash
set -e

echo "[INIT] Updating system repositories..."
sudo apt-get update -y

echo "[INSTALL] Ingesting low-level C++ toolchain and IPC prerequisites..."
sudo apt-get install -y \
    build-essential \
    cmake \
    clang-format \
    protobuf-compiler \
    libprotobuf-dev \
    protobuf-compiler-grpc \
    libgrpc++-dev \
    python3-pip \
    python3-dev

echo "[INSTALL] Building Python virtual environment and dependencies..."
python3 -m pip install --upgrade pip
pip3 install \
    grpcio \
    grpcio-tools \
    protobuf \
    pydantic \
    chromadb \
    mcp

echo "[SUCCESS] Environment configuration for Project PHALANX complete."
