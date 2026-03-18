import asyncio
from fastmcp.client import Client

async def main():
    # Define the server parameters (default is localhost:8000)
    client = Client("http://localhost:8001/mcp")

    # Initialize the client session
    async with client:
        # Discover server capabilities
        await client.initialize()
        tools = await client.list_tools()
        print(f"Available tools: {tools}")

        result = await client.call_tool(
            "get_expiry_dates",
            {"symbol": "NIFTY"}
        )

        print("\nTOOL RESULT:")
        print(result)



if __name__ == "__main__":
    asyncio.run(main())
