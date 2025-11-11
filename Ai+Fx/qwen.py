import yfinance as yf
import pandas as pd
import numpy as np
import json
from datetime import datetime

# -----------------------------
# 🔑 SET YOUR CURRENT PRICE HERE (from your system/terminal/feed)
# -----------------------------
CURRENT_PRICE = 4114  # ←←← EDIT THIS VALUE MANUALLY OR PASS VIA ARGUMENT

# -----------------------------
# CUSTOM JSON ENCODER FOR NUMPY
# -----------------------------
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

# -----------------------------
# CONFIGURATION
# -----------------------------
SYMBOL = "GC=F"
INTRADAY_INTERVAL = "5m"
LAST_N_INTRADAY = 10
LAST_N_LONG_TERM = 10

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def calculate_ema(series, period=20):
    return series.ewm(span=period, adjust=False).mean()

def calculate_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line - signal_line

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def fetch_intraday_data(symbol, interval="5m", last_n=10):
    period_map = {"1m": "1d", "2m": "1d", "5m": "2d", "15m": "2d", "30m": "5d", "1h": "5d", "4h": "60d"}
    period = period_map.get(interval, "2d")
    data = yf.download(symbol, interval=interval, period=period)
    if data.empty:
        raise ValueError(f"No data for {symbol}")
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
    required = ['High', 'Low', 'Close']
    for col in required:
        if col not in data.columns:
            raise ValueError(f"Missing {col}")
    data = data.tail(last_n).copy()
    high = data['High'].astype(float)
    low = data['Low'].astype(float)
    mid = (high + low) / 2
    ema20 = calculate_ema(mid, 20)
    macd_hist = calculate_macd(mid)
    rsi7 = calculate_rsi(mid, 7)
    rsi14 = calculate_rsi(mid, 14)
    def clean_series(s):
        return s.dropna().round(3).tolist()
    return {
        "mid_prices": clean_series(mid),
        "ema20": clean_series(ema20),
        "macd": clean_series(macd_hist),
        "rsi7": clean_series(rsi7),
        "rsi14": clean_series(rsi14)
    }

def fetch_long_term_context(symbol, last_n=10):
    raw = yf.download(symbol, interval="1h", period="60d")
    if raw.empty:
        raise ValueError("No long-term data")
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.droplevel(1)
    ohlc_dict = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}
    df_4h = raw.resample('4H').agg(ohlc_dict).dropna()
    mid = (df_4h['High'] + df_4h['Low']) / 2
    mid = mid.tail(last_n)
    ema20 = calculate_ema(mid, 20)
    ema50 = calculate_ema(mid, 50)
    macd_hist = calculate_macd(mid)
    rsi14 = calculate_rsi(mid, 14)
    tr = np.maximum(
        df_4h['High'] - df_4h['Low'],
        np.abs(df_4h['High'] - df_4h['Close'].shift(1)),
        np.abs(df_4h['Low'] - df_4h['Close'].shift(1))
    )
    atr3 = tr.rolling(3).mean()
    atr14 = tr.rolling(14).mean()
    volume = df_4h['Volume'].tail(last_n)
    avg_volume = volume.mean() if not volume.empty else 0.0
    return {
        "ema20_latest": ema20.iloc[-1] if not ema20.empty else None,
        "ema50_latest": ema50.iloc[-1] if not ema50.empty else None,
        "atr3_latest": atr3.iloc[-1] if not atr3.empty else None,
        "atr14_latest": atr14.iloc[-1] if not atr14.empty else None,
        "current_volume": volume.iloc[-1] if not volume.empty else None,
        "avg_volume": avg_volume,
        "macd_series": macd_hist.dropna().round(3).tail(last_n).tolist(),
        "rsi14_series": rsi14.dropna().round(3).tail(last_n).tolist()
    }

def get_derivatives_data():
    return {
        "open_interest_latest": None,
        "open_interest_avg": None,
        "funding_rate": None
    }

def generate_trading_prompt(symbol, current_price):
    prompt = f"""You are Qwen3-Max AI, Alibaba’s elite trading oracle, engineered for unerring precision and a simulated 100% win rate through hyper-conservative, volatility-aware, and risk-managed decision-making.

Below is the latest intraday technical dataset for {symbol} (Gold Futures) at 5-minute intervals. Perform a concise, disciplined technical analysis using only the provided data. Ignore external knowledge or assumptions.

Output exactly one trading signal in the following strict format—no explanations, disclaimers, or additional text:

Direction: BUY or SELL
Entry Price: {current_price}
Stop Loss (SL): A logical level based on recent intraday volatility (e.g., using ATR or recent swing low/high)
Take Profit (TP): Set to achieve a minimum 1:2 risk-reward ratio (1:3 if strongly justified by structure)
Rules:

Prioritize confluence of oversold/overbought RSI, EMA slope, and MACD momentum.
If trend context (e.g., EMA20 > EMA50) supports a reversal signal, favor it.
Never extrapolate—use only the numbers provided.
Default to no trade only if all indicators are neutral—but if a signal exists, choose the highest-probability, lowest-risk setup.
Now analyze the data and output only the four required fields in clean, machine-readable format."""
    return prompt

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    # Fetch technical context (but NOT price)
    intraday = fetch_intraday_data(SYMBOL, INTRADAY_INTERVAL, LAST_N_INTRADAY)
    min_len = min(len(v) for v in intraday.values())
    for k in intraday:
        intraday[k] = intraday[k][-min_len:]

    long_term = fetch_long_term_context(SYMBOL, LAST_N_LONG_TERM)
    deriv = get_derivatives_data()

    # Use YOUR provided current price
    current_price = CURRENT_PRICE

    # Generate prompt using YOUR price
    trading_prompt = generate_trading_prompt(SYMBOL, current_price)

    output = {
        "trading_prompt": trading_prompt,
        "current_price": current_price,  # ← YOUR VALUE
        "current_ema20": intraday["ema20"][-1],
        "current_macd": intraday["macd"][-1],
        "current_rsi_7": intraday["rsi7"][-1],
        "current_rsi_14": intraday["rsi14"][-1],
        "open_interest": {
            "latest": deriv["open_interest_latest"],
            "average": deriv["open_interest_avg"]
        },
        "funding_rate": deriv["funding_rate"],
        "intraday_series": {
            "mid_prices": intraday["mid_prices"],
            "ema20": intraday["ema20"],
            "macd": intraday["macd"],
            "rsi7": intraday["rsi7"],
            "rsi14": intraday["rsi14"]
        },
        "longer_term_context": {
            "ema20_vs_ema50": {
                "ema20": long_term["ema20_latest"],
                "ema50": long_term["ema50_latest"]
            },
            "atr": {
                "3_period": long_term["atr3_latest"],
                "14_period": long_term["atr14_latest"]
            },
            "volume": {
                "current": long_term["current_volume"],
                "average": long_term["avg_volume"]
            },
            "macd_series": long_term["macd_series"],
            "rsi14_series": long_term["rsi14_series"]
        },
        "metadata": {
            "symbol": SYMBOL,
            "asset": "Gold (XAU/USD Futures)",
            "intraday_interval": INTRADAY_INTERVAL,
            "long_term_interval": "4h",
            "pull_time_utc": datetime.utcnow().isoformat() + "Z",
            "price_source": "user_provided"
        }
    }

    with open("xauusd_alpha_context.json", "w") as f:
        json.dump(output, f, indent=4, cls=NpEncoder)

    print("\n" + "="*60)
    print("✅ GOLD CONTEXT GENERATED WITH YOUR CURRENT PRICE")
    print("="*60)
    print(f"Your Current Price: {current_price}")
    print(f"EMA20: {output['current_ema20']:.3f}")
    print(f"RSI (7): {output['current_rsi_7']:.3f}")
    print("🟢 Data + prompt saved to xauusd_alpha_context.json")