import yfinance as yf
import pandas as pd
import json

symbol = "GC=F"  # Gold Futures (XAUUSD)
interval = "5m"
last_n = 30  # Last 30 candles

# --- Helper Functions ---
def calculate_ema(series, period=20):
    return series.ewm(span=period, adjust=False).mean()

def calculate_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line - signal_line

def calculate_rsi(series, period=7):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_atr(data, period=14):
    high_low = data['High'] - data['Low']
    high_close = abs(data['High'] - data['Close'].shift())
    low_close = abs(data['Low'] - data['Close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def calculate_vwap(data):
    return ((data['High'] + data['Low'] + data['Close']) / 3 * data['Volume']).cumsum() / data['Volume'].cumsum()

def calculate_trade_levels(mid_price, atr):
    if pd.isna(atr):
        atr = 5  # fallback ATR if not enough data
    sl = round(mid_price - 5, 2)  # $5 loss
    tp = round(mid_price + 10, 2) # $10 profit
    return sl, tp

# --- Fetch intraday data ---
def fetch_intraday_data(symbol, interval="5m", last_n=30):
    period_map = {
    "1m": "1d",
    "5m": "2d",
    "15m": "3d",
}

    data = yf.download(symbol, interval=interval, period=period_map[interval], progress=False)

    # Flatten multi-index if exists
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]

    required_cols = ['High', 'Low', 'Close', 'Open', 'Volume']
    for col in required_cols:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")

    data = data.tail(last_n).copy().reset_index()

    # Calculate indicators
    data['Mid'] = (data['High'] + data['Low']) / 2
    data['EMA20'] = calculate_ema(data['Mid'], 20)
    data['EMA50'] = calculate_ema(data['Mid'], 50)
    data['MACD_Line'] = calculate_macd(data['Mid'])
    data['RSI7'] = calculate_rsi(data['Mid'], 7)
    data['ATR14'] = calculate_atr(data, 14)
    data['VWAP'] = calculate_vwap(data)

    return data

# --- Generate Grok prompt ---
def generate_grok_prompt(data, symbol, interval):
    latest = data.iloc[-1].copy()

    # Convert timestamps to strings for JSON safety
    for col in latest.index:
        if isinstance(latest[col], pd.Timestamp):
            latest[col] = latest[col].isoformat()

    sl, tp = calculate_trade_levels(latest['Mid'], latest['ATR14'])

    prompt = f"""
You are Grok Trader Professional, the AI engine for scalping precision. Below is the latest intraday data for GOLD (XAUUSD) with 5m intervals. Use this data to generate a clear and high win-rate trading signal for scalping. Each trade aims to WIN $10 and RISK $5 based on real-time gold market momentum.\n\nIndicator Usage Guide:\n- EMA20: Detect short-term price direction and quick scalp momentum.\n- EMA50: Confirm medium-term gold trend strength.\n- MACD: Confirm momentum shifts and potential reversal points.\n- RSI7: Identify gold’s overbought or oversold conditions for entry timing.\n- ATR14: Measure volatility to dynamically size stop loss and take profit.\n- VWAP: Show institutional control — price above = bullish, below = bearish.\n- Mid Price: Represent market balance for fine scalp entries.\n\nTrading Logic for Grok:\n- Use EMA20 crossing EMA50 to detect trend bias (bullish or bearish momentum).\n- Confirm with MACD crossover and RSI7 levels for precision timing.\n- Apply ATR14 to set stop loss ($5 risk) and take profit ($10 target) zones.\n- Align trades with VWAP direction to follow institutional flow.\n- Use Mid Price to refine scalp entry when volatility is low.\n\nGenerate the final professional scalping signal: BUY, SELL, or HOLD — with clear entry price, stop loss, and take profit that fits the $10 win / $5 loss structure."

"""
    return prompt.strip()

# --- Main ---
data = fetch_intraday_data(symbol, interval, last_n)
current_price = data['Mid'].iloc[-1]
grok_prompt = generate_grok_prompt(data, symbol, interval)

# Convert timestamps to string for full data JSON
data_copy = data.copy()
for col in data_copy.select_dtypes(include=['datetime', 'datetimetz']).columns:
    data_copy[col] = data_copy[col].astype(str)

output = {
    "current_price": round(current_price, 2),
    "symbol": symbol,
    "interval": interval,
    "pull_time": pd.Timestamp.utcnow().isoformat() + "Z",
    "intraday_data": data_copy.to_dict(orient='records'),
    "grok_prompt": grok_prompt
}

# --- Save JSON ---
output_file = "xauusd_intraday_grok_v3.json"
with open(output_file, "w") as f:
    json.dump(output, f, indent=4)

# --- Print summary ---
print(f"\n🟡 Current {symbol} {interval} Mid Price: {current_price:.2f}")
print(f"✅ Data saved to {output_file}")
print("\n📜 --- Copy this prompt to Grok --- 📜\n")
# print(grok_prompt)
