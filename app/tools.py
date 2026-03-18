from utils.option_chain import get_expiry_dates

def get_description(func):
    if not func.__doc__:
        return "No description available"
    return func.__doc__.strip().split("\n")[0]


TOOLS = {
    "get_expiry_dates": {
        "function": get_expiry_dates,
        "description": get_description(get_expiry_dates),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "NSE symbol like NIFTY, SBIN, BANKNIFTY, etc"
                }
            },
            "required": ["symbol"]
        }
    }
}