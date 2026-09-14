import asyncio
import os
from datetime import datetime, timezone

from dotenv import load_dotenv

from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType

from graphiti_core.llm_client.gemini_client import (
    GeminiClient,
    LLMConfig,
)

from graphiti_core.embedder.gemini import (
    GeminiEmbedder,
    GeminiEmbedderConfig,
)

from graphiti_core.cross_encoder.gemini_reranker_client import (
    GeminiRerankerClient,
)


load_dotenv()


async def main():

    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USER")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not gemini_key:
        raise ValueError("GEMINI_API_KEY is missing from .env")

    print("Connecting to Graphiti...")

    graphiti = Graphiti(
        neo4j_uri,
        neo4j_user,
        neo4j_password,

        llm_client=GeminiClient(
            config=LLMConfig(
                api_key=gemini_key,
                model="gemini-3.5-flash-lite",
            )
        ),

        embedder=GeminiEmbedder(
            config=GeminiEmbedderConfig(
                api_key=gemini_key,
                embedding_model="gemini-embedding-001",
            )
        ),

        cross_encoder=GeminiRerankerClient(
            config=LLMConfig(
                api_key=gemini_key,
                model="gemini-3.5-flash-lite",
            )
        ),
    )

    try:
        print("Setting up Graphiti!")
        await graphiti.build_indices_and_constraints()
        print("Reading sample.txt...")

        with open("sample.txt", "r", encoding="utf-8") as file:
            text = file.read()

        print("Adding document to knowledge graph...")

        await graphiti.add_episode(
            name="ContextGraph Sample Document",
            episode_body=text,
            source=EpisodeType.text,
            source_description="Sample uploaded text document",
            reference_time=datetime.now(timezone.utc),
        )

        print("Document added!")

        question = "What project is Daniel working on?"

        print()
        print("Searching for:")
        print(question)

        results = await graphiti.search(question)

        print()
        print("RESULTS:")
        print("--------")

        if not results:
            print("No results found.")

        for result in results:
            print(result.fact)

    finally:
        await graphiti.close()
        print()
        print("Connection closed.")


if __name__ == "__main__":
    asyncio.run(main())