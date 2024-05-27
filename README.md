# Weaviate Ollama Simple RAG

🎯 Overview
-----------

This is a simple demo of how one can run Weaviate with Ollama modules and create simple RAG.

📦 Requirements
----------------

In order to be able to create Weaviate one needs at least.

1. Docker
2. Python3

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

In order to run the python scripts, it's advised to setup a venv for a project.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

In order to import data issue:

```sh
python3 import.py
```

🔍 Search
----------

Data in this example has been vectorized using 2 embedding models (english only and multi lingual). Their target vector names are respectively `english` and `multi_lang`. Those 2 examples below shows a difference in querying english data using polish language and using 2 different target vectors:
 - [query_in_pl_using_english_model.gql](./graphql/query_in_pl_using_english_model.gql)
 - [query_in_pl_using_multi_lang_model.gql](./graphql/query_in_pl_using_multi_lang_model.gql)

📖 Prompts
----------

Create a tweet prompt ([generate_tweet.gql](./graphql/generate_tweet.gql)):

```
Use lot's of emojis to create a short (max 15 words) and passionate tweet in English language recommending a book from {author}, add hashtags at the end of the tweet, use this description: {description}
```

🤖 Code samples
---------------

All of those examples can be also executed using python scripts. If you haven't imported data issue:

```sh
python3 import.py
```

in order to perfom search queries and run RAG samples issue:

```sh
python3 query.py
```
