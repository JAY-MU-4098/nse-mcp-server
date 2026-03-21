import pandas as pd
import yfinance as yf


def _resolve_symbol(symbol: str):
    """
    Convert a user-given name or symbol into a valid Yahoo Finance ticker.

    It searches Yahoo Finance and returns the best matching symbol.
    """
    sym = yf.Search(symbol)
    quotes = list(filter(lambda x : x["exchange"] == "NSI" and x["symbol"].startswith(symbol.upper()), sym.quotes))

    if not quotes:
        raise ValueError("No matching symbol found")

    return quotes[0]["symbol"]


def get_historical_data(symbol: str, interval: str = "1d", period: str = "1mo"):
    """
    Get historical market data (OHLCV) for a stock, index, crypto, or forex.

    - interval: data frequency (e.g., 1m, 5m, 1h, 1d)
    - period: how much past data to fetch (e.g., 1d, 1mo, 1y, max)

    Returns price candles including open, high, low, close, and volume.
    """
    try:
        y_symbol = _resolve_symbol(symbol)
        ticker = yf.Ticker(y_symbol)

        df = ticker.history(interval=interval, period=period)

        if df.empty:
            return {"status": "fail", "data": "No data found"}

        df.reset_index(inplace=True)

        return {
            "status": "success",
            "data": {
                "symbol": symbol,
                "candles": df.to_dict(orient="records")
            }
        }

    except Exception as e:
        return {"status": "fail", "data": str(e)}


def get_company_profile(symbol: str):
    """
    Get basic company or asset information.

    Includes details like name, sector, industry, market cap,
    valuation metrics (PE ratio), and official website.
    """
    try:
        y_symbol = _resolve_symbol(symbol)
        ticker = yf.Ticker(y_symbol)
        info = ticker.info
        other_info = yf.Search(y_symbol).all

        return {
            "status": "success",
            "data": {**info, **other_info},
        }

    except Exception as e:
        return {"status": "fail", "data": str(e)}


def get_financials(symbol: str):
    """
    Get financial statements of a company.

    Includes:
    - Income statement (revenue, profit, etc.)
    - Balance sheet (assets, liabilities)
    - Cash flow (cash movements)

    Useful for fundamental analysis.
    """
    try:
        y_symbol = _resolve_symbol(symbol)
        ticker = yf.Ticker(y_symbol)

        return {
            "status": "success",
            "data": {
                "symbol": symbol,
                "income_statement": ticker.financials.fillna(0).to_dict(),
                "balance_sheet": ticker.balance_sheet.fillna(0).to_dict(),
                "cashflow": ticker.cashflow.fillna(0).to_dict()
            }
        }

    except Exception as e:
        return {"status": "fail", "data": str(e)}


def get_stock_news(symbol: str):
    """
    Get latest news articles related to a stock or asset.

    Returns headline, source, link, and publish time.
    Useful for tracking market sentiment and events.
    """
    try:
        y_symbol = _resolve_symbol(symbol)
        ticker = yf.Ticker(y_symbol)

        news = ticker.news

        return {
            "status": "success",
            "data": {
                "symbol": symbol,
                "news": news
            }
        }

    except Exception as e:
        return {"status": "fail", "data": str(e)}


def get_holders_data(symbol: str):
    """
    Get ownership details of a company.

    Includes:
    - Major holders
    - Institutional holders
    - Mutual fund holders

    Useful to understand:
    - Who owns the stock
    - Smart money activity
    """
    try:
        y_symbol = _resolve_symbol(symbol)
        ticker = yf.Ticker(y_symbol)

        return {
            "status": "success",
            "data": {
                "major_holders": ticker.major_holders.to_dict() if ticker.major_holders is not None else {},
                "institutional_holders": ticker.institutional_holders.to_dict() if ticker.institutional_holders is not None else {},
                "mutualfund_holders": ticker.mutualfund_holders.to_dict() if ticker.mutualfund_holders is not None else {}
            }
        }

    except Exception as e:
        return {"status": "fail", "data": str(e)}


def get_insider_activity(symbol: str):
    """
    Get insider trading activity.

    Includes:
    - Insider purchases
    - Insider transactions
    - Insider holdings

    Useful for detecting:
    - Smart money buying/selling
    """
    try:
        y_symbol = _resolve_symbol(symbol)
        ticker = yf.Ticker(y_symbol)

        return {
            "status": "success",
            "data": {
                "insider_purchases": ticker.insider_purchases.to_dict() if ticker.insider_purchases is not None else {},
                "insider_transactions": ticker.insider_transactions.to_dict() if ticker.insider_transactions is not None else {},
                "insider_roster": ticker.insider_roster_holders.to_dict() if ticker.insider_roster_holders is not None else {}
            }
        }

    except Exception as e:
        return {"status": "fail", "data": str(e)}


def get_corporate_actions(symbol: str):
    """
    Get corporate actions.

    Includes:
    - Dividends
    - Stock splits
    - Capital gains

    Useful for:
    - Long-term investors
    - Adjusted returns analysis
    """
    try:
        y_symbol = _resolve_symbol(symbol)
        ticker = yf.Ticker(y_symbol)

        return {
            "status": "success",
            "data": {
                "dividends": ticker.dividends.to_dict() if ticker.dividends is not None else {},
                "splits": ticker.splits.to_dict() if ticker.splits is not None else {},
                "capital_gains": ticker.capital_gains.to_dict() if ticker.capital_gains is not None else {}
            }
        }

    except Exception as e:
        return {"status": "fail", "data": str(e)}


def get_earnings_calendar(symbol: str):
    """
    Get upcoming and past company events.

    Includes:
    - Earnings dates
    - Dividend dates
    - Corporate events

    Useful for:
    - Event-based trading
    - Volatility prediction
    """
    try:
        y_symbol = _resolve_symbol(symbol)
        ticker = yf.Ticker(y_symbol)

        return {
            "status": "success",
            "data": ticker.calendar.to_dict() if ticker.calendar is not None else {}
        }

    except Exception as e:
        return {"status": "fail", "data": str(e)}


def get_analyst_insights(symbol: str):
    """
    Get analyst recommendations and price targets.

    Includes:
    - Buy/Sell ratings
    - Price targets
    - Upgrades/Downgrades

    Useful for:
    - Market sentiment
    - Institutional expectations
    """
    try:
        y_symbol = _resolve_symbol(symbol)
        ticker = yf.Ticker(y_symbol)

        return {
            "status": "success",
            "data": {
                "recommendations": ticker.recommendations.to_dict() if ticker.recommendations is not None else {},
                "summary": ticker.recommendations_summary,
                "upgrades_downgrades": ticker.upgrades_downgrades.to_dict() if ticker.upgrades_downgrades is not None else {},
                "price_targets": ticker.analyst_price_targets
            }
        }

    except Exception as e:
        return {"status": "fail", "data": str(e)}


def get_earnings_forecast(symbol: str):
    """
    Get earnings expectations and trends.

    Includes:
    - Earnings estimates
    - Revenue estimates
    - EPS trends
    - Revisions

    Useful for:
    - Predicting future performance
    """
    try:
        y_symbol = _resolve_symbol(symbol)
        ticker = yf.Ticker(y_symbol)

        return {
            "status": "success",
            "data": {
                "earnings_estimate": ticker.earnings_estimate.to_dict() if ticker.earnings_estimate is not None else {},
                "revenue_estimate": ticker.revenue_estimate.to_dict() if ticker.revenue_estimate is not None else {},
                "eps_trend": ticker.eps_trend.to_dict() if ticker.eps_trend is not None else {},
                "eps_revisions": ticker.eps_revisions.to_dict() if ticker.eps_revisions is not None else {},
                "growth_estimates": ticker.growth_estimates.to_dict() if ticker.growth_estimates is not None else {}
            }
        }

    except Exception as e:
        return {"status": "fail", "data": str(e)}


def get_esg_data(symbol: str):
    """
    Get ESG (Environmental, Social, Governance) scores.

    Useful for:
    - Responsible investing
    - Risk assessment
    """
    try:
        y_symbol = _resolve_symbol(symbol)
        ticker = yf.Ticker(y_symbol)

        return {
            "status": "success",
            "data": ticker.sustainability.to_dict() if ticker.sustainability is not None else {}
        }

    except Exception as e:
        return {"status": "fail", "data": str(e)}


def get_full_stock_data(symbol: str):
    """
    Get comprehensive stock data in one call.

    Combines:
    - Price
    - Fundamentals
    - News
    - Analyst data
    - Corporate actions

    This is a master tool for AI agents.
    """
    try:
        y_symbol = _resolve_symbol(symbol)
        ticker = yf.Ticker(y_symbol)

        return {
            "status": "success",
            "data": {
                "info": ticker.info,
                "fast_info": ticker.fast_info,
                "calendar": ticker.calendar,
                "recommendations": ticker.recommendations,
                "news": ticker.news,
                "dividends": ticker.dividends.to_dict() if ticker.dividends is not None else {},
                "splits": ticker.splits.to_dict() if ticker.splits is not None else {}
            }
        }

    except Exception as e:
        return {"status": "fail", "data": str(e)}


def get_balance_sheet_data(symbol: str):
    """
    Get balance sheet data for a stock.

    This includes:
    - Assets (current & non-current)
    - Liabilities (current & long-term)
    - Shareholder equity
    - Debt levels

    Also provides:
    - Quarterly and yearly balance sheet
    - Basic derived metrics like:
        - Debt to Equity ratio
        - Current ratio

    Returns structured financial data for analysis.
    """
    try:
        ticker = yf.Ticker(symbol)

        # Balance sheets
        annual_bs = ticker.balance_sheet.fillna(0)
        quarterly_bs = ticker.quarterly_balance_sheet.fillna(0)

        if annual_bs.empty and quarterly_bs.empty:
            return {
                "status": "fail",
                "data": "No balance sheet data found"
            }

        # Helper function to calculate ratios
        def calculate_ratios(bs: pd.DataFrame):
            ratios = {}
            try:
                total_assets = bs.loc["Total Assets"].iloc[0]
                total_liabilities = bs.loc["Total Liabilities Net Minority Interest"].iloc[0]
                current_assets = bs.loc["Current Assets"].iloc[0]
                current_liabilities = bs.loc["Current Liabilities"].iloc[0]

                debt = total_liabilities
                equity = total_assets - total_liabilities

                ratios = {
                    "debt_to_equity": debt / equity if equity else None,
                    "current_ratio": current_assets / current_liabilities if current_liabilities else None
                }
            except Exception:
                pass

            return ratios

        result = {
            "status": "success",
            "data": {
                "symbol": symbol,
                "annual_balance_sheet": annual_bs.to_dict(),
                "quarterly_balance_sheet": quarterly_bs.to_dict(),
                "ratios": {
                    "annual": calculate_ratios(annual_bs),
                    "quarterly": calculate_ratios(quarterly_bs)
                }
            }
        }

        return result

    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }
