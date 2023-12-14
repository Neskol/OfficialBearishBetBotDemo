from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
# from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from configparser import ConfigParser
import math

config = ConfigParser()
config.read('./Alpaca/alpaca.ini')

key = config.get('BearishBetsBot', 'API_KEY')
secret = config.get('BearishBetsBot', 'API_SECRET')

trading_client = TradingClient(key, secret, paper=True)

def get_all_positions(callback=None):
    try:
        # Get a list of all of our positions.
        portfolio = trading_client.get_all_positions()
        return portfolio
    except Exception:
        print("There was a problem getting all positions.")
        if callback:
            callback("There was a problem getting all positions.")
        return None
    
def get_buying_power(callback=None):
    try:
        # Get our account information.
        account = trading_client.get_account()
        # Check if our account is restricted from trading.
        if account.trading_blocked:
            return 0 #Account is currently restricted from trading
        return float("{0:.2f}".format(float(account.buying_power))) # How much money we can use to open new positions.
    except Exception:
        print("There was a problem getting buying power.")
        if callback:
            callback("There was a problem getting buying power.")
        return None

def get_position(symbol, callback=None):
    try:
        position = trading_client.get_open_position(symbol)
        return position
    except Exception:
        print(f"There was a problem getting the position for {symbol}.")
        if callback:
            callback(f"There was a problem getting the position for {symbol}.")
        return None
    

def buy_fractional_stock(symbol, amount, callback=None):
    notional = math.floor(float(amount))
    try:
        print(f'ATTEMPTING TO BUY ${notional:,.2f} WORTH OF {symbol}')
        if callback:
            callback(f'ATTEMPTING TO BUY ${notional:,.2f} WORTH OF {symbol}')
        market_order_data = MarketOrderRequest(
            symbol=symbol,
            notional=float(notional),
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY
        )
        # submit the limit order
        order = trading_client.submit_order(order_data=market_order_data)
        print(f'🚀🚀🚀🤑💰💸✅💲🔮💎🌙🏆🎯📊🚀🚀🚀\nBUY ORDER PLACED FOR ${notional:,.2f} WORTH OF {symbol}\n🚀🚀🚀🤑💰💸✅💲🔮💎🌙🏆🎯📊🚀🚀🚀')
        if callback:
            callback(f'🚀🚀🚀🤑💰💸✅💲🔮💎🌙🏆🎯📊🚀🚀🚀\nBUY ORDER PLACED FOR ${notional:,.2f} WORTH OF {symbol}\n🚀🚀🚀🤑💰💸✅💲🔮💎🌙🏆🎯📊🚀🚀🚀')
        return order
    except Exception:
        print(f"There was a problem buying fractional shares of {symbol}.")
        if callback:
            callback(f"There was a problem buying fractional shares of {symbol}.")
        return None

def close_position(symbol, callback=None):
    try:
        print(f'ATTEMPTING TO CLOSE POSITION IN {symbol}')
        if callback:
            callback(f'ATTEMPTING TO CLOSE POSITION IN {symbol}')
        order = trading_client.close_position(symbol)
        print(f'🚀🚀🚀🤑💰💸✅💲🔮💎🌙🏆🎯📊🚀🚀🚀\nCLOSING POSITION IN {symbol}\n🚀🚀🚀🤑💰💸✅💲🔮💎🌙🏆🎯📊🚀🚀🚀')
        if callback:
            callback(f'🚀🚀🚀🤑💰💸✅💲🔮💎🌙🏆🎯📊🚀🚀🚀\nCLOSING POSITION IN {symbol}\n🚀🚀🚀🤑💰💸✅💲🔮💎🌙🏆🎯📊🚀🚀🚀')
        return order
    except Exception:
        print(f"There was a problem closing the position in {symbol}.")
        if callback:
            callback(f"There was a problem closing the position in {symbol}.")
        return None
    

# Havn't tested yet
# def sell_stock(symbol, quantity):
#     market_order_data = MarketOrderRequest(
#         symbol=symbol,
#         qty=quantity,
#         side=OrderSide.SELL,
#         time_in_force=TimeInForce.DAY
#     )
#     market_order = trading_client.submit_order(order_data=market_order_data)
#     return market_order