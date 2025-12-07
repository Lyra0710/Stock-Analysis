# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData
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
        clear_screen()
        print("Update Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Exit Update Shares")
        option = input("Enter Menu Option: ")

        while option not in ["1", "2", "0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Update Shares ---")
            print("1 - Buy Shares")
            print("2 - Sell Shares")
            print("0 - Exit Update Shares")
            option = input("Enter Menu Option: ")
        if option == "1":
            buy_stock(stock_list)     
        elif option == "2":
            sell_stock(stock_list)     
        else:
            print("Returning to Manage Stocks")

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
    if not stock_list:
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
        print("Stock List:",end="")
        print()
        print(f"{'SYMBOL':<10}{'NAME':<20}{'SHARES':>10}")
        for stock in stock_list:
            print(f"{stock.symbol:<10}{stock.name:<20}{stock.shares:>10}")

    input("Press enter to continue...")

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    if not stock_list:
        print("No stocks available. Add a stock first. ")
        input("Press Enter to continue...")
        return
    list_stocks(stock_list)
    symbol = input("Enter stock symbol to add data for (or 0 to cancel): ").upper()
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
    # I need to ask for additional details such as date, price and volume of stocks
    date_input = input("Enter data (mm/dd/yy): ")
    try:
        date_value = datetime.strptime(date_input, "%m/%d/%y")
    except:
        print("Invalid date format. Please use MM/DD/YY.")
        input("Press Enter to continue...")
        return
    price_input = input("Enter closing price: ")
    try:
        price = float(price_input)
        if price <=0:
            print("The price must be positive!")
            input("Press Enter to continue...")
    except:
        print("Invalid Price! Must be a number")
        input("Press Enter to continue...")
        return
    volume_input = input("Enter volume: ")
    try:
        volume_value = int(volume_input)
        if volume_value < 0:
            print("Value cannot be negative!")
            input("Press Enter to continue...")
            return
    except:
        print("Invalid Volume! must be an integer.")
        input("Press Enter to continue...")
        return
    
    # I need to also add new daily data that we just got into the selected block
    daily_data = DailyData(date_value, price, volume_value)
    selected_stock.add_data(daily_data)

    print(f"Added daily data for {symbol} on {date_input}.")
    input("Press Enter to continue...")

# Display Report for All Stocks
def display_report(stock_list): # initially this was using stock_data. But, it's later called with stock_list as input so i changeed it 
    clear_screen()
    print("Stock Report ---")
    if not stock_list:
        print("No stocks are currently being tracked.")
        input("Press Enter to continue...")
        return
    sortStocks(stock_list)
    sortDailyData(stock_list)
    portfolio_total = 0.0
    for stock in stock_list:
        print(f"Symbol: {stock.symbol}")
        print(f"Name  : {stock.name}")
        print(f"Shares: {stock.shares}")
    # i need to deal with cases where there is no daily data as well
        if not stock.DataList:
            print("  No daily price data available.")
            continue
        closes = [d.close for d in stock.DataList]
        recent = stock.DataList[-1]
        high = max(closes)
        low = min(closes)
        average = sum(closes)/len(closes)

        pos_val = stock.shares * recent.close
        portfolio_total += pos_val

        print("Summary of this stock: ")
        print(f"Most Recent Date : {recent.date.strftime('%m/%d/%y')}") 
        print(f"Most Recent Close: ${recent.close:,.2f}")
        print(f"High Close       : ${high:,.2f}")
        print(f"Low Close        : ${low:,.2f}")
        print(f"Average Close    : ${average:,.2f}")
        print(f"Position Value   : ${pos_val:,.2f}") 
        input("Press Enter to continue...")      


# Display Chart
def display_chart(stock_list):
    clear_screen()
    print("Display Stock Chart ---", end="\n")
    if not stock_list:
        print("No stocks are currently being tracked right now.")
        input("Press Enter to continue...")
        return
    
    print("Stock List: [", end="") # showing which stocks are there right now before making the chart
    for i, stock in enumerate(stock_list):
        if i > 0:
            print(", ", end="")
        print(stock.symbol, end="")
    print("]")

    symbol = input("Enter Stock Symbol to Display Chart (or 0 to cancel): ").upper()
    if symbol == "0":
        return
    
    display_stock_chart(stock_list, symbol)
    input("Press Enter to continue...")
# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data ---")
        print("1 - Save Stock Data to Database")
        print("2 - Load Stock Data from Database")
        print("3 - Retrieve Stock Data from Web")
        print("4 - Import Stock Data from CSV")
        print("0 - Exit Manage Data")
        option = input("Enter Menu Option: ")

        while option not in ["1", "2", "3", "4", "0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Manage Data ---")
            print("1 - Save Stock Data to Database")
            print("2 - Load Stock Data from Database")
            print("3 - Retrieve Stock Data from Web")
            print("4 - Import Stock Data from CSV")
            print("0 - Exit Manage Data")
            option = input("Enter Menu Option: ")

        if option == "1":
            stock_data.save_stock_data(stock_list)
            print("Stock data saved to database.")
            input("Press Enter to continue...")

        elif option == "2":
            stock_data.load_stock_data(stock_list)
            print("Stock data loaded from database.")
            input("Press Enter to continue...")

        elif option == "3":
            retrieve_from_web(stock_list)

        elif option == "4":
            import_csv(stock_list)

        else: 
            print("Returning to Main Menu")



# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieve Stock Data from Web ---")
    if not stock_list:
        print("No stocks are currently being tracked right now.")
        input("Press Enter to continue...")
        return
    start_date = input("Enter start date (mm/dd/yy): ")
    end_date = input("Enter end date (mm/dd/yy): ")
    try:
        records = stock_data.retrieve_stock_web(start_date, end_date, stock_list)
        if records > 0:
            print(f'Retrieved {records} records from Yahoo! Finance.')
        else:
            print("No records found for the given date range.")
# earlier, i had gotten two types of errors when i was testing, one was an issue with chromedriver path, and the other was bad network. So, using that as exceptions here. 
    except RuntimeWarning as rw:
        print("Error: Chrome Drive not found. Check path!")
    except Exception as e:
        print("Unexpected error while retrieving data from web. Check connection and try again!", {e})

    input("Press Enter to continue...")

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import Stock Data from CSV ---")
    print()

    if not stock_list:
        print("No stocks are currently being tracked right now.")
        print("Add at least one stock before importing CSV data.")
        input("Press Enter to continue...")
        return

    print("Stock List: [", end="")
    for i, stock in enumerate(stock_list):
        if i > 0:
            print(", ", end="")
        print(stock.symbol, end="")
    print("]")

    symbol = input("Enter Stock Symbol to import data for (or 0 to cancel): ").upper()
    if symbol == "0":
        return
    
    matching_stock = None
    for s in stock_list:
        if s.symbol.upper() == symbol:
            matching_stock = s
            break

    if matching_stock is None:
        print("Stock symbol was not found!")
        input("Press Enter to continue...")
        return
    
    file_name = input("Enter the name of the csv file(include the .csv): ").strip()
    if not path.exists(file_name): # we check if the file exists or no
        print("File does not exist! Try again. ")
        input("Press Enter to continue...")
        return
    try:
        stock_data.import_stock_web_csv(stock_list, symbol, file_name)
        print(f"Imported CSV data for {symbol} from '{file_name}'.")
    except:
        print("An error has occurred! Try again. ")
    input("Press Enter to continue...")

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