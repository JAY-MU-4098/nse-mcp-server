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