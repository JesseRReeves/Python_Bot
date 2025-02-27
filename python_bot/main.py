from services.coingecko_service import CoinGecko
from services.exchange_service import Binance
from services.saving_service import SavingService
from utils.load_config import config
from utils.logger import logging
import time




# Initialize Our services

cg = CoinGecko()
exchange = Binance()
trades = SavingService("assets/trades.json")
portfolio = SavingService("assets/portfolio.json")


print(
    "THE BOT WILL PLACE LIVE ORDERS. Use the Keyboard interrupt (Ctrl + C or Cmd + C) to cancel execution. Waiting 10s before starting execution..."
)
time.sleep(10)

# The bot starts by checking the configured mode (either "GAINING" or "LOSING"). Based on this
#  setting, it will trade either the top gaining or top losing assets.

def main():
    # Set the Trading mode
    if config.mode =="GAINING":
        all_assets = cg.get_top_gainers_and_losers().top_gainers
        logging.info(f"Trading the {config.number_of_assets} Top Gaining assets")
    elif config.mode == "LOSING":
        all_assets = cg.get_top_gainers_and_losers().top_losers
        logging.info(f"Trading the {config.number_of_assets} Top Losing assets")
    else:
        logging.error(
            f"Invalid mode, please choose between GAINING and LOSING in config.json"
        )
        return # Exit if the mode is invalid

# Next, the bot selects the top assets based on the number specified in the configuration 
# (config.number_of_assets). For instance, if this number is set to 5, the bot will only trade 
# the top 5 assets returned.

    top_assets = all_assets[0 : config.number_of_assets]

# BUY Logic

# The bot then attempts to purchase each selected asset using the configured amount and 
# currency. If the purchase is successful, the order is logged in both portfolio.json and 
# trades.json for future reference. The reason for saving buys in 2 separate files is because 
# trades represent a historical view of all orders placed, while the portfolio only contains
#  assets that the bot holds. The files are available under the assets directory and are 
# automatically created.

    for asset in top_assets:
        try:
            res = exchange.buy(asset.symbol.upper(), config.amount, config.vs_currency)
            # Saving the order to Orders and Trades. We log the trade for historical purposes, and 
            # we add our order to our portfolio so we know what we hold.
            portfolio.save_order(res)
            trades.save_order(res)
            logging.info(
                f"Bought {res.executredQty} {res.symbol} at ${res.fills[0].price}. "
            )
        except Exception as e:
            logging.error(f"COULD NOT BUY {asset.symbol}: {e} ")

    # Update Take-Profit / Stop-Loss and SELL Logic
    # Next, the bot monitors the performance of assets in the portfolio. It checks the current price
    #  against the original purchase price and calculates the profit or loss percentage. If the
    #  price change exceeds the configured take-profit or stop-loss thresholds, the bot triggers a 
    # sell order.

    all_portfolio_assets = portfolio.load_orders()
    for order in all_portfolio_assets:
        original_price = float(order.fills[0].price)
        current_price = exchange.get_current_price(order.symbol)
        current_pnl = (current_price - original_price) / original_price * 100

        if current_pnl > config.take_profit or current_pnl < config.stop_loss:
            logging.info(
                f"SELL signal generated for {order.executedQty} {order.symbol} with order Id {order.orderId}"
            )

            # The summed up fees from all fills
            # The sell logic also accounts for transaction fees, deducting them from the sale amount
            #  before executing the trade. Once the sell is completed, the order is removed from 
            # the portfolio and saved in the trades for historical tracking.
            
            fees = sum([float(item.commission) for item in order.fills])

            try:
                amount_in_vs_currency = round(
                    current_price * (float(order.executedQty) - fees), 4
                )
                res = exchange.sell(order.symbol.upper(), amount_in_vs_currency)

                trades.save_order(res)
                portfolio.delete_order(order.orderId)
                logging.info(
                f"SOLD {res.executedQty} {res.symbol} at ${res.fills[0].price}. "
                )
            except Exception as e:
                logging.error(
                    f"COULD NOT SELL {order.executedQty} {order.symbol}: {e} "
                )

# To run this logic on a loop, we just need to call the main() function inside a loop, and add
#  our sleep timer from the bot’s configuration.

if __name__ == "__main__":
    while True:
        main()
        logging.info(
            f"Successfully completed bot cycle, waiting {config.bot_frequency_in_seconds} seconds before re-running..."
        )
        time.sleep(config.bot_frequency_in_seconds)

