import uvicorn
from fastapi import FastAPI
from tools import TOOLS

fast_app = FastAPI()


@fast_app.get("/health")
def health():
    return {"status": "ok"}


@fast_app.get("/tools")
def list_tools():
    return [
        {
            "name": name,
            "description": tool["description"],
            "input_schema": tool["input_schema"],

        }
        for name, tool in TOOLS.items()
    ]


@fast_app.post("/execute")
def execute_tool(payload: dict):
    tool_name = payload.get("tool")
    params = payload.get("params", {})

    tool = TOOLS.get(tool_name)

    if not tool:
        return {
            "status": "fail",
            "data": f"tool '{tool_name}' not found. valid tools: {list(TOOLS.keys())}"
        }

    try:
        return tool["function"](**params)
    except TypeError as e:
        return {
            "status": "fail",
            "data": f"Invalid parameters: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }


if __name__ == "__main__":
    uvicorn.run(fast_app, host="0.0.0.0", port=8000)