from loguru import logger
import json, sys
import weaviate
from weaviate.classes.config import Property, DataType, Configure, ReferenceProperty
from weaviate.classes.query import Filter, QueryReference
from weaviate.classes.data import DataReference
from weaviate.util import generate_uuid5
from weaviate.collections.classes.config import ConsistencyLevel
from weaviate.classes.init import AdditionalConfig, Timeout


def run_queries():
    with weaviate.connect_to_local(
        additional_config=AdditionalConfig(timeout=Timeout(init=2, query=300, insert=120)),
    ) as client:
        _embedding_models(client)
        _gen_ai_tweet(client)
        _gen_ai_translate(client)


def _embedding_models(client: weaviate.WeaviateClient):
    logger.debug("1. Difference between single and multi lingual embedding models")

    query_pl="Miłość sióstr w czasach drugiej wojny światowej"
    query_en="Sister's love during world war 2"

    logger.warning("Looking for data using a query written in polish language: \"{}\"", query_pl)
    logger.warning("An appropriate result should be The Nightingale ")
    logger.warning("- asking for results english only embedding model result:")
    books = client.collections.get("Books")
    res = books.query.near_text(query=query_pl, limit=1, target_vector="english", return_properties="description")
    found_description = res.objects[0].properties.get("description")
    logger.success("{}", found_description)
    logger.warning("- asking for results multi lingual embedding model result:")
    res = books.query.near_text(query=query_pl, limit=1, target_vector="multi_lang", return_properties="description")
    found_description = res.objects[0].properties.get("description")
    logger.success("{}", found_description)
    logger.warning("- asking for results english embedding model, this time using query in english: \"{}\" results:", query_en)
    res = books.query.near_text(query=query_en, limit=1, target_vector="english", return_properties="description")
    found_description = res.objects[0].properties.get("description")
    logger.success("{}", found_description)


def _gen_ai_tweet(client: weaviate.WeaviateClient):
    logger.debug("2a. Simple RAG presentation 1")
    prompt ="""
    Napisz krótkiego tweeta rekomendującego książkę {title} autorstwa {author}, użyj emotikonek i hashtagów,
    napisz go w języku francuskim, użyj do tego poniższego opisu:
    {description}"""

    logger.warning("Generating response from a LLM may take some time as the model is running locally...")
    logger.warning("Sending prompt:")
    logger.success("{}", prompt)

    books = client.collections.get("Books")
    result = books.generate.near_text(
        query="Miłość sióstr w czasach drugiej wojny światowej",
        target_vector="multi_lang",
        limit=1,
        single_prompt=prompt
    )

    for obj in result.objects:
        logger.warning("Received answer:")
        logger.success("{}", obj.generated)


def _gen_ai_translate(client: weaviate.WeaviateClient):
    logger.debug("2b. Simple RAG presentation 2")
    prompt ="""
    Please translate given description to Spanish:
    "{description}\""""

    logger.warning("Generating response from a LLM may take some time as the model is running locally...")
    logger.warning("Sending prompt:")
    logger.success("{}", prompt)

    books = client.collections.get("Books")
    result = books.generate.near_text(
        query="Miłość sióstr w czasach drugiej wojny światowej",
        target_vector="multi_lang",
        limit=1,
        single_prompt=prompt
    )

    for obj in result.objects:
        logger.warning("Received answer:")
        logger.success("{}", obj.generated)


if __name__ == "__main__":
    run_queries()