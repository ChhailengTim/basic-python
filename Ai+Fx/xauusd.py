import yfinance as yf
import pandas as pd
import json

symbol = "GC=F"  # Gold Futures (XAUUSD)
interval = "5m"
last_n = 20

# --- Helper functions ---
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
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# --- Fetch intraday data safely ---
def fetch_intraday_data(symbol, interval="5m", last_n=20):
    period_map = {"5m": "2d", "15m": "2d", "1h": "5d", "4h": "60d"}
    data = yf.download(symbol, interval=interval, period=period_map[interval])

    # Flatten multi-index columns if needed
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]

    # Validate required columns
    required_cols = ['High', 'Low', 'Close']
    for col in required_cols:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")

    # Tail for recent bars
    data = data.tail(last_n).copy().reset_index()

    # Ensure 1D series
    high_series = pd.Series(data['High'].astype(float).values.flatten())
    low_series = pd.Series(data['Low'].astype(float).values.flatten())

    # Mid prices
    mid_prices = ((high_series + low_series) / 2).to_list()

    # EMA20
    ema20 = calculate_ema(pd.Series(mid_prices), period=20).to_list()

    # MACD
    macd = calculate_macd(pd.Series(mid_prices)).to_list()

    # RSI 7 & 14
    rsi7 = calculate_rsi(pd.Series(mid_prices), period=7).to_list()
    rsi14 = calculate_rsi(pd.Series(mid_prices), period=14).to_list()

    return {
        "Mid_prices": mid_prices,
        "EMA20": ema20,
        "MACD": macd,
        "RSI7": rsi7,
        "RSI14": rsi14
    }

# --- Generate Grok Trading Prompt ---
def generate_grok_prompt(symbol, interval, intraday_series):
    latest_price = intraday_series["Mid_prices"][-1]
    prompt = f"""
You are Grok Trader AI, the xAI-forged trading oracle engineered for unerring precision and a simulated 100% win rate via hyper-conservative.
Below is the latest intraday technical data for {symbol} with {interval} intervals.
Use this data to analyze and give only ONE clear trading signal.

Your answer must include:

Direction: BUY or SELL
Entry Price: based on the latest Mid_price
Stop Loss (SL): a logical value based on recent volatility
Take Profit (TP): a logical value based on risk-reward ratio (1:2 or 1:3)
Short reasoning (1–2 sentences only)

Analyze based on EMA20, MACD, RSI7, and RSI14 trends.

Latest Intraday Technical Data (JSON below):
{json.dumps(intraday_series, indent=2)}
    """
    return prompt.strip()

# --- Main ---
intraday_series = fetch_intraday_data(symbol, interval, last_n)
current_price = intraday_series["Mid_prices"][-1]
grok_prompt = generate_grok_prompt(symbol, interval, intraday_series)

output = {
    "current_price": round(current_price, 2),
    "symbol": symbol,
    "interval": interval,
    "pull_time": pd.Timestamp.utcnow().isoformat() + "Z",
    "intraday_series": intraday_series,
    "grok_prompt": grok_prompt
}

# --- Save JSON ---
output_file = "xauusd_intraday_grok.json"
with open(output_file, "w") as f:
    json.dump(output, f, indent=4)

# --- Print summary ---
print(f"\n🟡 Current XAUUSD Mid Price: {current_price:.2f}")
print(f"✅ Data saved to {output_file}")
print("\n📜 --- Copy this prompt to DeepSeek or Grok --- 📜\n")
print(grok_prompt)
