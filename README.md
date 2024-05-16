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

Pull [Aya](https://cohere.com/research/aya) model. It's an open source multi linugal large language model from Cohere. Please note that you need at least 5GB of free space on your disk.

```sh
docker exec -i generative-ollama ollama pull aya
```

Prompts
---------

Create a tweet prompt:

```
Create a tweet recommending a book from {author} - {title} using this description below. Use hashtags and emojis.
```
