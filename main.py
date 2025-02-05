import argparse
import gate_api
from gate_api.exceptions import GateApiException, ApiException

# Function to open a futures position
def open_futures_position(symbol, amount, leverage, position_type, take_profit, stop_loss):
    
    # Configure API key authorization
    configuration = gate_api.Configuration(
        host="https://fx-api-testnet.gateio.ws/api/v4",
        key="61f122139462617db230d6c84bf4ed4b",
        secret="7ce479bf23d9b5316109f2fddf9adc72d3e0c7b7b9c7c891d8ff784497a39625"
    )
    # Create an instance of the API class
    api_client = gate_api.ApiClient(configuration)
    futures_api = gate_api.FuturesApi(api_client)

    try:
        # Get the current market price
        tickers = futures_api.list_futures_tickers('usdt', contract=symbol)
        current_price = float(tickers[0].last)
        current_price = round(current_price, 12)

        # Calculate the size based on the amount and current price
        size = int(amount / current_price)


        # Adjust size for leverage
        size *= leverage

        # Adjust size sign based on position type
        if position_type.lower() == 'short':
            size = -size

        # Prepare the order
        settle = 'usdt'
        contract = symbol
        tif = 'gtc'  # time in force: good till cancelled

        # Create the order object
        order = gate_api.FuturesOrder(
            contract=contract,
            size=size,
            price=str(current_price),
            tif=tif
        )

        # Set leverage
        # futures_api.update_position_leverage(settle, contract, {'leverage': str(leverage)})
        futures_api.update_position_leverage(settle, contract, str(leverage))

        # Create the futures order
        order_response = futures_api.create_futures_order(settle, order)
        print(f"Order placed: {order_response}")

        # Set take profit and stop loss
        if take_profit > 0:
            tp_trigger = current_price * (1 + take_profit) if position_type.lower() == 'long' else current_price * (1 - take_profit)
            print(f"Take profit trigger: {tp_trigger}")
            tp_trigger = round(tp_trigger, 12)
            tp_order = gate_api.FuturesOrder(
                contract=contract,
                size=-size,
                price=str(tp_trigger),
                tif='gtc',
                close=False,
                reduce_only=True
            )
            tp_response = futures_api.create_futures_order(settle, tp_order)
            print(f"Take profit order placed: {tp_response}")

        if stop_loss > 0:
            sl_trigger = current_price * (1 - stop_loss) if position_type.lower() == 'long' else current_price * (1 + stop_loss)
            print(f"Take Loss trigger: {sl_trigger}")
            sl_trigger = round(sl_trigger, 12)
            sl_order = gate_api.FuturesOrder(
                contract=contract,
                size=0,
                price=str(sl_trigger),
                # price=1,
                tif='gtc',
                close=True,
                reduce_only=True
            )
            sl_response = futures_api.create_futures_order(settle, sl_order)
            print(f"Stop loss order placed: {sl_response}")

    except GateApiException as ex:
        print(f"Gate API exception, label: {ex.label}, message: {ex.message}")
    except ApiException as e:
        print(f"Exception when calling FuturesApi: {e}")

# Function to close a futures position
def close_futures_position(symbol):
    # Configure API key authorization
    configuration = gate_api.Configuration(
        host="https://fx-api-testnet.gateio.ws/api/v4",
        key="61f122139462617db230d6c84bf4ed4b",
        secret="7ce479bf23d9b5316109f2fddf9adc72d3e0c7b7b9c7c891d8ff784497a39625"
    )
    # Create an instance of the API class
    api_client = gate_api.ApiClient(configuration)
    futures_api = gate_api.FuturesApi(api_client)

    try:
        
        # Get all open positions for the symbol
        positions = futures_api.list_positions('usdt')
        for position in positions:
            if position.contract == symbol and position.size != 0:
                # Close the position
                close_order = gate_api.FuturesOrder(
                    contract=symbol,
                    size=0,  # Close the entire position
                    price=str(position.mark_price),  # Use last price for closing
                    tif='gtc',
                    close=True
                )
                futures_api.create_futures_order('usdt', close_order)
                print(f"Closed position for {symbol}: {position.size}")

        # Cancel all open orders related to the symbol
        open_orders = futures_api.list_futures_orders('usdt', contract=symbol, status='open')
        print(f"open_orders: {open_orders}")
        for order in open_orders:
            futures_api.cancel_futures_order('usdt', order.id)
            print(f"Cancelled order: {order.id} for {symbol}")

        

    except GateApiException as ex:
        print(f"Gate API exception, label: {ex.label}, message: {ex.message}")
    except ApiException as e:
        print(f"Exception when calling FuturesApi: {e}")

# Main function to handle CLI input
def main():
    parser = argparse.ArgumentParser(description="Gate.io Futures Trading CLI")
    
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Open Position Command
    open_parser = subparsers.add_parser('open', help='Open a new futures position')
    open_parser.add_argument('symbol', type=str, help='Token symbol (e.g., DOGE_USDT)')
    open_parser.add_argument('amount', type=float, help='Amount in USD to open the position')
    open_parser.add_argument('leverage', type=int, help='Leverage (e.g., 20 for 20x)')
    open_parser.add_argument('position_type', type=str, choices=['long', 'short'], help='Position type (long or short)')
    open_parser.add_argument('--take_profit', type=float, default=0.0, help='Take profit percentage (e.g., 0.2 for 20%)')
    open_parser.add_argument('--stop_loss', type=float, default=0.0, help='Stop loss percentage (e.g., 0.4 for 40%)')

    # Close Position Command
    close_parser = subparsers.add_parser('close', help='Close an existing futures position')
    close_parser.add_argument('symbol', type=str, help='Token symbol (e.g., DOGE_USDT)')

    args = parser.parse_args()

    if args.command == 'open':
        open_futures_position(args.symbol, args.amount, args.leverage, args.position_type, args.take_profit, args.stop_loss)

    elif args.command == 'close':
        close_futures_position(args.symbol)

if __name__ == "__main__":
    main()
