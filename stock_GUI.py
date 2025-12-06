# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData

class StockApp:
    def __init__(self):
        self.stock_list = []
        #check for database, create if not exists
        if path.exists("stocks.db") == False:
            stock_data.create_database()

 # This section creates the user interface

        # Create Window
        self.root = Tk()
        self.root.title("MSFT Stock Manager") #Replace with a suitable name for your program


        # Add Menubar
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        # Add File Menu
        self.fileMenu = Menu(self.menubar, tearoff=0)
        self.fileMenu.add_command(label="Load Data", command=self.load)
        self.fileMenu.add_command(label="Save Data", command=self.save)

        # Add Web Menu
        self.webMenu = Menu(self.menubar, tearoff=0)
        self.webMenu.add_command(label="Get Data from Web", command=self.scrape_web_data)
        self.webMenu.add_command(label="Import CSV File", command=self.importCSV_web_data)

        # Add Chart Menu
        self.chartMenu = Menu(self.menubar, tearoff=0)
        self.chartMenu.add_command(label="Display Stock Chart", command=self.display_chart)

        # Add menus to window
        self.menubar.add_cascade(label="File", menu=self.fileMenu)
        self.menubar.add_cascade(label="Web", menu=self.webMenu)
        self.menubar.add_cascade(label="Chart", menu=self.chartMenu)

        # Add heading information
        self.headingLabel = Label(self.root, text="Stock Information", font=("Helvetica", 16))
        self.headingLabel.pack(pady=10)

        # Add stock list
        self.stockList = Listbox(self.root, height=10, width=50)
        self.stockList.pack(pady=10)
        self.stockList.bind('<<ListboxSelect>>', self.update_data)

        # Add Tabs
        self.tabControl = ttk.Notebook(self.root)
        self.tabControl.pack(pady=10)

        self.mainTab = Frame(self.tabControl)
        self.historyTab = Frame(self.tabControl)
        self.reportTab = Frame(self.tabControl)

        self.tabControl.add(self.mainTab, text="Main")
        self.tabControl.add(self.historyTab, text="History")
        self.tabControl.add(self.reportTab, text="Report")


        # Set Up Main Tab
        self.addSymbolLabel = Label(self.mainTab, text="Symbol:")
        self.addSymbolLabel.grid(row=0, column=0, padx=5, pady=5)
        self.addSymbolEntry = Entry(self.mainTab)
        self.addSymbolEntry.grid(row=0, column=1, padx=5, pady=5)
        self.addNameLabel = Label(self.mainTab, text="Name:")
        self.addNameLabel.grid(row=1, column=0, padx=5, pady=5)
        self.addNameEntry = Entry(self.mainTab)
        self.addNameEntry.grid(row=1, column=1, padx=5, pady=5)
        self.addSharesLabel = Label(self.mainTab, text="Shares:")
        self.addSharesLabel.grid(row=2, column=0, padx=5, pady=5)
        self.addSharesEntry = Entry(self.mainTab)
        self.addSharesEntry.grid(row=2, column=1, padx=5, pady=5)
        self.addStockButton = Button(self.mainTab, text="Add Stock", command=self.add_stock)
        self.addStockButton.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.updateSharesLabel = Label(self.mainTab, text="Shares to Buy/Sell:")
        self.updateSharesLabel.grid(row=4, column=0, padx=5, pady=5)
        self.updateSharesEntry = Entry(self.mainTab)
        self.updateSharesEntry.grid(row=4, column=1, padx=5, pady=5)
        self.buySharesButton = Button(self.mainTab, text="Buy Shares", command=self.buy_shares)
        self.buySharesButton.grid(row=5, column=0, padx=5, pady=5)
        self.sellSharesButton = Button(self.mainTab, text="Sell Shares", command=self.sell_shares)
        self.sellSharesButton.grid(row=5, column=1, padx=5, pady=5)
        self.deleteStockButton = Button(self.mainTab, text="Delete Stock", command=self.delete_stock)
        self.deleteStockButton.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Setup History Tab
        self.historyLabel = Label(self.historyTab, text="Daily Price and Volume Data", font=("Helvetica", 14))
        self.historyLabel.pack(pady=10)
        self.dailyDataList = Text(self.historyTab, height=15, width=60)
        self.dailyDataList.pack(pady=10)

        # Setup Report Tab

        self.reportLabel = Label(self.reportTab, text="Stock Report", font=("Helvetica", 14))
        self.reportLabel.pack(pady=10)
        self.stockReport = Text(self.reportTab, height=15, width=60)
        self.stockReport.pack(pady=10)

        ## Call MainLoop
        self.root.mainloop()

# This section provides the functionality
       
    # Load stocks and history from database.
    def load(self):
        self.stockList.delete(0,END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END,stock.symbol)
        messagebox.showinfo("Load Data","Data Loaded")

    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data","Data Saved")

    # Refresh history and report tabs
    def update_data(self, evt):
        self.display_stock_data()

    # Display stock price and volume history.
    def display_stock_data(self):
        # symbol = self.stockList.get(self.stockList.curselection())

        # added the following lines to avoid error if no selection is made because i initially got the error: _tkinter.TclError: bad listbox index "": must be active, anchor, end, @x,y, or a number between 0 and 0
        selection = self.stockList.curselection()
        if not selection:
            return
        index = selection[0]
        symbol = self.stockList.get(index)
        # end of added lines

        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                self.dailyDataList.delete("1.0",END)
                self.stockReport.delete("1.0",END)
                self.dailyDataList.insert(END,"- Date -   - Price -   - Volume -\n")
                self.dailyDataList.insert(END,"=================================\n")
                for daily_data in stock.DataList:
                    row = daily_data.date.strftime("%m/%d/%y") + "   " +  '${:0,.2f}'.format(daily_data.close) + "   " + str(daily_data.volume) + "\n"
                    self.dailyDataList.insert(END,row)

                #display report
                self.stockReport.insert(END,"Stock Report for " + stock.name + " (" + stock.symbol + ")\n")
                self.stockReport.insert(END, f"Records: {len(stock.DataList)}\n")
    # Add new stock to track.
    def add_stock(self):
        new_stock = Stock(self.addSymbolEntry.get(),self.addNameEntry.get(),float(str(self.addSharesEntry.get())))
        self.stock_list.append(new_stock)
        self.stockList.insert(END,self.addSymbolEntry.get())
        self.addSymbolEntry.delete(0,END)
        self.addNameEntry.delete(0,END)
        self.addSharesEntry.delete(0,END)

    # Buy shares of stock.
    def buy_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Buy Shares","Shares Purchased")
        self.updateSharesEntry.delete(0,END)

    # Sell shares of stock.
    def sell_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Sell Shares","Shares Sold")
        self.updateSharesEntry.delete(0,END)

    # Remove stock and all history from being tracked.
    def delete_stock(self):
       pass

    # Get data from web scraping.
    def scrape_web_data(self):
        dateFrom = simpledialog.askstring("Starting Date","Enter Starting Date (m/d/yy)")
        dateTo = simpledialog.askstring("Ending Date","Enter Ending Date (m/d/yy)")
        try:
            stock_data.retrieve_stock_web(dateFrom,dateTo,self.stock_list)
        except:
            messagebox.showerror("Cannot Get Data from Web","Check Path for Chrome Driver")
            return
        self.display_stock_data()
        messagebox.showinfo("Get Data From Web","Data Retrieved")

    # Import CSV stock history file.
    def importCSV_web_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(title="Select " + symbol + " File to Import",filetypes=[('Yahoo Finance! CSV','*.csv')])
        if filename != "":
            stock_data.import_stock_web_csv(self.stock_list,symbol,filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete",symbol + "Import Complete")   
    
    # Display stock price chart.
    def display_chart(self):
        # symbol = self.stockList.get(self.stockList.curselection())
        # same issue here. It crashes if no selection is made. So added the following lines:
        selection = self.stockList.curselection()
        if not selection:
            return
        index = selection[0]
        symbol = self.stockList.get(index)
        # end of added lines
        display_stock_chart(self.stock_list,symbol)


def main():
        app = StockApp()
        

if __name__ == "__main__":
    # execute only if run as a script
    main()