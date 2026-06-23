# Subscribing to order book changes

The Python API includes three functions for working with the [order book](/en/book/automation/marketbook).

bool market_book_add(symbol)

The market_book_add function subscribes to receive events about order book changes for the specified symbol. The name of the required financial instrument is indicated in a single unnamed parameter.

The function returns a boolean success indication.

The function is an analog of [MarketBookAdd](/en/book/automation/marketbook/marketbook_add_release). After completing work with the order book, the subscription should be canceled by calling market_book_release (see further).

tuple[] market_book_get(symbol)

The market_book_get function requests the current contents of the order book for the specified symbol. The result is returned as a tuple (array) of BookInfo records. Each entry is an analog of the MqlBookInfo structure, and from the Python point of view, this is a named tuple with the fields "type", "price", "volume", "volume_real". In case of an error, the None value is returned.

Note that for some reason in Python, the field is called volume_dbl, although in MQL5 the corresponding field is called volume_real.

To work with this function, you must first subscribe to receive order book events using the market_book_add function.

The function is an analog of [MarketBookGet](/en/book/automation/marketbook/marketbook_get). Please note that a Python script cannot receive OnBookEvent events directly and should poll the contents of the glass in a loop.

bool market_book_release(symbol)

The market_book_release function cancels the subscription for order book change events for the specified symbol. On success, the function returns True. The function is an analog of [MarketBookRelease](/en/book/automation/marketbook/marketbook_add_release).

Let's take a simple example (see MQL5/Scripts/MQL5Book/Python/eurusdbook.py).

```
import MetaTrader5 as mt5
import time               # connect a pack for the pause
   
# let's establish a connection to the MetaTrader 5 terminal
if not mt5.initialize():
   print("initialize() failed, error code =", mt5.last_error())
   mt5.shutdown()
   quit()
   
# subscribe to receive DOM updates for the EURUSD symbol
if mt5.market_book_add('EURUSD'):
   # run 10 times a loop to read data from the order book
   for i in range(10):
      # get the contents of the order book
      items = mt5.market_book_get('EURUSD')
      # display the entire order book in one line as is
      print(items)
      # now display each price level separately in the form of a dictionary, for clarity
      for it in items or []:
         print(it._asdict())
      # let's pause for 5 seconds before the next request for data from the order book
      time.sleep(5) 
   # unsubscribe to order book changes
   mt5.market_book_release('EURUSD')
else:
   print("mt5.market_book_add('EURUSD') failed, error code =", mt5.last_error())
   
# complete the connection to the MetaTrader 5 terminal
mt5.shutdown()

```

An example of the result:

```
(BookInfo(type=1, price=1.20036, volume=250, volume_dbl=250.0), BookInfo(type=1, price=1.20029, volume=100, volume...
{'type': 1, 'price': 1.20036, 'volume': 250, 'volume_dbl': 250.0}
{'type': 1, 'price': 1.20029, 'volume': 100, 'volume_dbl': 100.0}
{'type': 1, 'price': 1.20028, 'volume': 50, 'volume_dbl': 50.0}
{'type': 1, 'price': 1.20026, 'volume': 36, 'volume_dbl': 36.0}
{'type': 2, 'price': 1.20023, 'volume': 36, 'volume_dbl': 36.0}
{'type': 2, 'price': 1.20022, 'volume': 50, 'volume_dbl': 50.0}
{'type': 2, 'price': 1.20021, 'volume': 100, 'volume_dbl': 100.0}
{'type': 2, 'price': 1.20014, 'volume': 250, 'volume_dbl': 250.0}
(BookInfo(type=1, price=1.20035, volume=250, volume_dbl=250.0), BookInfo(type=1, price=1.20029, volume=100, volume...
{'type': 1, 'price': 1.20035, 'volume': 250, 'volume_dbl': 250.0}
{'type': 1, 'price': 1.20029, 'volume': 100, 'volume_dbl': 100.0}
{'type': 1, 'price': 1.20027, 'volume': 50, 'volume_dbl': 50.0}
{'type': 1, 'price': 1.20025, 'volume': 36, 'volume_dbl': 36.0}
{'type': 2, 'price': 1.20023, 'volume': 36, 'volume_dbl': 36.0}
{'type': 2, 'price': 1.20022, 'volume': 50, 'volume_dbl': 50.0}
{'type': 2, 'price': 1.20021, 'volume': 100, 'volume_dbl': 100.0}
{'type': 2, 'price': 1.20014, 'volume': 250, 'volume_dbl': 250.0}
(BookInfo(type=1, price=1.20037, volume=250, volume_dbl=250.0), BookInfo(type=1, price=1.20031, volume=100, volume...
{'type': 1, 'price': 1.20037, 'volume': 250, 'volume_dbl': 250.0}
{'type': 1, 'price': 1.20031, 'volume': 100, 'volume_dbl': 100.0}
{'type': 1, 'price': 1.2003, 'volume': 50, 'volume_dbl': 50.0}
{'type': 1, 'price': 1.20028, 'volume': 36, 'volume_dbl': 36.0}
{'type': 2, 'price': 1.20025, 'volume': 36, 'volume_dbl': 36.0}
{'type': 2, 'price': 1.20023, 'volume': 50, 'volume_dbl': 50.0}
{'type': 2, 'price': 1.20022, 'volume': 100, 'volume_dbl': 100.0}
{'type': 2, 'price': 1.20016, 'volume': 250, 'volume_dbl': 250.0}
...

```
