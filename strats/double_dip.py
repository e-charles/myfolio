import numpy as np

# double dip in SMA does not really make sense since 
def sma_strategy(data, crossover, crossunder):
    # Initialize variables
    entry_price_long = np.nan
    entry_price_short = np.nan
    total_trades = 0
    winning_trades = 0
    total_profit = 0.0
    total_loss = 0.0

    i = 1
    while i < len(data):
        trade_profit = np.nan

        if i + 2 >= len(data): # make sure i + 1 is within bounds 
            break # no more pairs to check 
        # checks [crossunder, no crossover, crossunder] for cross unders
        if (crossunder.iloc[i] and not crossover.iloc[i + 1] and crossunder.iloc[i + 2] and np.isnan(entry_price_long) or \
            crossunder.iloc[i] and crossunder.iloc[i + 1]  and np.isnan(entry_price_long)): # crosses under consecutivly 
            entry_price_long = data['Close'].iloc[i + 1]
            total_trades += 1
            #i += 2 # skips an iteration 
            continue
        # checks [Low, None, Low]
        elif (crossover.iloc[i] and not crossunder.iloc[i + 1] and crossover.iloc[i + 1] and not np.isnan(entry_price_long) or \
        crossover.iloc[i] and crossover.iloc[i + 1]  and not np.isnan(entry_price_long)): # crosses above twice 
            trade_profit = data['Close'].iloc[i + 1] - entry_price_long
            
            if trade_profit > 0:
                total_profit += trade_profit
                winning_trades += 1
            else:
                total_loss -= trade_profit

            entry_price_long = np.nan # closes the active long position     
            #i += 2 # skips an iteration 
            continue

        i += 1 # normal increment 
                
    return total_trades, winning_trades, total_profit, total_loss

def rsi_strategy(data, buy_signal, sell_signal):
    # Initialize variables
    entry_price_long = np.nan
    total_trades = 0
    winning_trades = 0
    total_profit = 0.0
    total_loss = 0.0

    i = 0
    while i < len(data) - 2:
        # Buy on consecutive oversold signals
        # signal + nuetral + signal 
        if np.isnan(entry_price_long): 
            if (buy_signal.iloc[i] and not sell_signal.iloc[i + 1] and buy_signal.iloc[i + 2]):
                entry_price_long = data['Close'].iloc[i+2]
                total_trades += 1
                i += 2
                continue
            
            # signal + signal 
            if (buy_signal.iloc[i] and buy_signal.iloc[i + 1]):
                entry_price_long = data['Close'].iloc[i + 1]
                total_trades += 1
                i += 1
                continue

        # Sell on consecutive overbought signals
        # signal + nuetral + signal 
        if not np.isnan(entry_price_long):
            if (sell_signal.iloc[i] and not buy_signal.iloc[i + 1] and sell_signal.iloc[i + 2]):
                trade_profit = data['Close'].iloc[i + 2] - entry_price_long
                if trade_profit > 0:
                    total_profit += trade_profit
                    winning_trades += 1
                else:
                    total_loss -= trade_profit
                entry_price_long = np.nan
                i += 2
                continue

            # signal + signal 
            if (sell_signal.iloc[i] and sell_signal.iloc[i + 1]):
                trade_profit = data['Close'].iloc[i + 1] - entry_price_long
                if trade_profit > 0:
                    total_profit += trade_profit
                    winning_trades += 1
                else:
                    total_loss -= trade_profit
                entry_price_long = np.nan
                i += 1
                continue
        i += 1
                
    return total_trades, winning_trades, total_profit, total_loss