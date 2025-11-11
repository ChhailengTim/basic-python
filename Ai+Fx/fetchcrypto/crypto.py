import ccxt
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime
import ta

class TradingDataProcessor:
    def __init__(self, api_key='', secret='', sandbox=True):
        """Initialize the exchange connection"""
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret,
            'sandbox': sandbox,
        })
        self.symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT', 'DOGE/USDT']
        
    def calculate_rsi(self, prices, periods=14):
        """Calculate RSI indicator"""
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gains = pd.Series(gains).rolling(window=periods).mean()
        avg_losses = pd.Series(losses).rolling(window=periods).mean()
        
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_ema(self, prices, period):
        """Calculate EMA indicator"""
        return prices.ewm(span=period).mean()
    
    def calculate_macd(self, prices):
        """Calculate MACD indicator"""
        exp1 = prices.ewm(span=12).mean()
        exp2 = prices.ewm(span=26).mean()
        macd = exp1 - exp2
        return macd
    
    def calculate_atr(self, high, low, close, period=14):
        """Calculate Average True Range"""
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())
        
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        atr = true_range.rolling(window=period).mean()
        return atr
    
    def get_ohlcv_data(self, symbol, timeframe='3m', limit=100):
        """Get OHLCV data from exchange"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Convert to numeric
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col])
                
            return df
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
    
    def get_current_price(self, symbol):
        """Get current price for a symbol"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker['last']
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None
    
    def get_funding_rate(self, symbol):
        """Get funding rate for perpetual futures"""
        try:
            # For perpetual futures, we need to modify the symbol
            futures_symbol = symbol.replace('/', '') + ':USDT'
            funding = self.exchange.fetch_funding_rate(futures_symbol)
            return funding['fundingRate'] if funding else 0.0001
        except:
            return 0.0001  # Default funding rate
    
    def get_open_interest(self, symbol):
        """Get open interest (simulated as we need futures data)"""
        try:
            # This would typically require futures API access
            # For demo, we'll return simulated data
            price = self.get_current_price(symbol)
            return {
                'latest': float(price) * 1000 if price else 30000,
                'average': float(price) * 1000 if price else 30000
            }
        except:
            return {'latest': 30000, 'average': 30000}
    
    def get_market_data(self):
        """Get complete market data for all symbols"""
        market_data = {}
        
        for symbol in self.symbols:
            print(f"Fetching data for {symbol}...")
            
            # Get intraday data (3-minute)
            intraday_df = self.get_ohlcv_data(symbol, '3m', 30)
            if intraday_df is None:
                continue
            
            # Get longer-term data (4-hour)
            longer_term_df = self.get_ohlcv_data(symbol, '4h', 50)
            if longer_term_df is None:
                continue
            
            # Calculate indicators for intraday
            intraday_df['ema_20'] = self.calculate_ema(intraday_df['close'], 20)
            intraday_df['macd'] = self.calculate_macd(intraday_df['close'])
            intraday_df['rsi_7'] = self.calculate_rsi(intraday_df['close'], 7)
            intraday_df['rsi_14'] = self.calculate_rsi(intraday_df['close'], 14)
            
            # Calculate indicators for longer-term
            longer_term_df['ema_20'] = self.calculate_ema(longer_term_df['close'], 20)
            longer_term_df['ema_50'] = self.calculate_ema(longer_term_df['close'], 50)
            longer_term_df['macd'] = self.calculate_macd(longer_term_df['close'])
            longer_term_df['rsi_14'] = self.calculate_rsi(longer_term_df['close'], 14)
            longer_term_df['atr_3'] = self.calculate_atr(
                longer_term_df['high'], longer_term_df['low'], longer_term_df['close'], 3
            )
            longer_term_df['atr_14'] = self.calculate_atr(
                longer_term_df['high'], longer_term_df['low'], longer_term_df['close'], 14
            )
            
            coin_symbol = symbol.replace('/USDT', '')
            current_price = self.get_current_price(symbol)
            
            market_data[coin_symbol] = {
                'current_price': current_price,
                'ema_20': intraday_df['ema_20'].iloc[-1],
                'macd': intraday_df['macd'].iloc[-1],
                'rsi_7': intraday_df['rsi_7'].iloc[-1],
                'rsi_14': intraday_df['rsi_14'].iloc[-1],
                'open_interest': self.get_open_interest(symbol),
                'funding_rate': self.get_funding_rate(symbol),
                'intraday_series': {
                    'mid_prices': intraday_df['close'].tail(10).tolist(),
                    'ema_20': intraday_df['ema_20'].tail(10).tolist(),
                    'macd': intraday_df['macd'].tail(10).tolist(),
                    'rsi_7': intraday_df['rsi_7'].tail(10).tolist(),
                    'rsi_14': intraday_df['rsi_14'].tail(10).tolist()
                },
                'longer_term_context': {
                    'ema_20': longer_term_df['ema_20'].iloc[-1],
                    'ema_50': longer_term_df['ema_50'].iloc[-1],
                    'atr_3': longer_term_df['atr_3'].iloc[-1],
                    'atr_14': longer_term_df['atr_14'].iloc[-1],
                    'current_volume': longer_term_df['volume'].iloc[-1],
                    'average_volume': longer_term_df['volume'].mean(),
                    'macd_series': longer_term_df['macd'].tail(10).tolist(),
                    'rsi_14_series': longer_term_df['rsi_14'].tail(10).tolist()
                }
            }
            
            time.sleep(0.1)  # Rate limiting
        
        return market_data
    
    def simulate_account_data(self, market_data):
        """Simulate account data based on market conditions"""
        # This would normally come from your exchange account
        # For demo purposes, we simulate realistic data
        
        base_value = 10000
        total_return_pct = np.random.uniform(80, 150)
        account_value = base_value * (1 + total_return_pct / 100)
        available_cash = account_value * 0.3  # 30% cash
        
        positions = []
        position_sizes = {
            'BTC': 0.12, 'ETH': 5.74, 'SOL': 33.88, 
            'BNB': 5.64, 'XRP': 3609.0, 'DOGE': 27858.0
        }
        
        for coin, size in position_sizes.items():
            if coin in market_data:
                current_price = market_data[coin]['current_price']
                entry_price = current_price * np.random.uniform(0.85, 0.95)  # Simulate entry at lower price
                unrealized_pnl = (current_price - entry_price) * size
                
                # Calculate stop loss and profit target based on volatility
                atr = market_data[coin]['longer_term_context']['atr_14']
                stop_loss = current_price - (atr * 2)
                profit_target = current_price + (atr * 3)
                
                positions.append({
                    'symbol': coin,
                    'quantity': size,
                    'entry_price': round(entry_price, 2),
                    'current_price': round(current_price, 2),
                    'liquidation_price': round(entry_price * 0.8, 2),  # Simulated
                    'unrealized_pnl': round(unrealized_pnl, 2),
                    'leverage': 10,
                    'exit_plan': {
                        'profit_target': round(profit_target, 2),
                        'stop_loss': round(stop_loss, 2),
                        'invalidation_condition': f'If the price closes below {round(stop_loss * 0.98, 2)} on a 3-minute candle'
                    },
                    'confidence': 0.65,
                    'risk_usd': round(abs(stop_loss - entry_price) * size * 10, 4),  # With leverage
                    'notional_usd': round(current_price * size, 2)
                })
        
        return {
            'total_return_percent': round(total_return_pct, 2),
            'available_cash': round(available_cash, 2),
            'account_value': round(account_value, 2),
            'sharpe_ratio': round(np.random.uniform(0.5, 0.8), 3),
            'positions': positions
        }
    
    def format_for_ai_prompt(self, market_data, account_data):
        """Format the data into the specific structure for AI analysis"""
        
        formatted_data = f"""It has been {np.random.randint(6000, 7000)} minutes since you started trading. The current time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} and you've been invoked {np.random.randint(2500, 2700)} times. Below, we are providing you with a variety of state data, price data, and predictive signals so you can discover alpha. Below that is your current account information, value, performance, positions, etc.

ALL OF THE PRICE OR SIGNAL DATA BELOW IS ORDERED: OLDEST → NEWEST

Timeframes note: Unless stated otherwise in a section title, intraday series are provided at 3‑minute intervals. If a coin uses a different interval, it is explicitly stated in that coin's section.

CURRENT MARKET STATE FOR ALL COINS
"""
        
        for coin, data in market_data.items():
            formatted_data += f"\nALL {coin} DATA\n"
            formatted_data += f"current_price = {data['current_price']}, current_ema20 = {data['ema_20']:.3f}, current_macd = {data['macd']:.3f}, current_rsi (7 period) = {data['rsi_7']:.3f}\n\n"
            
            formatted_data += f"In addition, here is the latest {coin} open interest and funding rate for perps (the instrument you are trading):\n\n"
            formatted_data += f"Open Interest: Latest: {data['open_interest']['latest']} Average: {data['open_interest']['average']}\n\n"
            formatted_data += f"Funding Rate: {data['funding_rate']}\n\n"
            
            formatted_data += "Intraday series (by minute, oldest → latest):\n\n"
            formatted_data += f"Mid prices: {data['intraday_series']['mid_prices']}\n\n"
            formatted_data += f"EMA indicators (20‑period): {[round(x, 3) for x in data['intraday_series']['ema_20']]}\n\n"
            formatted_data += f"MACD indicators: {[round(x, 3) for x in data['intraday_series']['macd']]}\n\n"
            formatted_data += f"RSI indicators (7‑Period): {[round(x, 3) for x in data['intraday_series']['rsi_7']]}\n\n"
            formatted_data += f"RSI indicators (14‑Period): {[round(x, 3) for x in data['intraday_series']['rsi_14']]}\n\n"
            
            formatted_data += "Longer‑term context (4‑hour timeframe):\n\n"
            lt = data['longer_term_context']
            formatted_data += f"20‑Period EMA: {lt['ema_20']:.3f} vs. 50‑Period EMA: {lt['ema_50']:.3f}\n\n"
            formatted_data += f"3‑Period ATR: {lt['atr_3']:.3f} vs. 14‑Period ATR: {lt['atr_14']:.3f}\n\n"
            formatted_data += f"Current Volume: {lt['current_volume']:.3f} vs. Average Volume: {lt['average_volume']:.3f}\n\n"
            formatted_data += f"MACD indicators: {[round(x, 3) for x in lt['macd_series']]}\n\n"
            formatted_data += f"RSI indicators (14‑Period): {[round(x, 3) for x in lt['rsi_14_series']]}\n\n"
        
        formatted_data += "HERE IS YOUR ACCOUNT INFORMATION & PERFORMANCE\n"
        formatted_data += f"Current Total Return (percent): {account_data['total_return_percent']}%\n\n"
        formatted_data += f"Available Cash: {account_data['available_cash']}\n\n"
        formatted_data += f"Current Account Value: {account_data['account_value']}\n\n"
        
        formatted_data += "Current live positions & performance: "
        for i, pos in enumerate(account_data['positions']):
            formatted_data += str(pos)
            if i < len(account_data['positions']) - 1:
                formatted_data += " "
        
        formatted_data += f"\n\nSharpe Ratio: {account_data['sharpe_ratio']}\n"
        
        return formatted_data
    
    def create_ai_signal_prompt(self, market_data, account_data):
        """Create a clean prompt for AI signal generation"""
        
        prompt = """Based on the following real-time market data and current positions, generate trading signals with specific entry/exit points:

CURRENT MARKET CONDITIONS:
"""
        
        for coin, data in market_data.items():
            price_trend = "BULLISH" if data['current_price'] > data['ema_20'] else "BEARISH"
            rsi_status = "OVERSOLD" if data['rsi_7'] < 30 else "OVERBOUGHT" if data['rsi_7'] > 70 else "NEUTRAL"
            macd_status = "BULLISH" if data['macd'] > 0 else "BEARISH"
            
            prompt += f"""
{coin}:
  Price: ${data['current_price']:.2f} | Trend: {price_trend}
  EMA20: ${data['ema_20']:.2f} | RSI(7): {data['rsi_7']:.1f} ({rsi_status}) | MACD: {data['macd']:.3f} ({macd_status})
  Funding: {data['funding_rate']:.6f} | OI: {data['open_interest']['latest']:,.0f}
"""
        
        prompt += f"""
ACCOUNT OVERVIEW:
  Total Return: {account_data['total_return_percent']}% | Account Value: ${account_data['account_value']:,.2f}
  Available Cash: ${account_data['available_cash']:,.2f} | Sharpe Ratio: {account_data['sharpe_ratio']}

CURRENT POSITIONS:
"""
        
        for pos in account_data['positions']:
            pnl_percent = (pos['unrealized_pnl'] / (pos['entry_price'] * pos['quantity'])) * 100
            status = "PROFIT" if pos['unrealized_pnl'] > 0 else "LOSS"
            prompt += f"  {pos['symbol']}: {pos['quantity']} @ ${pos['entry_price']} → ${pos['current_price']} ({pnl_percent:+.1f}% {status})\n"
        
        prompt += """

GENERATE TRADING SIGNALS:
For each coin, provide:
1. SIGNAL: LONG/SHORT/HOLD
2. ENTRY: Price level
3. STOP LOSS: Price level  
4. TAKE PROFIT: Price level
5. CONFIDENCE: 0-1
6. REASONING: Technical rationale

Consider:
- RSI levels (overbought >70, oversold <30)
- MACD crossovers and momentum
- Price relative to EMA20
- Current positions and risk management
- Funding rates and market structure

Format your response as JSON with clear levels and reasoning.
"""
        
        return prompt
    
    def run_complete_analysis(self):
        """Run the complete analysis and save all data"""
        
        print("🔄 Fetching market data...")
        market_data = self.get_market_data()
        
        print("🔄 Generating account data...")
        account_data = self.simulate_account_data(market_data)
        
        print("📊 Formatting for AI...")
        # Format in the original style
        original_format = self.format_for_ai_prompt(market_data, account_data)
        with open('trading_data_original.txt', 'w') as f:
            f.write(original_format)
        
        # Create clean AI prompt
        ai_prompt = self.create_ai_signal_prompt(market_data, account_data)
        with open('ai_trading_prompt.txt', 'w') as f:
            f.write(ai_prompt)
        
        # Save structured JSON data
        structured_data = {
            'timestamp': datetime.now().isoformat(),
            'market_data': market_data,
            'account_data': account_data
        }
        with open('trading_data_structured.json', 'w') as f:
            json.dump(structured_data, f, indent=2)
        
        print("✅ Analysis complete!")
        print("📁 Files created:")
        print("   - trading_data_original.txt (original format)")
        print("   - ai_trading_prompt.txt (clean AI prompt)") 
        print("   - trading_data_structured.json (structured data)")
        print("\n📋 Copy content from 'ai_trading_prompt.txt' to ask DeepSeek AI for signals")

def main():
    """Main function to run the trading analysis"""
    
    # Initialize the processor (no API keys needed for public data)
    processor = TradingDataProcessor(api_key='', secret='', sandbox=True)
    
    try:
        processor.run_complete_analysis()
        
        # Display sample of what was created
        print("\n" + "="*50)
        print("SAMPLE OF GENERATED DATA:")
        print("="*50)
        
        with open('ai_trading_prompt.txt', 'r') as f:
            lines = f.readlines()
            for line in lines[:20]:  # Show first 20 lines
                print(line.strip())
        
        print("\n... (see full files for complete data)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have an internet connection and required packages installed.")

if __name__ == "__main__":
    main()