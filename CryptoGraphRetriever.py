import tkinter as tk
import webbrowser

from pycoingecko import CoinGeckoAPI # using CoinGeckoAPI to retrieve live data
import pandas as pd
import plotly.graph_objs as go # For candle PLot


cg = CoinGeckoAPI() # creating object


def create_and_check(cryptoname,currency,numberofdays):

    try:
        #cryptoname,currency,numberofdays = input_data()
        cryptoData = cg.get_coin_market_chart_by_id(id = cryptoname, vs_currency = currency, days = numberofdays)
    except ValueError as v:
            if ('invalid literal' in str(v)):
                error_msg = 'Please Enter Valid NO of days'
                error_text.insert(tk.END, error_msg + '\n')
                error_text.see(tk.END)  # Scroll to the end of the text widget
            elif ('coin not found' in str(v)):
                error_msg = 'Please Enter Valid name of Crypto-Currency'
                error_text.insert(tk.END, error_msg + '\n')
                error_text.see(tk.END) 
            elif ("invalid vs_currency" in str(v)):
                error_msg = 'Please Enter Valid Currency in correct Format'
                error_text.insert(tk.END, error_msg + '\n')
                error_text.see(tk.END)
            else:
                error_msg = 'The Error is :'
                error_msg = str(v)
            error_msg = ('Please Try Again \n')
            error_text.insert(tk.END, error_msg + '\n')
            error_text.see(tk.END)
            # Display the error message in the text widget
            
            #cryptoData = None
    return cryptoData





def Graph_Data_create(cryptoData):
    Data = pd.DataFrame(cryptoData['prices'], columns = ['Time', 'Price'])
    Data['Price'] = Data['Price'].apply(lambda x: round(x,2))
    Data['Time'] = pd.to_datetime(Data['Time'],unit='ms')
    Candlestick_data = Data.groupby(Data.Time.dt.date).agg({'Price': ['min',
                                                                  'max',
                                                                  'first',
                                                                  'last']}
                                                      )
    return Candlestick_data





def saveplot(Candlestick_data,cryptoname,currency):
    fig = go.Figure(data = [go.Candlestick(x = Candlestick_data.index,
                                                   open = Candlestick_data['Price']['first'],
                                                   high = Candlestick_data['Price']['max'],
                                                   low = Candlestick_data['Price']['min'],
                                                   close = Candlestick_data['Price']['last']
                                                   )
                                    ])
    fig.update_layout(xaxis_title = 'Date', yaxis_title='Price in '+ currency ,title = 'Prices of '+ cryptoname,height = 800)
    fig.write_html('crypto_graph.html')
    print("Crypto graph retrieved successfully")



def retrieve_and_display():
    # Retrieve input values from entry widgets
    cryptoname = crypto_entry.get().lower()
    currency = currency_entry.get().lower()
    try:
        numberofdays = int(days_entry.get())
    except ValueError as v:
        if ('invalid literal' in str(v)):
                error_msg = 'Please Enter Valid NO of days'
                error_text.insert(tk.END, error_msg + '\n')
                error_text.see(tk.END)
                error_msg = ('Please Try Again \n')
                error_text.insert(tk.END, error_msg + '\n')
                error_text.see(tk.END)

    cryptoData = create_and_check(cryptoname,currency,numberofdays)

    Candlestick_data = Graph_Data_create(cryptoData)
    saveplot(Candlestick_data,cryptoname,currency)

    # Open the saved Plotly JavaScript file in the default web browser
    webbrowser.open("crypto_graph.html")



'''
--------------------------------------------------------------------------
                GUI
--------------------------------------------------------------------------
'''


# main application window
root = tk.Tk()
root.title("Crypto Graph Retriever")




# Create input fields for 
# crypto name
tk.Label(root, text="Crypto Name:").pack()
crypto_entry = tk.Entry(root)
crypto_entry.pack()

# currency
tk.Label(root, text="Currency(PLease enter acronyms) :").pack()
currency_entry = tk.Entry(root)
currency_entry.pack()

# number of days
tk.Label(root, text="Number of Days:").pack()
days_entry = tk.Entry(root)
days_entry.pack()



# Create a button to retrieve and display the graph
retrieve_button = tk.Button(root, text="Retrieve Crypto Graph", command=retrieve_and_display)
retrieve_button.pack(pady=10)


error_text = tk.Text(root, height=5, width=50)
error_text.pack()

# Run the application
root.mainloop()
