#!/bin/bash

# scripts/install_models.sh
# Script to install Ollama models used in Cortex

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Checking for Ollama...${NC}"

if ! command -v ollama &> /dev/null; then
    echo -e "${RED}Ollama is not installed. Please install it from https://ollama.com${NC}"
    exit 1
fi

echo -e "${GREEN}Ollama found. Pulling models...${NC}"

# Inference model
echo -e "${GREEN}Pulling mistral-3:3b (Inference)...${NC}"
ollama pull ministral-3:3b

# Embedding model
echo -e "${GREEN}Pulling qwen3-embedding:0.6b (Embeddings)...${NC}"
ollama pull qwen3-embedding:0.6b

echo -e "${GREEN}Models installed successfully!${NC}"
