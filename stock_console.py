# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

# Add new stock to track
def add_stock(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("- Add New Stock")
        symbol = input("Enter Stock Symbol (or 0 to cancel): ").upper()
        if symbol == "0":
            return
        name = input("Enter Stock Name: ")
        shares = input("Enter Number of Shares: ")
        try:
            shares = int(shares)
            n_stock = Stock(symbol,name,shares)
            stock_list.append(n_stock)
            print(f"Stock {symbol} added successfully.")
            option = "0"
        except:
            print("Invalid number of shares and Try again!")
            input("Press Enter to continue...")

# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        print("- Update Shares")
        symbol = input("Enter Stock Symbol (or 0 to cancel): ").upper()
        if symbol == "0":
            return
        stock = None
        for stock in stock_list:
            if stock.symbol == symbol:
                stock = stock
                break
        if stock is None:
            print("Stock symbol not found.")
            input("Press Enter to continue...")
            continue
        shares = input("Enter new number of shares: ")
        try:
            shares = int(shares)
            stock.shares = shares
            print(f"Shares for {symbol} updated successfully.")
            option = "0"
        except:
            print("Invalid number of shares and Try again!")
            input("Press Enter to continue...")

# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    print("Stock List: [",end="")
    # I am printing only the available stocks for buying
    for i, stock in enumerate(stock_list):
        if i > 0:
            print(", ",end="")
        print(f"{stock.symbol} ({stock.shares} shares)",end="")
    print("]")

    symbol = input("Enter Stock Symbol to Buy (or 0 to cancel): ").upper()
    if symbol == "0":
        return
    selected_stock = None
    for s in stock_list:
        if s.symbol.upper() == symbol:
            selected_stock = s
            break
    if selected_stock is None:
        print("Stock symbol not found.")
        input("Press Enter to continue...")
        return
    shares_input = input("Enter number of shares to buy: ")
    try:
        shares = int(shares_input)
        # I am also adding code to make sure that the shares value are not negative
        if shares <= 0:
            print("Number of shares must be positive!")
            input("Press Enter to continue...")
            return
        selected_stock.buy(shares) # calling buy method from Stock class
        print(f"Bought {shares} shares of {symbol} successfully.")
    except:
        print("Invalid number of shares and Try again!")
        input("Press Enter to continue...")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ---")
    print("Stock List: [",end="")
    for i, stock in enumerate(stock_list):
        if i > 0:
            print(", ",end="")
        print(f"{stock.symbol} ({stock.shares} shares)",end="")
    print("]")

    symbol = input("Enter Stock Symbol to Sell (or 0 to cancel): ").upper()
    if symbol == "0":
        return 
    selected_stock = None
    for s in stock_list:
        if s.symbol.upper() == symbol:
            selected_stock = s
            break
    if selected_stock is None:
        print("Stock symbol was not found.")
        input("Press Enter to continue...")
        return 
    
    shares_input = input("Enter number of shares to sell: ")
    try:
        shares = int(shares_input)
        if shares <= 0:
            print("Number of shares must be positive!")
            input("Press Enter to continue...")
            return
        if shares > selected_stock.shares:
            print("Cannot sell more shares than you own!")
            input("Press Enter to continue...")
            return
        selected_stock.sell(shares) # sell method from stock class
        print(f"Sold {shares} shares of {selected_stock.symbol} successfully.")
    except:
        print("Invalid number of shares and Try again!")
        input("Press Enter to continue...")

# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    print("Delete Stock ---")
    if len(stock_list == 0):
        print("No stocks to delete.")
        input("Press Enter to continue...")
        return
    print("Stock List: [",end="")
    for i, stock in enumerate(stock_list):
        if i > 0:
            print(", ",end="")
        print(f"{stock.symbol} ({stock.shares} shares)",end="")
    print("]")

    symbol = input("Enter Stock Symbol to Delete (or 0 to cancel): ").upper()
    if symbol == "0":
        return

    selected_stock = None
    for s in stock_list:
        if s.symbol.upper() == symbol:
            selected_stock = s
            break

    if selected_stock is None:
        print("Stock symbol not found.")
        input("Press Enter to continue...")
        return

    confirm = input(f"Are you sure you want to delete {selected_stock.symbol} and ALL its daily data? (Y/N): ").strip().upper()
    if confirm != "Y":
        print("Deletion cancelled.")
        input("Press Enter to continue...")
        return

    try:
        stock_list.remove(selected_stock)
    except ValueError:
        pass

    print(f"Stock {selected_stock.symbol} deleted successfully.")
    input("Press Enter to continue...")


# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    if not stock_list:
        print("No stocks are being tracked right now.")
    else:
        print("Stock List: [",end="")
        for i, stock in enumerate(stock_list):
            if i > 0:
                print(", ",end="")
            print(f"{stock.symbol} ({stock.shares} shares)",end="")
        print("]")

    input("Press enter to continue...")

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    

# Display Report for All Stocks
def display_report(stock_data):
    clear_screen()
    print("Stock Report ---")
    for stock in stock_data:
        pass


  


# Display Chart
def display_chart(stock_list):
    print("Stock List: [",end="")
    for stock in stock_list:
        pass

# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        pass


# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    pass

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    pass

# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()