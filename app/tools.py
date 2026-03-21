from utils.pnsea_lib import get_expiry_dates, get_option_chain_data, get_current_price, get_symbol_info, \
    get_market_status, get_all_indices, get_index_info, get_delivery_history, get_insider_data, get_pledged_data, \
    get_sast_data, get_fno_stocks, get_mf_insider_data

from utils.yfinance_screnner import run_screener, list_predefined_screeners

from utils.yfinance_lib import get_financials, get_esg_data, get_holders_data, get_historical_data, get_full_stock_data, \
    get_stock_news, get_balance_sheet_data, get_analyst_insights, get_insider_activity, get_corporate_actions, \
    get_earnings_calendar, get_earnings_forecast, get_company_profile


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

    "list_predefined_screeners": {
        "function": list_predefined_screeners,
        "description": "List all available predefined stock and mutual fund screeners with details",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },

    "run_screener": {
        "function": run_screener,
        "description": get_description(run_screener),
        "input_schema": {
            "type": "object",
            "properties": {
                "screener_type": {
                    "type": "string",
                    "enum": ["equity", "fund"],
                    "description": "Type of screener: 'equity' for NSE stocks, 'fund' for mutual funds"
                },
                "query_dict": {
                    "type": "object",
                    "description": "Custom query in structured format using AND/OR and operators like gt, lt, eq, in, between"
                },
                "predefined": {
                    "type": "string",
                    "enum": [
                        "nse_top_gainers",
                        "nse_top_losers",
                        "nse_undervalued",
                        "nse_growth",
                        "top_mutual_funds"
                    ],
                    "description": "Predefined screener name"
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of results to skip (pagination)",
                    "default": 0
                },
                "count": {
                    "type": "integer",
                    "description": "Number of results to return (max 250)"
                },
                "size": {
                    "type": "integer",
                    "description": "Alternative to count (Yahoo API compatibility)"
                },
                "sortField": {
                    "type": "string",
                    "description": "Field to sort results (e.g., percentchange, dayvolume)"
                },
                "sortAsc": {
                    "type": "boolean",
                    "description": "Sort ascending if true, descending if false"
                },
                "symbols": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Filter results for specific symbols (prefix match, e.g., RELIANCE)"
                },
                "index": {
                    "type": "string",
                    "description": "Filter results by index (e.g., NIFTY, BANKNIFTY)"
                }
            },
            "required": []
        }
    },
    "get_historical_data": {
        "function": get_historical_data,
        "description": get_description(get_historical_data),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol like RELIANCE, TCS, INFY (NSE supported)"
                },
                "interval": {
                    "type": "string",
                    "description": "Data interval (e.g., 1m, 5m, 15m, 1h, 1d)",
                    "default": "1d"
                },
                "period": {
                    "type": "string",
                    "description": "Time period (e.g., 1d, 5d, 1mo, 6mo, 1y, max)",
                    "default": "1mo"
                }
            },
            "required": ["symbol"]
        }
    },

    "get_company_profile": {
        "function": get_company_profile,
        "description": get_description(get_company_profile),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol like RELIANCE, INFY, SBIN"
                }
            },
            "required": ["symbol"]
        }
    },

    "get_financials": {
        "function": get_financials,
        "description": get_description(get_financials),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol for financial statements"
                }
            },
            "required": ["symbol"]
        }
    },

    "get_stock_news": {
        "function": get_stock_news,
        "description": get_description(get_stock_news),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol to fetch latest news"
                }
            },
            "required": ["symbol"]
        }
    },

    "get_holders_data": {
        "function": get_holders_data,
        "description": get_description(get_holders_data),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol to get ownership details"
                }
            },
            "required": ["symbol"]
        }
    },

    "get_insider_activity": {
        "function": get_insider_activity,
        "description": get_description(get_insider_activity),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol to get insider trading activity"
                }
            },
            "required": ["symbol"]
        }
    },

    "get_corporate_actions": {
        "function": get_corporate_actions,
        "description": get_description(get_corporate_actions),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol to get dividends, splits, and corporate actions"
                }
            },
            "required": ["symbol"]
        }
    },

    "get_earnings_calendar": {
        "function": get_earnings_calendar,
        "description": get_description(get_earnings_calendar),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol to get earnings and events calendar"
                }
            },
            "required": ["symbol"]
        }
    },

    "get_analyst_insights": {
        "function": get_analyst_insights,
        "description": get_description(get_analyst_insights),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol to get analyst ratings and price targets"
                }
            },
            "required": ["symbol"]
        }
    },

    "get_earnings_forecast": {
        "function": get_earnings_forecast,
        "description": get_description(get_earnings_forecast),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol to get earnings estimates and trends"
                }
            },
            "required": ["symbol"]
        }
    },

    "get_esg_data": {
        "function": get_esg_data,
        "description": get_description(get_esg_data),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol to get ESG (Environmental, Social, Governance) scores"
                }
            },
            "required": ["symbol"]
        }
    },

    "get_full_stock_data": {
        "function": get_full_stock_data,
        "description": get_description(get_full_stock_data),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol to get complete data (price, fundamentals, news, etc.)"
                }
            },
            "required": ["symbol"]
        }
    },

    "get_balance_sheet_data": {
        "function": get_balance_sheet_data,
        "description": get_description(get_balance_sheet_data),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol to get balance sheet and financial ratios"
                }
            },
            "required": ["symbol"]
        }
    }

}
