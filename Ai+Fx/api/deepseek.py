import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
import logging

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ForexTradingSystem:
    def __init__(self):
        # Forex pairs in yfinance format
        self.forex_pairs = {
            'EURUSD=X': 'Euro/US Dollar',
            'GBPUSD=X': 'British Pound/US Dollar', 
            'USDJPY=X': 'US Dollar/Japanese Yen',
            'USDCHF=X': 'US Dollar/Swiss Franc',
            'AUDUSD=X': 'Australian Dollar/US Dollar',
            'USDCAD=X': 'US Dollar/Canadian Dollar',
            'NZDUSD=X': 'New Zealand Dollar/US Dollar',
            'GC=F': 'Gold Futures'
        }
        
        # Trading parameters
        self.risk_per_trade = 0.01  # 1% risk per trade
        self.account_balance = 10000  # Default account balance
    
    def get_forex_data(self, symbol, period='6mo', interval='1d'):
        """Get forex data using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                logging.warning(f"No data found for {symbol}")
                return None
            
            return data
        except Exception as e:
            logging.error(f"Error getting data for {symbol}: {e}")
            return None
    
    def get_realtime_quote(self, symbol):
        """Get real-time forex quote using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1m')
            
            if data.empty:
                data = ticker.history(period='5d', interval='1d')
            
            if not data.empty:
                latest = data.iloc[-1]
                return {
                    'symbol': symbol,
                    'price': latest['Close'],
                    'bid': latest['Close'] - 0.0001,
                    'ask': latest['Close'] + 0.0001,
                    'high': latest['High'],
                    'low': latest['Low'],
                    'volume': latest['Volume']
                }
            return None
        except Exception as e:
            logging.error(f"Error getting real-time quote for {symbol}: {e}")
            return None
    
    def calculate_technical_indicators(self, data):
        """Calculate comprehensive technical indicators"""
        if data is None or len(data) < 50:
            return None
        
        df = data.copy()
        
        closes = df['Close']
        highs = df['High']
        lows = df['Low']
        opens = df['Open']
        
        # Moving Averages
        df['SMA_5'] = closes.rolling(5).mean()
        df['SMA_20'] = closes.rolling(20).mean()
        df['SMA_50'] = closes.rolling(50).mean()
        df['EMA_12'] = closes.ewm(span=12, adjust=False).mean()
        df['EMA_26'] = closes.ewm(span=26, adjust=False).mean()
        
        # RSI
        df['RSI'] = self.calculate_rsi(closes)
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        # Bollinger Bands
        df['BB_Middle'] = closes.rolling(20).mean()
        bb_std = closes.rolling(20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        # Stochastic Oscillator
        df['STOCH_K'] = self.calculate_stochastic(highs, lows, closes)
        df['STOCH_D'] = df['STOCH_K'].rolling(3).mean()
        
        # Average True Range (ATR)
        df['ATR'] = self.calculate_atr(highs, lows, closes)
        
        # Support and Resistance
        df['Resistance'] = highs.rolling(20).max()
        df['Support'] = lows.rolling(20).min()
        
        # Drop NaN values
        df = df.dropna()
        
        return df
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_stochastic(self, highs, lows, closes, period=14):
        """Calculate Stochastic %K"""
        lowest_low = lows.rolling(period).min()
        highest_high = highs.rolling(period).max()
        stoch_k = ((closes - lowest_low) / (highest_high - lowest_low)) * 100
        return stoch_k
    
    def calculate_atr(self, highs, lows, closes, period=14):
        """Calculate Average True Range"""
        tr1 = highs - lows
        tr2 = abs(highs - closes.shift())
        tr3 = abs(lows - closes.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(period).mean()
        return atr
    
    def generate_trading_signals(self, technical_data, current_price):
        """Generate trading signals and return entry, SL, TP levels - MORE SENSITIVE VERSION"""
        if technical_data is None or len(technical_data) < 5:
            return {"action": "NO SIGNAL", "entry": "N/A", "sl": "N/A", "tp": "N/A"}
        
        current = technical_data.iloc[-1]
        
        # Calculate signal strength with weighted scoring
        bullish_score = 0
        bearish_score = 0
        
        # Trend analysis (weight: 2 points)
        if current['SMA_5'] > current['SMA_20']:
            bullish_score += 2
        else:
            bearish_score += 2
        
        # RSI analysis (weight: 3 points)
        rsi = current.get('RSI', 50)
        if rsi < 35:  # More sensitive oversold
            bullish_score += 3
        elif rsi < 45:  # Mild oversold
            bullish_score += 1
        elif rsi > 65:  # More sensitive overbought
            bearish_score += 3
        elif rsi > 55:  # Mild overbought
            bearish_score += 1
        
        # MACD analysis (weight: 2 points)
        if current['MACD'] > current['MACD_Signal']:
            bullish_score += 2
        else:
            bearish_score += 2
        
        # Bollinger Bands (weight: 3 points)
        bb_position = (current_price - current['BB_Lower']) / (current['BB_Upper'] - current['BB_Lower'])
        if bb_position < 0.2:  # Near lower band
            bullish_score += 3
        elif bb_position > 0.8:  # Near upper band
            bearish_score += 3
        elif bb_position < 0.4:  # Lower half
            bullish_score += 1
        else:  # Upper half
            bearish_score += 1
        
        # Stochastic (weight: 2 points)
        stoch_k = current.get('STOCH_K', 50)
        if stoch_k < 25:  # More sensitive oversold
            bullish_score += 2
        elif stoch_k > 75:  # More sensitive overbought
            bearish_score += 2
        
        # Support/Resistance (weight: 2 points)
        support = current.get('Support', current_price * 0.98)
        resistance = current.get('Resistance', current_price * 1.02)
        distance_to_support = abs(current_price - support) / current_price
        distance_to_resistance = abs(resistance - current_price) / current_price
        
        if distance_to_support < 0.005:  # Within 0.5% of support
            bullish_score += 2
        elif distance_to_resistance < 0.005:  # Within 0.5% of resistance
            bearish_score += 2
        
        # Determine action and calculate levels
        atr = current.get('ATR', 0.001)
        
        # More sensitive thresholds - only need 2 point difference
        if bullish_score > bearish_score:
            action = "BUY"
            entry = current_price
            sl = entry - (atr * 1.5)  # 1.5x ATR for stop loss
            tp = entry + (atr * 3)    # 3x ATR for take profit (2:1 risk reward)
        elif bearish_score > bullish_score:
            action = "SELL"
            entry = current_price
            sl = entry + (atr * 1.5)
            tp = entry - (atr * 3)
        else:
            action = "HOLD"
            entry = sl = tp = "N/A"
        
        return {
            "action": action,
            "entry": round(entry, 5) if action != "HOLD" else "N/A",
            "sl": round(sl, 5) if action != "HOLD" else "N/A",
            "tp": round(tp, 5) if action != "HOLD" else "N/A",
            "current_price": round(current_price, 5),
            "atr": round(atr, 5),
            "rsi": round(rsi, 1),
            "bullish_score": bullish_score,
            "bearish_score": bearish_score
        }
    
    def calculate_position_size(self, current_price, stop_loss_pips, symbol):
        """Calculate position size based on risk management"""
        if 'JPY' in symbol or symbol == 'GC=F':
            pip_value = 0.01
        else:
            pip_value = 0.0001
        
        risk_amount = self.account_balance * self.risk_per_trade
        stop_loss_amount = stop_loss_pips * pip_value
        
        if stop_loss_amount > 0:
            position_size = risk_amount / stop_loss_amount
        else:
            position_size = 0
        
        lot_size = position_size / 100000
        
        return {
            'position_size_units': int(position_size),
            'lot_size': round(lot_size, 2)
        }
    
    def analyze_forex_pair(self, symbol, description):
        """Analyze forex pair and return trading levels"""
        # Get real-time data
        realtime_data = self.get_realtime_quote(symbol)
        if not realtime_data:
            return None
        
        current_price = realtime_data['price']
        
        # Get historical data
        historical_data = self.get_forex_data(symbol, period='3mo')
        if historical_data is None:
            return None
        
        # Calculate technical indicators
        technical_data = self.calculate_technical_indicators(historical_data)
        if technical_data is None:
            return None
        
        # Generate trading signals with levels
        signals = self.generate_trading_signals(technical_data, current_price)
        
        # Calculate position size if we have a trade signal
        if signals["action"] in ["BUY", "SELL"]:
            # Calculate stop loss in pips
            if signals["action"] == "BUY":
                stop_loss_pips = (signals["current_price"] - signals["sl"]) 
            else:  # SELL
                stop_loss_pips = (signals["sl"] - signals["current_price"])
            
            # Adjust for JPY pairs and Gold
            if 'JPY' in symbol or symbol == 'GC=F':
                stop_loss_pips = stop_loss_pips / 0.01
            else:
                stop_loss_pips = stop_loss_pips / 0.0001
                
            position_info = self.calculate_position_size(current_price, stop_loss_pips, symbol)
            signals.update(position_info)
        else:
            signals.update({
                'position_size_units': 'N/A',
                'lot_size': 'N/A'
            })
        
        signals['symbol'] = symbol
        signals['description'] = description
        
        return signals
    
    def monitor_all_pairs(self):
        """Monitor all forex pairs and return trading signals"""
        print("FOREX TRADING SIGNALS WITH ENTRY/SL/TP LEVELS")
        print("=" * 120)
        print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Account Balance: ${self.account_balance:,.2f}")
        print(f"Risk per Trade: {self.risk_per_trade * 100}%")
        print("=" * 120)
        
        results = []
        
        print(f"\n{'SYMBOL':<12} {'ACTION':<8} {'CURRENT':<10} {'ENTRY':<10} {'SL':<10} {'TP':<10} {'LOTS':<8} {'RSI':<6} {'BULL':<6} {'BEAR':<6}")
        print("-" * 120)
        
        for symbol, description in self.forex_pairs.items():
            result = self.analyze_forex_pair(symbol, description)
            if result:
                results.append(result)
                
                # Color coding for actions
                action = result["action"]
                if action == "BUY":
                    action_display = f"\033[92m{action:<8}\033[0m"  # Green
                elif action == "SELL":
                    action_display = f"\033[91m{action:<8}\033[0m"  # Red
                else:
                    action_display = f"\033[93m{action:<8}\033[0m"  # Yellow
                
                print(f"{symbol:<12} {action_display} {result['current_price']:<10} "
                      f"{result['entry']:<10} {result['sl']:<10} {result['tp']:<10} "
                      f"{result['lot_size']:<8} {result['rsi']:<6} "
                      f"{result['bullish_score']:<6} {result['bearish_score']:<6}")
        
        return results
    
    def generate_detailed_reports(self, results):
        """Generate detailed trading reports for each pair"""
        print(f"\n{'=' * 100}")
        print("DETAILED TRADING REPORTS")
        print(f"{'=' * 100}")
        
        trade_signals = [r for r in results if r["action"] in ["BUY", "SELL"]]
        
        if not trade_signals:
            print("No active trading signals detected.")
            print("Market conditions appear to be ranging or uncertain.")
            return
        
        for result in trade_signals:
            print(f"\n\033[1m{result['symbol']} - {result['description']}\033[0m")
            print(f"ACTION: \033[1m{result['action']}\033[0m")
            print(f"Current Price: {result['current_price']}")
            print(f"Entry: {result['entry']}")
            print(f"Stop Loss: {result['sl']}")
            print(f"Take Profit: {result['tp']}")
            print(f"Position Size: {result['position_size_units']:,} units ({result['lot_size']} lots)")
            print(f"Risk/Reward: 1:2")
            print(f"RSI: {result['rsi']}")
            print(f"ATR (Volatility): {result['atr']}")
            print(f"Signal Score: Bullish {result['bullish_score']} vs Bearish {result['bearish_score']}")
            
            # Calculate pip distance
            if result["action"] == "BUY":
                sl_pips = (result['current_price'] - result['sl'])
                tp_pips = (result['tp'] - result['current_price'])
            else:
                sl_pips = (result['sl'] - result['current_price'])
                tp_pips = (result['current_price'] - result['tp'])
            
            # Adjust for JPY and Gold
            if 'JPY' in result['symbol'] or result['symbol'] == 'GC=F':
                sl_pips = sl_pips / 0.01
                tp_pips = tp_pips / 0.01
            else:
                sl_pips = sl_pips / 0.0001
                tp_pips = tp_pips / 0.0001
            
            print(f"Stop Loss: {sl_pips:.1f} pips")
            print(f"Take Profit: {tp_pips:.1f} pips")
            print("-" * 50)

def main():
    """Main function to run the Forex trading system"""
    forex_system = ForexTradingSystem()
    
    # Get trading signals for all pairs
    results = forex_system.monitor_all_pairs()
    
    # Generate detailed reports
    if results:
        forex_system.generate_detailed_reports(results)
        
        # Summary statistics
        buy_signals = len([r for r in results if r["action"] == "BUY"])
        sell_signals = len([r for r in results if r["action"] == "SELL"])
        hold_signals = len([r for r in results if r["action"] == "HOLD"])
        
        print(f"\n{'=' * 100}")
        print("SUMMARY STATISTICS")
        print(f"{'=' * 100}")
        print(f"Total Pairs Analyzed: {len(results)}")
        print(f"BUY Signals: {buy_signals}")
        print(f"SELL Signals: {sell_signals}")
        print(f"HOLD Signals: {hold_signals}")
        
        if buy_signals + sell_signals > 0:
            print(f"\nTrading Opportunities: {buy_signals + sell_signals} out of {len(results)} pairs")
        else:
            print(f"\nNo strong trading signals detected. Market may be in consolidation.")
    
    print(f"\nAnalysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Always use proper risk management!")

if __name__ == "__main__":
    main()