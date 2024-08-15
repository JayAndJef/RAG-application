from dotenv import load_dotenv
import weaviate
import weaviate.classes as wvc
from weaviate.classes.config import Configure
import os

load_dotenv()

DATABASE_TOKEN = os.environ["WEAVIATE_KEY"]
OPENAI_KEY = os.environ["OPENAI_KEY"]
DATABASE_URL = os.environ["WEAVIATE_URL"]

def generate_client():
    return weaviate.connect_to_weaviate_cloud(
        cluster_url=DATABASE_URL,             
        auth_credentials=wvc.init.Auth.api_key(DATABASE_TOKEN),
        headers={"X-OpenAI-Api-Key": OPENAI_KEY},
    )

def add_text(client) -> None:
    """
    Adds the full story of 'The Tell-Tale Heart', in sentences
    """
    with client as c:
        with open("tth.txt", "r") as f:
            tth_chunks = f.read().replace("\n", "").split(". ")

            tth_chunks_dict_list = []
            for t in tth_chunks:
                tth_chunks_dict_list.append({"text": t})

            database_collection = c.collections.get("TextChunks")
            database_collection.data.insert_many(tth_chunks_dict_list)

def prompt(client, prompt: str, keywords: list[str]):
    """
    Prompt the model given keywords for near-text search for relevant sentances in the database. Returns a Weaviate object containing details about the response
    """
    with client as c:
        texts = c.collections.get("TextChunks")
        response = texts.generate.near_text(
            query=" ".join(keywords),
            limit=3,
            grouped_task=prompt,
        )

        return response

if __name__ == "__main__":
    client = generate_client()

    with client as c:
        c.collections.create(
            "TextChunks",
            vectorizer_config=[
                Configure.NamedVectors.text2vec_openai(
                    name="text_vector",
                    source_properties=["title"],
                    model="text-embedding-3-small",
                    dimensions=1536,
                )
            ],
            generative_config=wvc.config.Configure.Generative.openai(),
        )

    add_text(client)

        