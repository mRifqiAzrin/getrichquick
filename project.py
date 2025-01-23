import requests
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')

# Function to get historical stock prices from FMP API
def get_historical_data(ticker, start_date, end_date):
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?from={start_date}&to={end_date}&apikey={API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'historical' in data:
            return data['historical']
        else:
            print(f"Error: No data for {ticker}")
            return []
    else:
        print("Error fetching historical data.")
        return []

# Function to verify sentiment with actual stock movement
def verify_sentiment_with_price(stocks, start_date, end_date):
    verification_results = []
    for stock in stocks:
        ticker = stock['ticker']
        sentiment = stock['sentiment']
        
        # Get historical data for the stock
        historical_data = get_historical_data(ticker, start_date, end_date)
        
        if not historical_data:
            continue
        
        # Get the opening price on the first day and closing price on the last day
        start_price = historical_data[0]['open']
        end_price = historical_data[-1]['close']
        
        # Compare sentiment with price movement
        correct_prediction = False
        if sentiment == 'Bullish' and end_price > start_price:
            correct_prediction = True
        elif sentiment == 'Bearish' and end_price < start_price:
            correct_prediction = True
        
        verification_results.append((ticker, sentiment, correct_prediction, start_price, end_price))
    return verification_results

# Visualize the stocks with sentiment verification
def visualize(stocks, start_date, end_date):
    # Verify the sentiment with actual price data
    verification_results = verify_sentiment_with_price(stocks, start_date, end_date)
    
    # Categorize stocks into Bullish and Bearish
    bullish_stocks = [stock for stock in verification_results if stock[1] == 'Bullish']
    bearish_stocks = [stock for stock in verification_results if stock[1] == 'Bearish']

    # Extracting tickers, no_of_comments, and verification results
    bullish_tickers = [stock[0] for stock in bullish_stocks]
    bullish_comments = [stock[3] for stock in bullish_stocks]  # Using start price as comments for illustration
    bullish_correct = [stock[2] for stock in bullish_stocks]  # Correct prediction (True/False)
    
    bearish_tickers = [stock[0] for stock in bearish_stocks]
    bearish_comments = [stock[3] for stock in bearish_stocks]  # Using start price as comments for illustration
    bearish_correct = [stock[2] for stock in bearish_stocks]  # Correct prediction (True/False)

    # Create subplots to plot Bullish and Bearish separately
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotting Bullish stocks
    ax.bar(bullish_tickers, bullish_comments, color='green', label='Bullish')

    # Plotting Bearish stocks
    ax.bar(bearish_tickers, bearish_comments, color='red', label='Bearish')

    # Title and labels
    ax.set_title('Number of Comments by Stock Ticker (Bullish vs Bearish)')
    ax.set_xlabel('Stock Ticker')
    ax.set_ylabel('Number of Comments')

    # Rotate x-axis labels for readability
    plt.xticks(rotation=45)

    # Add a legend
    ax.legend()

    # Add annotations for sentiment verification
    for i, ticker in enumerate(bullish_tickers):
        color = 'green' if bullish_correct[i] else 'red'
        ax.text(i, bullish_comments[i] + 0.2, 'Correct' if bullish_correct[i] else 'Incorrect', ha='center', color=color)
    
    for i, ticker in enumerate(bearish_tickers):
        color = 'green' if bearish_correct[i] else 'red'
        ax.text(i + len(bullish_tickers), bearish_comments[i] + 0.2, 'Correct' if bearish_correct[i] else 'Incorrect', ha='center', color=color)

    # Show the plot
    plt.show()

def WSB(date):
    url = 'https://tradestie.com/api/v1/apps/reddit?date={}'.format(str(date))
    response = requests.get(url)

    if response.status_code == 200:
        WSB_data = response.json()
        return WSB_data
    else:
        print("Error.")
        return False

def TTMS(date):
    url = 'https://tradestie.com/api/v1/apps/ttm-squeeze-stocks?date={}'.format(str(date))
    response = requests.get(url)

    if response.status_code == 200:
        TTMS_data = response.json()
        return TTMS_data
    else:
        print("Error.")
        return False

def overlap(WSB, TTMS):
    WSB_Tickers = []
    TTMS_Tickers = []
    
    for ticker in WSB:
        tickers = ticker['ticker']
        WSB_Tickers.append(tickers)

    for ticker in TTMS:
        tickers = ticker['ticker']
        TTMS_Tickers.append(tickers)

    overlapping_tickers = list(set(WSB_Tickers) & set(TTMS_Tickers))
    Overlap = [stock for stock in WSB if stock['ticker'] in overlapping_tickers]

    return Overlap

def process_date_input():
    start_date = entry_start_date.get()
    end_date = entry_end_date.get()

    try:
        # Check if the user has entered a range of dates or a single date
        if start_date and end_date:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

            # Loop through the date range and collect data for each date
            all_overlapping_stocks = []
            current_date = start_date_obj
            while current_date <= end_date_obj:
                WSB_data = WSB(current_date)
                TTMS_data = TTMS(current_date)
                if WSB_data and TTMS_data:
                    overlaps = overlap(WSB_data, TTMS_data)
                    all_overlapping_stocks.extend(overlaps)
                current_date += timedelta(days=1)

            visualize(all_overlapping_stocks, start_date, end_date)

        elif start_date:
            date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            WSB_data = WSB(date_obj)
            TTMS_data = TTMS(date_obj)
            if WSB_data and TTMS_data:
                overlaps = overlap(WSB_data, TTMS_data)
                visualize(overlaps, start_date, start_date)
            else:
                messagebox.showinfo("Error", "No data found for the given date.")

        else:
            messagebox.showinfo("Error", "Please enter a date or date range.")

    except ValueError:
        messagebox.showinfo("Invalid Input", "Please enter the dates in the format YYYY-MM-DD.")

# Create the GUI
root = tk.Tk()
root.title("Stock Sentiment Visualizer")

# Labels and entry widgets for date input
label_start_date = tk.Label(root, text="Start Date (YYYY-MM-DD):")
label_start_date.grid(row=0, column=0, padx=10, pady=10)

entry_start_date = tk.Entry(root)
entry_start_date.grid(row=0, column=1, padx=10, pady=10)

label_end_date = tk.Label(root, text="End Date (YYYY-MM-DD):")
label_end_date.grid(row=1, column=0, padx=10, pady=10)

entry_end_date = tk.Entry(root)
entry_end_date.grid(row=1, column=1, padx=10, pady=10)

# Submit button to process input
submit_button = tk.Button(root, text="Generate Graph", command=process_date_input)
submit_button.grid(row=2, column=0, columnspan=2, pady=20)

# Run the GUI
root.mainloop()
