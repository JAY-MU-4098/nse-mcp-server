from utils.option_chain import get_expiry_dates, get_option_chain_data, get_current_price, get_symbol_info


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
    },
    "get_option_chain_data": {
        "function": get_option_chain_data,
        "description": get_description(get_option_chain_data),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "NSE symbol like NIFTY, SBIN, BANKNIFTY, etc"
                },
                "expiry_date": {
                    "type": "string",
                    "description": "NSE expiry date in YYYY-MM-DD format."
                }
            },
            "required": ["symbol"]
        }
    },
    "get_current_price": {
        "function": get_current_price,
        "description": get_description(get_current_price),
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
    },
    "get_symbol_info": {
        "function": get_symbol_info,
        "description": get_description(get_symbol_info),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Equity NSE symbol like SBIN or BIRLANU"
                }
            },
            "required": ["symbol"]
        }
    },
}