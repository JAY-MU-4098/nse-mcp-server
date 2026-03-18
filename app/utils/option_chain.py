from .nse_client import nse

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
