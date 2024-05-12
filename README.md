# Weaviate Ollama Simple RAG

🎯 Overview
-----------

This is a simple demo of how one can run Weaviate with Ollama modules and create simple RAG.

📦 Requirements
----------------

In order to be able to create Weaviate one needs at least.

1. docker

💡 Running
----------

In order to run the setup one needs to issue:

```sh
docker compose up -d
```

Please note that below operations take some time to succeed.

Pull vectorizer model. Please note that you need at least 300MB of free space on your disk.

```sh
docker exec -i text2vec-ollama /bin/ollama pull nomic-embed-text
```

Pull llama3 model. Please note that you need at least 5GB of free space on your disk.

```sh
docker exec -i generative-ollama /bin/ollama pull llama3
```