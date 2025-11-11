import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import warnings
import logging

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ForexTradingSystem:
    def __init__(self, account_balance=10000, risk_per_trade=0.01):
        self.account_balance = account_balance
        self.risk_per_trade = risk_per_trade
        
        self.major_pairs = {
            'EURUSD': 'EURUSD=X',
            'GBPUSD': 'GBPUSD=X',
            'USDJPY': 'USDJPY=X',
            'USDCHF': 'USDCHF=X',
            'AUDUSD': 'AUDUSD=X',
            'USDCAD': 'USDCAD=X',
            'NZDUSD': 'NZDUSD=X',
            'XAUUSD': 'GC=F'
        }

    def fetch_historical_data(self, symbol, period="2y"):
        try:
            data = yf.download(symbol, period=period, interval="1d", auto_adjust=False)
            if data.empty:
                logging.error(f"No data for {symbol} in period {period}")
                return None
            data = data.rename(columns={
                'Open': '1. open',
                'High': '2. high',
                'Low': '3. low',
                'Close': '4. close',
                'Volume': '5. volume'
            })
            return data.sort_index(ascending=True)
        except Exception as e:
            logging.error(f"Error fetching {symbol}: {e}")
            return None

    def get_current_price(self, symbol):
        try:
            hist = yf.download(symbol, period="1d", interval="1m")
            if not hist.empty:
                return hist['Close'].iloc[-1]
            else:
                data = self.fetch_historical_data(symbol, period="5d")
                return data['4. close'].iloc[-1] if data is not None else None
        except Exception as e:
            logging.error(f"Error fetching current price for {symbol}: {e}")
            return None

    def calculate_rsi(self, prices, period=14):
        if prices.isnull().any():
            logging.warning(f"RSI calculation: Null values detected in prices.")
            prices = prices.dropna()

        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def calculate_stochastic(self, highs, lows, closes, period=14):
        lowest_low = lows.rolling(period).min()
        highest_high = highs.rolling(period).max()
        return ((closes - lowest_low) / (highest_high - lowest_low)) * 100

    def calculate_atr(self, highs, lows, closes, period=14):
        tr1 = highs - lows
        tr2 = abs(highs - closes.shift())
        tr3 = abs(lows - closes.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(period).mean()

    def calculate_dmi(self, highs, lows, closes, period=14):
        df = pd.DataFrame({'high': highs, 'low': lows, 'close': closes})
        up = df['high'].diff()
        down = -df['low'].diff()
        plus_dm = np.where((up > down) & (up > 0), up, 0.0)
        minus_dm = np.where((down > up) & (down > 0), down, 0.0)

        tr_temp = pd.concat([
            df['high'] - df['low'],
            (df['high'] - df['close'].shift()).abs(),
            (df['low'] - df['close'].shift()).abs()
        ], axis=1)
        tr = tr_temp.max(axis=1)
        
        atr = tr.rolling(period).mean()
        plus_dm_sm = pd.Series(np.nan, index=df.index)
        minus_dm_sm = pd.Series(np.nan, index=df.index)
        plus_di = pd.Series(np.nan, index=df.index)
        minus_di = pd.Series(np.nan, index=df.index)
        dx = pd.Series(np.nan, index=df.index)
        adx = pd.Series(np.nan, index=df.index)
        
        for i in range(period, len(df)):
            plus_dm_sm[i] = plus_dm[i - period:i].mean()
            minus_dm_sm[i] = minus_dm[i - period:i].mean()
            atr[i] = atr[i - period:i].mean()
            plus_di[i] = (plus_dm_sm[i] / atr[i]) * 100 if atr[i] != 0 else 0
            minus_di[i] = (minus_dm_sm[i] / atr[i]) * 100 if atr[i] != 0 else 0
            dx[i] = abs(plus_di[i] - minus_di[i]) / (plus_di[i] + minus_di[i]) * 100 if (plus_di[i] + minus_di[i]) != 0 else 0

        adx = pd.Series(adx).rolling(period).mean()  # ADX smoothing
        
        return adx, plus_di, minus_di

    def generate_trading_signals(self, technical_data, current_price):
        if technical_data is None or len(technical_data) < 50:
            return None
        
        last_row = technical_data.iloc[-1].to_dict()
        
        def safe_get(key, default=0.0):
            val = last_row.get(key, default)
            try:
                return float(val)
            except (TypeError, ValueError, AttributeError):
                return default

        # Extracting the necessary values from technical data
        sma5 = safe_get('SMA_5')
        sma20 = safe_get('SMA_20')
        sma50 = safe_get('SMA_50')
        rsi = safe_get('RSI')
        macd = safe_get('MACD')
        macd_signal = safe_get('MACD_Signal')
        macd_hist = safe_get('MACD_Histogram')
        bb_lower = safe_get('BB_Lower')
        bb_upper = safe_get('BB_Upper')
        support = safe_get('Support')
        resistance = safe_get('Resistance')
        stoch_k = safe_get('STOCH_K')
        stoch_d = safe_get('STOCH_D')
        adx = safe_get('ADX')
        plus_di = safe_get('+DI')
        minus_di = safe_get('-DI')
        atr_val = safe_get('ATR')

        # Analyzing trading signals
        signals = []
        score = 0
        if sma5 > sma20 > sma50:
            signals.append("Uptrend: SMA5 > SMA20 > SMA50")
            score += 3
        elif sma5 < sma20 < sma50:
            signals.append("Downtrend: SMA5 < SMA20 < SMA50")
            score -= 3
        
        # RSI, MACD, ADX, etc. (you can continue the analysis as you did before)
        # After these checks, return the signals

        return {
            'action': "HOLD", 
            'score': score,
            'signals': signals,
            'support': support,
            'resistance': resistance,
            'atr': atr_val
        }

    def analyze_pair(self, pair_name, symbol):
        print(f"\n🔍 Analyzing {pair_name}...")
        hist = self.fetch_historical_data(symbol)
        if hist is None:
            print(f"  ❌ No historical data for {pair_name}")
            return None

        price = self.get_current_price(symbol)
        if price is None:
            price = hist['4. close'].iloc[-1]

        tech = self.calculate_technical_indicators(hist)
        if tech is None:
            print(f"  ❌ Insufficient data for indicators")
            return None

        sig = self.generate_trading_signals(tech, price)
        if sig is None or sig['action'] == "HOLD":
            print(f"  ➤ No trade signal (Action: {sig['action'] if sig else 'None'})")
            return None

        # Calculate trade levels, R:R, and other details as needed
        entry, sl, tp = self.calculate_trade_levels(price, sig, pair_name)
        if entry is None:
            return None

        # Risk-to-Reward ratio
        risk = abs(entry - sl)
        reward = abs(tp - entry)
        rr_ratio = reward / risk if risk > 0 else 0

        print(f"  💰 Current Price: {price:.5f}")
        print(f"  📊 Action: {sig['action']} (Score: {sig['score']})")
        print(f"  📌 Entry:       {entry:.5f}")
        print(f"  🛑 Stop Loss:   {sl:.5f}")
        print(f"  🎯 Take Profit: {tp:.5f}")
        print(f"  📈 R:R Ratio:   1 : {rr_ratio:.1f}")
        for s in sig['signals']:
            print(f"  → {s}")

        return {
            'pair': pair_name,
            'price': price,
            'action': sig['action'],
            'entry': entry,
            'sl': sl,
            'tp': tp,
            'score': sig['score'],
            'rr': rr_ratio
        }

    def monitor_all_pairs(self):
        print("🚀 FOREX SIGNAL GENERATOR - ENTRY / SL / TP")
        print("="*60)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Account: ${self.account_balance:,.2f} | Risk: {self.risk_per_trade*100}%")
        print("="*60)

        results = []
        for name, symbol in self.major_pairs.items():
            try:
                res = self.analyze_pair(name, symbol)
                if res:
                    results.append(res)
            except Exception as e:
                logging.error(f"Error in {name}: {e}")
        return results

def main():
    system = ForexTradingSystem(account_balance=10000, risk_per_trade=0.01)
    results = system.monitor_all_pairs()

    if results:
        print(f"\n{'='*60}")
        print("✅ TRADE PLAN SUMMARY")
        print(f"{'='*60}")
        for r in results:
            print(f"{r['pair']:8} | {r['action']:12} | "
                  f"Entry: {r['entry']:8.5f} | "
                  f"SL: {r['sl']:8.5f} | "
                  f"TP: {r['tp']:8.5f} | "
                  f"R:R={r['rr']:.1f}")
    else:
        print("\n⚠️  No trade signals found.")

    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
