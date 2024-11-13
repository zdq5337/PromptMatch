from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.vectorstores import VectorStore
from langchain_postgres.vectorstores import PGVector

from setting import config


def generation_pgvector() -> VectorStore:
    connection = config['rag']['vector']['pg-vector']['url']     # Uses psycopg3!
    collection_name = "docs"
    embeddings = HuggingFaceEmbeddings(
        model_name="shibing624/text2vec-base-chinese",
        cache_folder=config['embedding-model']['text2vec-base-chinese']['model-path'],
        show_progress=True,
    )

    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=connection,
        use_jsonb=True,
    )
    return vectorstore
