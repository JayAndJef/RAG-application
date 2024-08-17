from dotenv import load_dotenv
import weaviate
import weaviate.classes as wvc
from weaviate.classes.config import Configure
from openai import OpenAI
from keywords import find_keywords
import os

import settings

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

def create_openai_client():
    return OpenAI(api_key=OPENAI_KEY) 

def query_llm(context: list[str], prompt: str, message_history: list[dict[str, str]], openai_client: OpenAI) -> tuple[str, list[dict[str, str]]]:
    """
    Make a history-aware query to the llm given context sentances, the user prompt, and message history. Returns updated message history for 3 messages.
    """
    globbed_text = "\n".join(context)
    assistant_prompt = {"role": "assistant", "content": "The following are sentances of information:\n {}".format(globbed_text)}
    user_prompt = {"role": "user", "content": prompt}
    if len(message_history) > 6:
        total_history = [message_history[0],] + message_history[-4:] + [assistant_prompt, user_prompt]
    else:
        total_history = message_history + [assistant_prompt, user_prompt]

    response = openai_client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=total_history,
    )

    return response.choices[0].message.content, total_history
    

def prompt(client, openai_client: OpenAI, prompt: str, keywords: list[str], message_history: list[dict[str, str]]) -> tuple[str, list[dict[str, str]]]:
    """
    Prompt the model given keywords for near-text search for relevant sentances in the database.
    """
    with client as c:
        texts = c.collections.get("TextChunks")
        response = texts.generate.near_text(
            query=" ".join(keywords),
            limit=5,
        )

        response = [*response.objects]
        response = [r.properties['text'] for r in response] 

    return query_llm(response, prompt, message_history, openai_client) # response and updated chat history



if __name__ == "__main__":
    client = generate_client()

    # with client as c:
    #     c.collections.create(
    #         "TextChunks",
    #         vectorizer_config=[
    #             Configure.NamedVectors.text2vec_openai(
    #                 name="text_vector",
    #                 source_properties=["title"],
    #                 model="text-embedding-3-small",
    #                 dimensions=1536,
    #             )
    #         ],
    #         generative_config=wvc.config.Configure.Generative.openai(),
    #     )

    # add_text(client)

    keywords = find_keywords("where did the narrator dispose of the man's body?", 5)

    print(keywords)

    results = prompt(
        client,
        "Using the information, answer this question: 'where did the narrator dispose of the man's body?'",
        keywords,
    )

    print(results)

        