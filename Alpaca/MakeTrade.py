from Alpaca.Trades import *

# Set the global thresholds
EMOTION_SCORE_THRESHOLD = 0.25  # Threshold for emotion score, above which the sentiment is considered very positive
CORRELATION_THRESHOLD = .25  # Threshold for correlation to stock, above which and if sentiment is positive, stock will be bought
PORTFOLIO_CAP = 0.10  # Maximum proportion of total portfolio value that any individual stock can represent 
AVG_REDDIT_SCORE = 100

def make_trade_decision(reddit_score, emotion_score, emotion_type, ticker, correlation_to_stock, callback=None):
    try:
        # Get current portfolio status
        current_positions = get_all_positions()
        # Check if correlation to stock and emotion score are high enough to do any trading at all.
        if correlation_to_stock > CORRELATION_THRESHOLD and emotion_score > EMOTION_SCORE_THRESHOLD:
            print(f"Correlation and emotion score thresholds met...")
            if(callback):
                callback(f"Correlation and emotion score thresholds met...")
            if emotion_type == "NEGATIVE":
                print(f"Found strong negative sentiment")
                if(callback):
                    callback(f"Found strong negative sentiment")
                if any(position.symbol == ticker for position in current_positions):
                    # Make the trade!!!
                    close_position(ticker, callback=callback)
                else:
                    print(f"Already have no ownership in {ticker}. Good Job!")
                    if(callback):
                        callback(f"Already have no ownership in {ticker}. Good Job!")
            else:
                print(f"Found strong positive sentiment")
                if(callback):
                    callback(f"Found strong positive sentiment")
                # Get buying power
                buying_power = float(get_buying_power())
                
                if float(buying_power) > 0:
                    # STEP 1: Find max investment in order to keep allocation to the position under PORTFOLIO_CAP
                    # 1a. Get total portfolio value
                    # 1b. If the stock is in the portfolio, get the current investment value
                    # 1c. Calculate the maximum investment allowed as a cap of the total portfolio value
                    total_portfolio_value = sum([float(pos.market_value) for pos in current_positions]) + buying_power

                    # current_investment = next((float(pos['market_value']) for pos in current_positions if pos['symbol'] == ticker), 0)
                    current_investment=10000 #FIXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                    investment_cap = (total_portfolio_value * PORTFOLIO_CAP) - current_investment                    

                    # STEP 2: Decide the amount to buy based on emotion_score, and reddit_score
                    # 2a. Normalize reddit score into a scale of 0 to 1
                    # 2b. Find the suggested buy amount
                    reddit_score_normalized = reddit_score / (reddit_score + AVG_REDDIT_SCORE)
                    suggested_buy_amount = float(buying_power) * emotion_score * reddit_score_normalized * correlation_to_stock

                    # Find the min between the suggested buy amount and max investment
                    buy_amount = min(suggested_buy_amount, investment_cap)
                    # Make the trade!!!
                    buy_fractional_stock(ticker, buy_amount, callback=callback)
                else:
                    print(f"No Buying Power Left")
                    if(callback):
                        callback(f"No Buying Power Left")
        else:
            print(f"Correlation to stock or emotion score did not meet thresholds...\nNo trade")
            if(callback):
                callback(f"Correlation to stock or emotion score did not meet thresholds...\nNo trade")
    except Exception as e:
        print(f"Sorry but there was a problem trading with {ticker}... maybe it was for the best")
        if(callback):
            callback(f"Sorry but there was a problem trading with {ticker}... maybe it was for the best")
# TRY IT OUT!!!
# make_trade_decision(50, .8, 'POS', 'GME', .99)
# make_trade_decision(50, .8, 'NEG', 'GOOG', .99)
# print('hello')
