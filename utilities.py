#Helper Functions
# sorting, plotting, clearing screen
import matplotlib.pyplot as plt

from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    stock_list.sort(key=lambda s: s.symbol)
    # i learned that the above function is equivalent to:
    # def get_symbol(stock):
    #     return stock.symbol
    # stock_list.sort(key=get_symbol). I am just using lambda here so it's more concise.

# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    for stock in stock_list:
        stock.DataList.sort(key=lambda d: d.date)

# Function to create stock chart
def display_stock_chart(stock_list,symbol):
    select_stock = None
    for stock in stock_list:
        if stock.symbol == symbol:
            select_stock = stock
            break
    if select_stock is None:
            print("Stock symbol not found.")
            return
        # I am also making sure that the data is sorted before plotting
    select_stock.DataList.sort(key=lambda d: d.date)
    dates = [data.date for data in select_stock.DataList]
    prices = [data.close for data in select_stock.DataList]
    plt.figure(figsize=(10, 5))
    plt.plot(dates, prices, marker='o')
    plt.title(f"Stock Price History for {select_stock.symbol}")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()