from datetime import datetime, timedelta, time, UTC
import requests
import threading

STEP_CANDLES = 43
MARKET_START = time(9, 15)
MARKET_END = time(15, 30)
CANDLE_INTERVAL = timedelta(minutes=15)
CANDLES_PER_DAY = 25



# ---------------- CACHE ----------------
_holiday_cache = {
    "data": None,
    "last_updated": None
}

_cache_lock = threading.Lock()
CACHE_TTL_HOURS = 24


# ---------------- FETCH ----------------
def _fetch_nse_holidays():
    url = "https://www.nseindia.com/api/holiday-master?type=trading"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com/",
    }

    session = requests.Session()

    # warmup (important for NSE)
    session.get("https://www.nseindia.com", headers=headers, timeout=5)

    response = session.get(url, headers=headers, timeout=5)
    response.raise_for_status()

    res = response.json()

    holidays = set()

    for item in res.get("COM", []):
        date_str = item["tradingDate"]
        parsed = datetime.strptime(date_str, "%d-%b-%Y").strftime("%Y-%m-%d")
        holidays.add(parsed)

    return holidays


# ---------------- PUBLIC ----------------
def get_nse_holidays():
    """
    Cached NSE holiday fetcher with TTL + fallback.
    """

    with _cache_lock:
        now = datetime.now(UTC)

        if (
            _holiday_cache["data"] is not None
            and _holiday_cache["last_updated"] is not None
            and now - _holiday_cache["last_updated"] < timedelta(hours=CACHE_TTL_HOURS)
        ):
            return _holiday_cache["data"]

        try:
            holidays = _fetch_nse_holidays()

            _holiday_cache["data"] = holidays
            _holiday_cache["last_updated"] = now

            return holidays

        except Exception as e:
            # Fallback to old cache if exists
            if _holiday_cache["data"] is not None:
                return _holiday_cache["data"]

            # Absolute fallback (fail-safe)
            print("⚠️ NSE holiday fetch failed:", e)
            return set()


def is_trading_day(dt, holidays):
    return dt.weekday() < 5 and dt.strftime("%Y-%m-%d") not in holidays


def next_trading_day(dt, holidays):
    dt += timedelta(days=1)
    while not is_trading_day(dt, holidays):
        dt += timedelta(days=1)
    return dt


def add_trading_days(dt, days, holidays):
    count = 0
    while count < days:
        dt += timedelta(days=1)
        if is_trading_day(dt, holidays):
            count += 1
    return dt


def align_start(dt, holidays):
    if not is_trading_day(dt, holidays):
        dt = next_trading_day(dt, holidays)
        return datetime.combine(dt.date(), MARKET_START)

    if dt.time() < MARKET_START:
        return datetime.combine(dt.date(), MARKET_START)

    if dt.time() >= MARKET_END:
        dt = next_trading_day(dt, holidays)
        return datetime.combine(dt.date(), MARKET_START)

    return dt


def candle_index_in_day(dt):
    minutes = (dt.hour * 60 + dt.minute) - (9 * 60 + 15)
    return minutes // 15


def candles_remaining_today(dt):
    idx = candle_index_in_day(dt)
    return CANDLES_PER_DAY - idx - 1


def jump_n_candles(dt, n, holidays):
    dt = align_start(dt, holidays)

    remaining_today = candles_remaining_today(dt)

    if n <= remaining_today:
        return dt + n * CANDLE_INTERVAL

    n -= (remaining_today + 1)
    full_days = n // CANDLES_PER_DAY
    dt = add_trading_days(dt, full_days + 1, holidays)

    remainder = n % CANDLES_PER_DAY

    return datetime.combine(dt.date(), MARKET_START) + remainder * CANDLE_INTERVAL


def format_candle_time(dt):
    end = dt + timedelta(minutes=15)

    start_str = dt.strftime("%I:%M")
    end_str = end.strftime("%I:%M")

    suffix = end.strftime("%p")

    return f"{start_str} - {end_str} {suffix}"


def generate_43_step_candles(start_dt, count):
    result = []

    holidays = get_nse_holidays()
    current = start_dt

    for _ in range(count):
        current = jump_n_candles(current, STEP_CANDLES, holidays)
        result.append(
            {
                "date": current.strftime("%d %B %Y"),
                "day": current.strftime("%A"),
                "candle_time": format_candle_time(current),
            }
        )

    return result


def get_samay_zone(start_dt_str:str, count:int=5):
    """
    Generate a sequence of future NSE candle timestamps using a fixed step (43 candles).

    This function calculates future candle times based on a given start datetime,
    skipping non-trading hours (before 09:15, after 15:30), weekends, and NSE holidays.
    Each step jumps forward by 43 candles (15-minute intervals).

    Args:
        start_dt_str (str): Start datetime in format "YYYY-MM-DD HH:MM"
            Example: "2026-04-23 11:30"

        count (int, optional): Number of future candle timestamps to generate.
            Default is 5.

    Returns:
        dict: Response object with status and generated candle data.
            {
                "status": "success",
                "data": [
                    {
                        "date": "23 April 2026, Thursday",
                        "day": 23,
                        "candle_time": "11:30 - 11:45 AM"
                    },
                    ...
                ]
            }

    Raises:
        ValueError: If input datetime format is invalid.

    Notes:
        - Uses 15-minute candle intervals.
        - Market hours: 09:15 to 15:30 (last candle starts at 15:15).
        - Automatically skips weekends and NSE holidays.
        - Uses exclusive candle stepping (next candle progression).
    """
    try:
        if count <= 0:
            raise ValueError("count must be greater than 0")

        start = datetime.strptime(start_dt_str, "%Y-%m-%d %H:%M")
        candles = generate_43_step_candles(start, count)

        return {
            "status": "success",
            "data": candles
        }

    except Exception as e:
        return {
            "status": "fail",
            "data": str(e)
        }

