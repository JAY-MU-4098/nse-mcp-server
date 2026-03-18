import json
from fastmcp import FastMCP
from main import fast_app
from tools import TOOLS

server = FastMCP.from_fastapi(app=fast_app, name="NSE MCP Server")


for name, tool in TOOLS.items():
    print(f"Registering tool: {name}")
    fn = tool["function"]
    fn.__name__ = name
    fn.__doc__ = tool["description"]
    server.tool(name=name)(fn)

@server.resource("info://server")
def server_info() -> str:
    """Get info about the nse-mcp-server"""
    info = {
        "name": "NSE MCP Server",
        "version": "1.0.0",
        "description": "A MCP Server to get NSE related data",
        "tools": list(TOOLS.keys()),
        "author": "Jay Gogra",
    }

    return json.dumps(info, indent=2)

if __name__ == "__main__":
    server.run(transport="http", host="0.0.0.0", port=8001)
