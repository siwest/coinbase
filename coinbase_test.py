from coinbase.wallet.client import Client
from coinbase.wallet.error import TwoFactorRequiredError
import time


def maxProfit(prices):
    """
    :type prices: List[int]
    :rtype: int, int, int
    """
    maximum = 0
    buy_day = 0
    sell_day = 0
    for i in range(len(prices)-1):
        sell_price = max(prices[i+1:])
        buy_price = min(prices[:i+1])
        profit = sell_price - buy_price
        transaction_cost = buy_price * .03 + sell_price * .03

        if profit > transaction_cost:
            maximum = max(maximum, profit)

    return maximum, buy_day, sell_day


client = Client(
    api_key='',
    api_secret=''
)

historic_prices = client.get_historic_prices()
price_list = [float(day['price']) for day in historic_prices['prices']]
print(price_list)
max_profit = maxProfit(price_list)
print("Max profit:  $" + str(max_profit))

for i in range(10):
    time.sleep(10)
    print("Buy price " + str(client.get_buy_price(currency_pair='BTC-USD')))
    print("Sell price " + str(client.get_sell_price(currency_pair='BTC-USD')))
    print("Spot price " + str(client.get_spot_price(currency_pair='BTC-USD')))
