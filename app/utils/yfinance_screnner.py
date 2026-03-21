from yfinance.screener.screener import EqyQy, FndQy
import yfinance as yf

EQUITY_FIELDS = {
    "epsgrowth.lasttwelvemonths",
    "intradaymarketcap",
    "intradayprice",
    "dayvolume",
    "percentchange",
    "quarterlyrevenuegrowth.quarterly",
    "sector",
    "short_percentage_of_shares_outstanding.value",
    "avgdailyvol3m",
    "eodvolume",
    "peratio.lasttwelvemonths",
    "pegratio_5y",
}


FUND_FIELDS = {
    "categoryname",
    "performanceratingoverall",
    "initialinvestment",
    "annualreturnnavy1categoryrank",
    "riskratingoverall",
    "fundnetassets",
}


OP_MAP = {
    "eq": "EQ",
    "gt": "GT",
    "gte": "GTE",
    "lt": "LT",
    "lte": "LTE",
    "between": "BTWN",
    "in": "IS-IN",
}


PREDEFINED_SCREENERS = {
    "nse_top_gainers": {
        "type": "equity",
        "sortField": "percentchange",
        "sortAsc": False,
        "count": 250,
        "query": {
            "and": [
                {"field": "percentchange", "op": "gt", "value": 2},
                {"field": "dayvolume", "op": "gt", "value": 1000000}
            ]
        }
    },
    "nse_top_losers": {
        "type": "equity",
        "sortField": "percentchange",
        "sortAsc": True,
        "count": 250,
        "query": {
            "and": [
                {"field": "percentchange", "op": "lt", "value": -2},
                {"field": "dayvolume", "op": "gt", "value": 1000000}
            ]
        }
    },
    "nse_undervalued": {
        "type": "equity",
        "sortField": "peratio.lasttwelvemonths",
        "sortAsc": True,
        "count": 250,
        "query": {
            "and": [
                {"field": "peratio.lasttwelvemonths", "op": "lt", "value": 20},
                {"field": "pegratio_5y", "op": "lt", "value": 1}
            ]
        }
    },
    "nse_growth": {
        "type": "equity",
        "sortField": "epsgrowth.lasttwelvemonths",
        "sortAsc": False,
        "count": 250,
        "query": {
            "and": [
                {"field": "epsgrowth.lasttwelvemonths", "op": "gt", "value": 20},
                {"field": "quarterlyrevenuegrowth.quarterly", "op": "gt", "value": 20}
            ]
        }
    },
    "top_mutual_funds": {
        "type": "fund",
        "sortField": "fundnetassets",
        "sortAsc": False,
        "count": 250,
        "query": {
            "and": [
                {"field": "performanceratingoverall", "op": "in", "value": [4, 5]},
                {"field": "riskratingoverall", "op": "lte", "value": 3}
            ]
        }
    }
}


INDEX_MAP = {
    "NIFTY": [ "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK",
                "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BEL", "BHARTIARTL",
                "CIPLA", "COALINDIA", "DRREDDY", "EICHERMOT", "ETERNAL",
                "GRASIM", "HCLTECH", "HDFCBANK", "HDFCLIFE", "HINDALCO",
                "HINDUNILVR", "ICICIBANK", "INDIGO", "INFY", "ITC",
                "JIOFIN", "JSWSTEEL", "KOTAKBANK", "LT", "M&M",
                "MARUTI", "MAXHEALTH", "NESTLEIND", "NTPC", "ONGC",
                "POWERGRID", "RELIANCE", "SBILIFE", "SHRIRAMFIN", "SBIN",
                "SUNPHARMA", "TCS", "TATACONSUM", "TMPV", "TATASTEEL",
                "TECHM", "TITAN", "TRENT", "ULTRACEMCO", "WIPRO"],
    "BANKNIFTY": ["AUBANK", "AXISBANK", "BANDHANBNK", "BANKBARODA", "FEDERALBNK",
                "HDFCBANK", "ICICIBANK", "IDFCFIRSTB", "INDUSINDBK", "KOTAKBANK",
                "PNB", "SBIN", "YESBANK", "CANBK"]
}


def list_predefined_screeners():
    """
    Dict all available predefined screeners with metadata.

    Returns:
        dict[dict]: Each screener includes:
            - key: screener key
            - value : data of the screener
                - type: equity or fund
                - sortField: default sorting field
                - sortAsc: sorting order
                - query: with fields and operator and values

    """
    return {"status": "success", "data": PREDEFINED_SCREENERS}



def _validate_field(field, screener_type):
    if screener_type == "equity" and field not in EQUITY_FIELDS:
        raise ValueError(f"Invalid equity field: {field}")
    if screener_type == "fund" and field not in FUND_FIELDS:
        raise ValueError(f"Invalid fund field: {field}")


def _has_exchange_filter(node):
    if "and" in node or "or" in node:
        key = "and" if "and" in node else "or"
        return any(_has_exchange_filter(n) for n in node[key])
    return node.get("field") == "exchange"


def _build_query(node, screener_type):
    Q = EqyQy if screener_type == "equity" else FndQy

    if "and" in node:
        children = [_build_query(n, screener_type) for n in node["and"]]

        if len(children) == 1:
            return children[0]  # 🔥 FIX: unwrap single condition

        return Q("and", children)

        # ✅ Handle OR
    if "or" in node:
        children = [_build_query(n, screener_type) for n in node["or"]]

        if len(children) == 1:
            return children[0]  # 🔥 FIX

        return Q("or", children)

        # ✅ Leaf node
    field = node["field"]
    op = node["op"].lower()
    value = node["value"]

    _validate_field(field, screener_type)

    if op not in OP_MAP:
        raise ValueError(f"Unsupported operator: {op}")

    if op == "between":
        return Q(OP_MAP[op], [field, value[0], value[1]])

    if op == "in":
        return Q(OP_MAP[op], [field] + value)

    return Q(OP_MAP[op], [field, value])


def run_screener(
    screener_type: str = None,
    query_dict: dict = None,
    predefined: str = None,
    offset: int = 0,
    count: int = None,
    size: int = None,
    sortField: str = None,
    sortAsc: bool = None,
    symbols: list = None,
    index: str = None,
):
    """
    Run a stock or mutual fund screener using Yahoo Finance.

    This tool supports both predefined screeners and fully custom queries
    for equities (NSE) and mutual funds.

    --- Features ---
    • Predefined screeners (ready-to-use strategies)
    • Custom query builder (AND / OR + operators)
    • NSE-only enforcement for equity queries
    • Pagination support (offset, count, size)
    • Sorting support (sortField, sortAsc)
    • Optional filtering by symbols or index (post-processing)

    --- Parameters ---
    screener_type : str, optional
        Type of screener to run:
        • "equity" → Stocks (NSE enforced automatically)
        • "fund" → Mutual funds

    query_dict : dict, optional
        Custom query in structured format.

        Example:
        {
            "and": [
                {"field": "percentchange", "op": "gt", "value": 2},
                {"field": "dayvolume", "op": "gt", "value": 100000}
            ]
        }

        Supported operators:
        • eq   → equals
        • gt   → greater than
        • gte  → greater than or equal
        • lt   → less than
        • lte  → less than or equal
        • between → range [min, max]
        • in   → list of values
        • and / or → logical grouping

    predefined : str, optional
        Name of predefined screener.

        Available options:
        • "nse_top_gainers"
        • "nse_top_losers"
        • "nse_undervalued"
        • "nse_growth"
        • "nse_high_volume"
        • "top_mutual_funds"
        • "low_risk_funds"

    offset : int, optional (default=0)
        Number of results to skip (for pagination).

    count : int, optional
        Number of results to return (max 250).

    size : int, optional
        Alternative to count (Yahoo API compatibility).

    sortField : str, optional
        Field to sort results by (e.g., "percentchange", "dayvolume").

    sortAsc : bool, optional
        Sorting order:
        • True  → ascending
        • False → descending

    symbols : list[str], optional
        Filter results for specific stock symbols.
        Supports partial match (e.g., "RELIANCE" matches "RELIANCE.NS").

    index : str, optional
        Filter results by index (e.g., "NIFTY50", "BANKNIFTY").
        Applied after screener results.

    --- Returns ---
    list[dict]
        List of matching instruments with normalized fields:

        • symbol → Stock ticker (e.g., RELIANCE.NS)
        • price → Current market price
        • change_percent → % price change
        • volume → Trading volume

    --- Notes ---
    • Equity queries are automatically restricted to NSE (exchange = "NSI").
    • Some fields may not be available for all NSE stocks due to Yahoo limitations.
    • Symbol and index filters are applied after fetching results.

    --- Examples ---

    Predefined screener:
        run_screener(predefined="nse_top_gainers")

    Custom equity screener:
        run_screener(
            screener_type="equity",
            query_dict={
                "and": [
                    {"field": "percentchange", "op": "gt", "value": 2},
                    {"field": "dayvolume", "op": "gt", "value": 100000}
                ]
            }
        )

    Custom fund screener:
        run_screener(
            screener_type="fund",
            query_dict={
                "and": [
                    {"field": "performanceratingoverall", "op": "in", "value": [4, 5]},
                    {"field": "riskratingoverall", "op": "lte", "value": 3}
                ]
            }
        )

    Filter by index:
    run_screener(
        predefined="nse_top_gainers",
        index="NIFTY50"
    )

    Filter by symbols:
        run_screener(
            predefined="nse_top_gainers",
            symbols=["RELIANCE", "TCS"]
        )
    """
    try:
        if predefined:
            config = PREDEFINED_SCREENERS[predefined]

            screener_type = config["type"]
            query_dict = config["query"]

            # Apply defaults if not provided
            if count is None:
                count = config.get("count", 25)

            if sortField is None:
                sortField = config.get("sortField")

            if sortAsc is None:
                sortAsc = config.get("sortAsc")

        if not screener_type or not query_dict:
            raise ValueError("Provide either predefined or (screener_type + query_dict)")


        query = _build_query(query_dict, screener_type)


        if screener_type == "equity":
            if not _has_exchange_filter(query_dict):
                query = EqyQy("and", [
                    EqyQy("eq", ["exchange", "NSI"]),
                    query
                ])

        if index or symbols:
            count = 250
            size = 250

        result = yf.screen(
            query,
            offset=offset,
            count=count,
            size=size,
            sortField=sortField,
            sortAsc=sortAsc
        )

        quotes = result.get("quotes", [])

        if index:
            index_symbols = set(INDEX_MAP.get(index, []))

            modified_symbols = list(map(lambda x :  x + ".NS", index_symbols))
            print(modified_symbols)
            print(quotes)
            quotes = [
                q for q in quotes
                if q.get("symbol", "") in modified_symbols
            ]

        if symbols:
            modified_symbols = [f"{s}.NS" for s in symbols]
            quotes = [
                q for q in quotes
                if q.get("symbol") in modified_symbols
            ]

        filter_data = [
                {
                "symbol": q.get("symbol").replace(".NS", ""),
                "price": q.get("regularMarketPrice"),
                "change_percent": q.get("regularMarketChangePercent"),
                "change": q.get("regularMarketChange"),
                "previous_close": q.get("regularMarketPreviousClose"),
                "volume": q.get("regularMarketVolume"),
            } for q in quotes
        ]

        return {
            "status": "success",
            "data": quotes
        }

    except Exception as e:
        print(f"here : {e}")
        return {"status": "fail", "data": str(e)}
