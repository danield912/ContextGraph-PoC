import asyncio
from mcp import Client


async def main():

    async with Client("http://localhost:8000/mcp") as client:

        print("Connected to ContextGraph MCP server!")

        result = await client.call_tool(
            "search_context",
            {
                "query": "What project is Daniel working on?"
            }
        )

        print()
        print("MCP RESULT:")
        print("-----------")
        print(result.structured_content)


if __name__ == "__main__":
    asyncio.run(main())