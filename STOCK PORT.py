import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

API_KEY = '3LQJ98K26BFW0JCC'  # Replace with your actual API key

class StockTracker:

    def __init__(self):
        self.holdings = {}
        self.price_history = {}

    def add_shares(self, symbol, quantity):
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        print(f"Added {quantity} shares of {symbol} to your tracker.")

    def remove_shares(self, symbol, quantity):
        if symbol in self.holdings and self.holdings[symbol] >= quantity:
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            print(f"Removed {quantity} shares of {symbol} from your tracker.")
        else:
            print(f"Insufficient shares: Cannot remove {quantity} of {symbol}.")

    def view_holdings(self):
        return self.holdings

    # def get_current_price(self, symbol):
    #     url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}'
    #     response = requests.get(url)
    #     data = response.json()
    #     try:
    #         latest_close = float(list(data['Time Series (1min)'].values())[0]['4. close'])
    #         return latest_close
    #     except KeyError:
    #         print(f"Data unavailable for {symbol}. Please check the symbol and try again.")
    #         return None
    def get_current_price(self, symbol):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}'
        try:
            response = requests.get(url)
            data = response.json()
            try:
                latest_close = float(list(data['Time Series (1min)'].values())[0]['4. close'])
                return latest_close
            except KeyError:
                print(f"Data unavailable for {symbol}.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data for {symbol}: {e}")
            return None

    def calculate_total_value(self):
        total_value = 0
        for symbol, quantity in self.holdings.items():
            price = self.get_current_price(symbol)
            if price:
                total_value += price * quantity
        return total_value

    def track_price_changes(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for symbol, _ in self.holdings.items():
            if symbol not in self.price_history:
                self.price_history[symbol] = []
            price = self.get_current_price(symbol)
            if price:
                self.price_history[symbol].append((current_time, price))

    def visualize_performance(self):
        if not self.price_history:
            print("No performance data available. Track price changes first.")
            return

        plt.figure(figsize=(10, 6))
        for symbol, data in self.price_history.items():
            timestamps = [datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S') for record in data]
            prices = [record[1] for record in data]
            plt.plot(timestamps, prices, marker='o', label=symbol)

        plt.xlabel('Date and Time')
        plt.ylabel('Stock Price')
        plt.title('Stock Performance Over Time')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

tracker = StockTracker()

def main_menu():
    while True:
        print("\n1. Add Shares")
        print("2. Remove Shares")
        print("3. View Holdings")
        print("4. Check Portfolio Value")
        print("5. Track and Visualize Performance")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            symbol = input("Enter the stock symbol (uppercase): ").upper()
            quantity = int(input("Enter the number of shares to add: "))
            tracker.add_shares(symbol, quantity)
        elif choice == '2':
            symbol = input("Enter the stock symbol (uppercase): ").upper()
            quantity = int(input("Enter the number of shares to remove: "))
            tracker.remove_shares(symbol, quantity)
        elif choice == '3':

            print("Current Portfolio:", tracker.view_holdings())

        elif choice == '4':

            total_value = tracker.calculate_total_value()

            print(f"Total Portfolio Value: ${total_value:.2f}")

        elif choice == '5':

            tracker.track_price_changes()

            tracker.visualize_performance()

        elif choice == '6':

            break

        else:

            print("Invalid choice. Please try again.")



if __name__ == "__main__":

    main_menu()