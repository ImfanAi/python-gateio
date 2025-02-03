# Gate.io Futures Trading CLI

This project provides a command-line interface (CLI) for trading futures on Gate.io. You can open and close positions in the futures market using simple commands.

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.x installed on your machine.
- A Gate.io account with API access enabled.
- Your API key and secret from Gate.io.

## Installation

1. **Install the required libraries**:
Create a virtual environment (optional but recommended):
`python -m venv venv`<br />
Activate the virtual environment:

- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```
  source venv/bin/activate
  ```

2. **Install dependencies**:<br />
Run:  `pip install -r requirements.txt`

## Configuration

Open `main.py` and replace the placeholders for your API key and secret:

`key="YOUR_API_KEY", # Replace with your API key
secret="YOUR_API_SECRET" # Replace with your API secret`

## Usage

### Opening a Position

To open a new futures position, use the following command:

`python main.py open <symbol> <amount> <leverage> <position_type> [--take_profit <value>] [--stop_loss <value>]`


**Parameters:**

- `<symbol>`: The token symbol (e.g., `DOGEUSDT`).
- `<amount>`: The amount in USD to open the position (e.g., `20`).
- `<leverage>`: The leverage to use (e.g., `20` for 20x).
- `<position_type>`: The type of position (`long` or `short`).
- `--take_profit`: Optional; take profit percentage (e.g., `0.2` for 20%).
- `--stop_loss`: Optional; stop loss percentage (e.g., `0.4` for 40%).

**Example:**

`python main.py open DOGEUSDT 20 20 long --take_profit 0.2 --stop_loss 0.4
`


### Closing a Position

To close an existing futures position, use the following command:

`python main.py close <symbol>`


**Parameters:**

- `<symbol>`: The token symbol (e.g., `DOGEUSDT`).

**Example:**

`python main.py close DOGEUSDT`


## Important Notes

- Ensure that your API key has permissions to trade on the futures market.
- Always test with small amounts or in a simulated environment before executing trades with real funds.
- Monitor your open positions and orders regularly to manage risk effectively.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

[]
