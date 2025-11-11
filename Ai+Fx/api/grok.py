import json
import yfinance as yf
import pandas as pd
import numpy as np

class ForexDataCollector:
    def __init__(self):
        self.major_pairs = [
            ('EUR', 'USD', 'Euro/US Dollar'),
            ('GBP', 'USD', 'British Pound/US Dollar'), 
            ('USD', 'JPY', 'US Dollar/Japanese Yen'),
            ('USD', 'CHF', 'US Dollar/Swiss Franc'),
            ('AUD', 'USD', 'Australian Dollar/US Dollar'),
            ('USD', 'CAD', 'US Dollar/Canadian Dollar'),
            ('NZD', 'USD', 'New Zealand Dollar/US Dollar'),
            ('XAU', 'USD', 'Gold/US Dollar')
        ]
    
    def get_realtime_quote(self, from_currency, to_currency):
        if from_currency == 'XAU' and to_currency == 'USD':
            ticker = 'GC=F'
        else:
            ticker = f'{from_currency}{to_currency}=X'
        data = yf.Ticker(ticker).history(period='1d', interval='1m')
        if data.empty:
            return None
        current_price = data['Close'].iloc[-1]
        bid_price = current_price - 0.00005
        ask_price = current_price + 0.00005
        return {
            'symbol': ticker.upper(),
            'description': f"{from_currency}/{to_currency}",
            'current_price': current_price,
            'bid': bid_price,
            'ask': ask_price
        }
    
    def get_historical_data(self, from_symbol, to_symbol, outputsize='full'):
        if from_symbol == 'XAU' and to_symbol == 'USD':
            ticker = 'GC=F'
        else:
            ticker = f'{from_symbol}{to_symbol}=X'
        if outputsize == 'full':
            data = yf.Ticker(ticker).history(period='max')
        else:
            data = yf.Ticker(ticker).history(period='1y')
        if data.empty:
            return None
        data = data.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })
        return data
    
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
        atr = pd.Series(np.nan, index=df.index)
        plus_dm_sm = pd.Series(np.nan, index=df.index)
        minus_dm_sm = pd.Series(np.nan, index=df.index)
        plus_di = pd.Series(np.nan, index=df.index)
        minus_di = pd.Series(np.nan, index=df.index)
        dx = pd.Series(np.nan, index=df.index)
        adx = pd.Series(np.nan, index=df.index)
        if len(df) < period:
            return adx, plus_di, minus_di
        start = period
        atr[start-1] = tr[1:start+1].mean()
        plus_dm_sm[start-1] = plus_dm[1:start+1].mean()
        minus_dm_sm[start-1] = minus_dm[1:start+1].mean()
        plus_di[start-1] = (plus_dm_sm[start-1] / atr[start-1]) * 100
        minus_di[start-1] = (minus_dm_sm[start-1] / atr[start-1]) * 100
        dx[start-1] = abs(plus_di[start-1] - minus_di[start-1]) / (plus_di[start-1] + minus_di[start-1]) * 100 if (plus_di[start-1] + minus_di[start-1]) != 0 else 0
        for i in range(start, len(df)):
            atr[i] = (atr[i-1] * (period - 1) + tr[i]) / period
            plus_dm_sm[i] = (plus_dm_sm[i-1] * (period - 1) + plus_dm[i]) / period
            minus_dm_sm[i] = (minus_dm_sm[i-1] * (period - 1) + minus_dm[i]) / period
            plus_di[i] = (plus_dm_sm[i] / atr[i]) * 100
            minus_di[i] = (minus_dm_sm[i] / atr[i]) * 100
            dx[i] = abs(plus_di[i] - minus_di[i]) / (plus_di[i] + minus_di[i]) * 100 if (plus_di[i] + minus_di[i]) != 0 else 0
        adx_start = start + period - 1
        if len(df) > adx_start:
            adx[adx_start] = dx[start-1:adx_start+1].mean()
            for i in range(adx_start + 1, len(df)):
                adx[i] = (adx[i-1] * (period - 1) + dx[i]) / period
        return adx, plus_di, minus_di
    
    def calculate_technical_indicators(self, data):
        if data is None or len(data) < 50:
            return None
        df = data.copy().sort_index(ascending=True)
        closes = df['close']
        highs = df['high']
        lows = df['low']
        opens = df['open']
        volume = df['volume'] if 'volume' in df.columns else pd.Series(0, index=df.index)
        
        # SMA
        df['SMA_5'] = closes.rolling(5).mean()
        df['SMA_10'] = closes.rolling(10).mean()
        df['SMA_20'] = closes.rolling(20).mean()
        df['SMA_50'] = closes.rolling(50).mean()
        
        # EMA
        df['EMA_12'] = closes.ewm(span=12, adjust=False).mean()
        df['EMA_26'] = closes.ewm(span=26, adjust=False).mean()
        
        # VWAP
        typical_price = (highs + lows + closes) / 3
        vwap_volume = typical_price * volume
        df['VWAP'] = vwap_volume.cumsum() / volume.cumsum()
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        # STOCH
        period = 14
        lowest_low = lows.rolling(period).min()
        highest_high = highs.rolling(period).max()
        df['STOCH_K'] = ((closes - lowest_low) / (highest_high - lowest_low)) * 100
        df['STOCH_D'] = df['STOCH_K'].rolling(3).mean()
        
        # RSI
        delta = closes.diff()
        gain = (delta.where(delta > 0, 0)).ewm(span=14, adjust=False).mean()
        loss = (-delta.where(delta < 0, 0)).ewm(span=14, adjust=False).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # ADX
        df['ADX'], df['+DI'], df['-DI'] = self.calculate_dmi(highs, lows, closes)
        
        # CCI
        tp = (highs + lows + closes) / 3
        ma_tp = tp.rolling(20).mean()
        md = tp.rolling(20).std()
        df['CCI'] = (tp - ma_tp) / (0.015 * md)
        
        # AROON
        period = 25
        high_period = highs.rolling(period+1).apply(lambda x: x.argmax(), raw=True)
        low_period = lows.rolling(period+1).apply(lambda x: x.argmin(), raw=True)
        df['AROON_UP'] = ((period - high_period) / period) * 100
        df['AROON_DOWN'] = ((period - low_period) / period) * 100
        
        # BBANDS
        df['BB_Middle'] = closes.rolling(20).mean()
        bb_std = closes.rolling(20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        # AD (Chaikin A/D Line)
        money_flow_multiplier = ((closes - lows) - (highs - closes)) / (highs - lows)
        money_flow_volume = money_flow_multiplier * volume
        df['AD'] = money_flow_volume.cumsum()
        
        # OBV
        obv = pd.Series(0, index=df.index)
        obv.iloc[1:] = np.sign(closes.diff().iloc[1:]) * volume.iloc[1:]
        df['OBV'] = obv.cumsum()
        
        latest = df.iloc[-1]
        technicals = {
            'SMA_5': latest['SMA_5'],
            'SMA_10': latest['SMA_10'],
            'SMA_20': latest['SMA_20'],
            'SMA_50': latest['SMA_50'],
            'EMA_12': latest['EMA_12'],
            'EMA_26': latest['EMA_26'],
            'VWAP': latest['VWAP'],
            'MACD': latest['MACD'],
            'MACD_Signal': latest['MACD_Signal'],
            'MACD_Histogram': latest['MACD_Histogram'],
            'STOCH_K': latest['STOCH_K'],
            'STOCH_D': latest['STOCH_D'],
            'RSI': latest['RSI'],
            'ADX': latest['ADX'],
            '+DI': latest['+DI'],
            '-DI': latest['-DI'],
            'CCI': latest['CCI'],
            'AROON_UP': latest['AROON_UP'],
            'AROON_DOWN': latest['AROON_DOWN'],
            'BB_Upper': latest['BB_Upper'],
            'BB_Middle': latest['BB_Middle'],
            'BB_Lower': latest['BB_Lower'],
            'AD': latest['AD'],
            'OBV': latest['OBV']
        }
        return technicals
    
    def collect_data(self):
        pairs_data = []
        for from_curr, to_curr, description in self.major_pairs:
            quote = self.get_realtime_quote(from_curr, to_curr)
            if quote:
                historical_data = self.get_historical_data(from_curr, to_curr)
                if historical_data is not None:
                    technicals = self.calculate_technical_indicators(historical_data)
                    if technicals:
                        quote['technicals'] = technicals
                pairs_data.append(quote)
        return {"pairs": pairs_data}
    
    def save_to_json(self, data, filename='forex_data.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4, default=str)
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    collector = ForexDataCollector()
    data = collector.collect_data()
    collector.save_to_json(data)