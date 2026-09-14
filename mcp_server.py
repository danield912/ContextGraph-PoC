import os

from dotenv import load_dotenv
from mcp.server import MCPServer

from graphiti_core import Graphiti
from graphiti_core.llm_client.gemini_client import GeminiClient, LLMConfig
from graphiti_core.embedder.gemini import (
    GeminiEmbedder,
    GeminiEmbedderConfig,
)
from graphiti_core.cross_encoder.gemini_reranker_client import (
    GeminiRerankerClient,
)


load_dotenv()

mcp = MCPServer("ContextGraph")


def create_graphiti():
    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USER")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not gemini_key:
        raise ValueError("GEMINI_API_KEY is missing from .env")

    return Graphiti(
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

        max_coroutines=1,
    )


@mcp.tool()
async def search_context(query: str) -> str:
    """
    Search the ContextGraph knowledge graph for information.
    """

    graphiti = create_graphiti()

    try:
        results = await graphiti.search(query)

        if not results:
            return "No matching information was found."

        facts = []

        for result in results[:5]:
            facts.append(result.fact)

        return "\n".join(facts)

    finally:
        await graphiti.close()