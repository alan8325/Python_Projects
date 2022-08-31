import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from bs4 import BeautifulSoup as BS
import requests
import re

#Fixing blurry UI on Windows
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)


root = tk.Tk()
root.title('Sats to Dollars Converter')
root.geometry('460x150-50+50')
root.iconbitmap('C:/Users/alan8/Python_Projects/Bitcoin Tools/bitcoin-icon.ico')

#frame
frame = ttk.Frame(root)

options = {'padx': 5, 'pady': 5}

def sats_to_dollars(s):   
    """ Convert satoshis to US dollars
    """

    return float(s / 100000000) * BTCPrice

def get_float_in_string(s):
    """Get floating point number from a string that contains a single floating point number
    """
    s=s.replace(',', '')
    temp = re.findall(r'[-+]?(?:\d*\.\d+|\d+)', s)
    return float(temp[0])


def convert_button_clicked(event=None):
    """  Handle convert button click event 
    """

    try:
        s = float(sats.get())
        d = sats_to_dollars(s)
        result = f'{s} Satoshis = ${d:.2f}'
        result_label.config(text=result)
    except ValueError as error:
        showerror(title='Error', message=error)

def get_price(url):
    """  Fetch BTC price
    """
    data = requests.get(url)

    soup = BS(data.text, 'html.parser')

    div = soup.find("div", class_ ="BNeawe iBp4i AP7Wnd").text
    
    divfloat = get_float_in_string(div)
    
    return(divfloat)

url = "https://www.google.com/search?q=bitcoin+price"

BTCPrice = get_price(url)

#BTC Price label
price_label = ttk.Label(frame, text='BTC Price: ')
price_label.grid(column=0, row=0, sticky='W', **options)

#BTC Price Value
price_label = ttk.Label(frame, text='$'+str(BTCPrice))
price_label.grid(column=1, row=0, sticky='W', **options)

#Satoshis label
sats_label = ttk.Label(frame, text='Satoshis')
sats_label.grid(column=0, row=1, sticky='W', **options)

#Satoshis entry
sats = tk.StringVar()
sats_entry = ttk.Entry(frame, textvariable=sats)
sats_entry.grid(column=1, row=1, **options)
sats_entry.focus()

#Convert button
convert_button = ttk.Button(frame, text='Convert')
convert_button.grid(column=2, row=1, sticky='W', **options)
convert_button.configure(command = convert_button_clicked)
root.bind('<Return>', convert_button_clicked)

#Result label
result_label = ttk.Label(frame)
result_label.grid(row=2, columnspan=3, **options)


#add padding to the frame and show it
frame.grid(padx=10, pady=10)

root.mainloop()

