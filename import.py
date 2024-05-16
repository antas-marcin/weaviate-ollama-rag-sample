from loguru import logger
import json
import weaviate
from weaviate.classes.config import Property, DataType, Configure, ReferenceProperty
from weaviate.classes.query import Filter, QueryReference
from weaviate.classes.data import DataReference
from weaviate.util import generate_uuid5
from weaviate.collections.classes.config import ConsistencyLevel


def import_books():
    with weaviate.connect_to_local() as client:
        _clear_schema(client)
        _create_schema(client)
        _import_data(client)
        logger.success("successfully imported data")


def _clear_schema(client: weaviate.WeaviateClient):
    logger.info("clear schema")
    client.collections.delete_all()


def _create_schema(client: weaviate.WeaviateClient):
    logger.info("create Books collection")
    books = client.collections.create(
        name="Books",
        properties=[
            Property(name="uuid", data_type=DataType.UUID),
            Property(name="author", data_type=DataType.TEXT),
            Property(name="title", data_type=DataType.TEXT),
            Property(name="description", data_type=DataType.TEXT),
            Property(name="genre", data_type=DataType.TEXT),
            Property(name="page_count", data_type=DataType.INT),
        ],
        vectorizer_config=[
            Configure.NamedVectors.text2vec_transformers(
                name="english",
                source_properties=["description"],
                inference_url="http://t2v-transformers-mixedbread-ai-mxbai-embed:8080",
                vectorize_collection_name=False,
                vector_index_config=Configure.VectorIndex.hnsw(
                    quantizer=Configure.VectorIndex.Quantizer.pq(),
                ),
            ),
            Configure.NamedVectors.text2vec_transformers(
                name="multi_lang",
                source_properties=["description"],
                vectorize_collection_name=False,
                vector_index_config=Configure.VectorIndex.flat(),
            ),
        ],
        generative_config=Configure.Generative.ollama(
            api_endpoint="http://generative-ollama:11434",
            model="aya",
        )
    )
    assert books is not None
    assert books.name == "Books"


def _import_data(client: weaviate.WeaviateClient):
    books_json = "data/books.json"
    with open(books_json) as f:
        books = json.load(f)
        logger.info("import {} books", len(books))
        collection = client.collections.get("Books")
        with collection.batch.dynamic() as batch:
            for book in books:
                batch.add_object(properties=book, uuid=book["uuid"])
            batch.flush()


if __name__ == "__main__":
    import_books()
