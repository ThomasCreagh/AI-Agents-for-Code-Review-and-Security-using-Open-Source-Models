#!/bin/bash

./bin/ollama serve &

pid=$!

sleep 5

echo "Pulling models..."
echo "Pulling $EMBEDDING_MODEL"
ollama pull "$EMBEDDING_MODEL"
echo "Pulling $LLM_MODEL"
ollama pull "$LLM_MODEL"

wait $pid
