from utils.option_chain import get_expiry_dates, get_option_chain_data, get_current_price, get_symbol_info, \
    get_market_status, get_all_indices, get_index_info, get_delivery_history, get_insider_data, get_pledged_data, \
    get_sast_data, get_fno_stocks, get_mf_insider_data


def get_description(func):
    if not func.__doc__:
        return "No description available"
    return func.__doc__.strip()


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
    "get_market_status": {
        "function": get_market_status,
        "description": get_description(get_market_status),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    "get_all_indices": {
        "function": get_all_indices,
        "description": get_description(get_all_indices),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    "get_index_info": {
        "function": get_index_info,
        "description": get_description(get_index_info),
        "input_schema": {
            "type": "object",
            "properties": {
                "index_name": {
                    "type": "string",
                    "description": "Index name like INDIA VIX, NIFTY 50, BANKNIFTY, etc"
                }
            },
            "required": ["index_name"]
        }
    },
    "get_delivery_history": {
        "function": get_delivery_history,
        "description": get_description(get_delivery_history),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "NSE symbol like RELIANCE, SBIN, TCS, etc"
                },
                "from_date": {
                    "type": "string",
                    "description": "Start date in DD-MM-YYYY format (e.g., 01-03-2026)"
                },
                "to_date": {
                    "type": "string",
                    "description": "End date in DD-MM-YYYY format (e.g., 18-03-2026)"
                }
            },
            "required": ["symbol", "from_date", "to_date"]
        }
    },
    "get_insider_data": {
        "function": get_insider_data,
        "description": get_description(get_insider_data),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "NSE symbol like INFY, RELIANCE (optional)"
                },
                "from_date": {
                    "type": "string",
                    "description": "Start date in DD-MM-YYYY format (optional)"
                },
                "to_date": {
                    "type": "string",
                    "description": "End date in DD-MM-YYYY format (optional)"
                }
            },
            "required": []
        }
    },
    "get_pledged_data": {
        "function": get_pledged_data,
        "description": get_description(get_pledged_data),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "NSE symbol like ESCORTS, RELIANCE, INFY, etc"
                }
            },
            "required": ["symbol"]
        }
    },
    "get_sast_data": {
        "function": get_sast_data,
        "description": get_description(get_sast_data),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "NSE symbol like ESCORTS, INFY, RELIANCE"
                },
                "from_date": {
                    "type": "string",
                    "description": "Start date in DD-MM-YYYY format (optional)"
                },
                "to_date": {
                    "type": "string",
                    "description": "End date in DD-MM-YYYY format (optional)"
                }
            },
            "required": ["symbol"]
        }
    },
    "get_fno_stocks": {
        "function": get_fno_stocks,
        "description": get_description(get_fno_stocks),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    "get_mf_insider_data": {
        "function": get_mf_insider_data,
        "description": get_description(get_mf_insider_data),
        "input_schema": {
            "type": "object",
            "properties": {
                "from_date": {
                    "type": "string",
                    "description": "Start date in DD-MM-YYYY format (optional)"
                },
                "to_date": {
                    "type": "string",
                    "description": "End date in DD-MM-YYYY format (optional)"
                },
                "isin": {
                    "type": "string",
                    "description": "ISIN like INF879O01027 (optional)"
                },
                "symbol": {
                    "type": "string",
                    "description": "Mutual fund name like PPFAS Mutual Fund (optional)"
                }
            },
            "required": []
        }
    },
}
