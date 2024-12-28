from message import Message 
import json 
import re
from datetime import datetime, timedelta, timezone
from binance.client import Client

# Set your API key and secret
api_key = 'TciargnDf3WDndjshzKlg736w1e3PGMyhr3WfGT2uCaPWgKqv3kpHEyT8KadpKmL'
api_secret = 'T8HhDSeXzGLsUhhhDjMKk33WNuhobZkUVXhuEGUorLcL9xQqcIDCbKWq9304GLwj'

# # Initialize the Binance client
client = Client(api_key, api_secret)



def enterTrade(msg):
    # TO:DO parse the message send
    
    balance , trading = getStatus()
    float_balane = float(balance)
    if (trading):
        if (is_time_difference_exceeded(msg.date, k=2)):
            infoMsg = parse_coin_data(msg.text)
            if (infoMsg['type'] == "Halal"):
                place_buy_order(infoMsg['coin_name'], float_balane)

                print("Enter Trade , Coin : {0} , new pirce : {1} , target : {2}".format(infoMsg['coin_name'],infoMsg['new_price'],infoMsg['target_price']))
            else:
                print("trade haram")
    else:
        print("status is disactivated")
    return 

    
def getStatus():
    with open("status.json", "r") as file:
        data = json.load(file)
    return data["balance"], data["trading"]

def parse_coin_data(text):
    # Extract the coin name (e.g., STGUSDT)
    coin_match = re.search(r'#(\w+)', text)
    coin_name = coin_match.group(1) if coin_match else None

    # Extract the type (Haram or Halal)
    type_match = re.search(r'⚡️ Shariah Status: ❌ (Haram)|✅ (Halal)', text)
    coin_type = 'Haram' if type_match and type_match.group(1) else 'Halal' if type_match and type_match.group(2) else None

    # Extract the new price
    new_price_match = re.search(r'💰 New Price: ([\d.]+)', text)
    new_price = float(new_price_match.group(1)) if new_price_match else None

    # Extract the target price
    target_match = re.search(r'🎯 1% Target: ([\d.]+)', text)
    target_price = float(target_match.group(1)) if target_match else None

    return {
        'coin_name': coin_name,
        'type': coin_type,
        'new_price': new_price,
        'target_price': target_price
    }



def is_time_difference_exceeded(d1, k=5):
    try:
        # Parse d1 into a datetime object
        d1_datetime = datetime.fromisoformat(d1)

        # Get the current PC time in UTC+1
        pc_time = datetime.now(timezone.utc).astimezone(tz=timezone(timedelta(hours=1)))

        # Calculate the difference in seconds
        time_difference = abs((pc_time - d1_datetime).total_seconds())

        # Return True if the difference exceeds the threshold
        return time_difference < k
    except ValueError:
        # Return False if d1 format is invalid
        return False

# Example usage


def place_buy_order(symbol, spend_amount):
    """
    Places a market buy order using a specified amount of your spot balance.

    Args:
        symbol (str): The trading pair (e.g., BTCUSDT).
        spend_amount (float): The amount in the quote currency to spend (e.g., USDT).

    Returns:
        dict: The response from the Binance API.
    """
    try:
        # Get the latest price for the symbol
        ticker = client.get_symbol_ticker(symbol=symbol)
        current_price = float(ticker['price'])

        # Calculate the quantity to buy (amount in base asset)
        quantity = spend_amount / current_price

        # Adjust for Binance's minimum quantity precision
        symbol_info = client.get_symbol_info(symbol)
        step_size = float(next(
            filter(lambda f: f['filterType'] == 'LOT_SIZE', symbol_info['filters'])
        )['stepSize'])

        quantity = round(quantity - (quantity % step_size), 8)  # Adjust for step size

        # Place the market buy order
        order = client.create_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        return order

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
# symbol = "BTCUSDT"     # Trading pair
# spend_amount = 50.0    # Spend 50 USDT to buy BTC

# order_response = place_buy_order(symbol, spend_amount)
# print(order_response)


#
def get_spot_balance(asset):
    """
    Get the available spot balance for a specific asset.

    Args:
        asset (str): The asset to check balance for (e.g., USDT).

    Returns:
        float: The available balance.
    """
    try:
        account_info = client.get_account()
        balance = next(b for b in account_info['balances'] if b['asset'] == asset)
        return float(balance['free'])
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0.0
