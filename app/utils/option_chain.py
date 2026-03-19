import pprint

from nse_client import nse

def get_expiry_dates(symbol:str):
    """
    Get expiry dates for an NSE symbol.

    Args:
        symbol (str): NSE symbol like NIFTY or BANKNIFTY

    Returns:
        dict: status and list of expiry dates in YYYY-MM-DD format
    """
    try:
        expiry_dates = nse.options.expiry_dates(symbol.upper())
        return {
            "status": "success",
            "data": expiry_dates
        }
    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }


def get_symbol_info(symbol:str):
    """
    Get all the information of any equity NSE symbol.

    Args:
        symbol (str): NSE symbol like SBIN or BIRLANU
    Returns:
        dict: status and data of symbol
    """
    try:

        result = nse.equity.info(symbol.upper())

        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }


def get_current_price(symbol:str):
    """
        Get current price (underlying price)  for an NSE symbols.

        Args:
            symbol (str): NSE symbol like NIFTY or BANKNIFTY
        Returns:
            dict: status and data where data is the LTP
        """
    try:
        try:
            result = nse.options.option_chain(symbol.upper())[2]
        except:
            result = nse.equity.info(symbol.upper())["priceInfo"]["lastPrice"]

        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }


def get_option_chain_data(symbol:str, expiry_date: str|None=None):
    """
    Get option chain data for an NSE symbol and expiry date.

    Args:
        symbol (str): NSE symbol like NIFTY or BANKNIFTY
        expiry_date (str): expiry date of NSE symbol in YYYY-MM-DD format if not pass then current expiry date will be selected
    Returns:
        dict: status and list of dict where key is strike price and values has dict
    """
    try:

        option_chain = nse.options.option_chain(symbol.upper(), expiry_date=expiry_date)[0]
        result = option_chain.to_dict(orient="records")

        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }


def get_market_status():
    """
    Get current NSE market status across segments.

    Returns:
        dict: status and market status data
    """
    try:
        result = nse.equity.market_status()

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }



def get_all_indices():
    """
    Get all NSE indices data.

    Returns:
        dict: status and list of indices data
    """
    try:
        df = nse.equity.all_indices()
        cols = [
            "index",
            "last",
            "variation",
            "percentChange",
            "open",
            "high",
            "low"
        ]

        df = df[cols]

        return {
            "status": "success",
            "data": df.to_dict(orient="records")
        }

    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }


def get_index_info(index_name: str):
    """
    Get detailed information for a specific NSE index.

    Args:
        index_name (str): Index name like INDIA VIX, NIFTY 50, BANKNIFTY

    Returns:
        dict: status and index data
    """
    try:
        result = nse.equity.find_index(index_name.upper())

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }


def get_delivery_history(symbol: str, from_date: str, to_date: str):
    """
    Get delivery history for a given NSE symbol.

    Args:
        symbol (str): NSE symbol like RELIANCE, SBIN
        from_date (str): Start date in DD-MM-YYYY format
        to_date (str): End date in DD-MM-YYYY format

    Returns:
        dict: status and delivery history data
    """
    try:
        df = nse.equity.delivery_history(
            symbol.upper(),
            from_date,
            to_date
        )

        return {
            "status": "success",
            "data": df.to_dict(orient="records")
        }

    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }


def get_insider_data(symbol: str = None, from_date: str = None, to_date: str = None):
    """
    Get NSE insider trading data.

    Args:
        symbol (str, optional): NSE symbol like INFY, RELIANCE
        from_date (str, optional): Start date in DD-MM-YYYY format
        to_date (str, optional): End date in DD-MM-YYYY format

    Returns:
        dict: status and insider trading data
    """
    try:
        df = nse.insider.insider_data(
            symbol=symbol.upper() if symbol else None,
            from_date=from_date,
            to_date=to_date
        )

        # Convert date columns to string (safe for JSON)
        for col in ["date", "acqfromDt", "acqtoDt", "intimDt"]:
            if col in df.columns:
                df[col] = df[col].astype(str)

        return {
            "status": "success",
            "data": df.to_dict(orient="records")
        }

    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }


def get_pledged_data(symbol: str):
    """
    Get pledged shares data for a given NSE symbol.

    Args:
        symbol (str): NSE symbol like ESCORTS, RELIANCE, INFY

    Returns:
        dict: status and pledged shares data
    """
    try:
        result = nse.insider.getPledgedData(symbol.upper())["data"][0]

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }


def get_sast_data(symbol: str, from_date: str = None, to_date: str = None):
    """
    Get SAST (Substantial Acquisition of Shares) data for an NSE symbol.

    Args:
        symbol (str): NSE symbol like ESCORTS, INFY
        from_date (str, optional): Start date in DD-MM-YYYY format
        to_date (str, optional): End date in DD-MM-YYYY format

    Returns:
        dict: status and SAST data
    """
    try:
        df = nse.insider.getSastData(
            symbol.upper(),
            from_date=from_date,
            to_date=to_date
        )

        # Convert date columns to string
        for col in ["timestamp", "time", "sysTime"]:
            if col in df.columns:
                df[col] = df[col].astype(str)

        return {
            "status": "success",
            "data": df.to_dict(orient="records")
        }

    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }


def get_fno_stocks():
    """
    Get list of all NSE F&O stocks.

    Returns:
        dict: status and list of F&O symbols
    """
    try:
        result = nse.equityOptions.fno_stocks_list()

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }


def get_mf_insider_data(
    from_date: str = None,
    to_date: str = None,
    isin: str = None,
    symbol: str = None
):
    """
    Get Mutual Fund insider trading data.

    Args:
        from_date (str, optional): Start date in DD-MM-YYYY format
        to_date (str, optional): End date in DD-MM-YYYY format
        isin (str, optional): ISIN like INF879O01027
        symbol (str, optional): Mutual fund name like PPFAS Mutual Fund

    Returns:
        dict: status and MF insider data
    """
    try:
        df = nse.mf.mf_insider_data(
            from_date=from_date,
            to_date=to_date,
            isin=isin,
            symbol=symbol
        )

        # Convert datetime columns to string (safe JSON)
        for col in [
            "ebdExchangeDate",
            "ebdSubmissionDate",
            "ebdTransactionDate",
            "ebdCreationDate"
        ]:
            if col in df.columns:
                df[col] = df[col].astype(str)

        return {
            "status": "success",
            "data": df.to_dict(orient="records")
        }

    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }
