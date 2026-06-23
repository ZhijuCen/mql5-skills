# Copying timeseries to matrices and vectors

The matrix<T>::CopyRates method copies timeseries with the quoting history directly into a matrix or vector. This method works similarly to the functions which we will cover in detail in Part 5, in the chapter on [timeseries](/en/book/applications/timeseries), namely: [CopyRates](/en/book/applications/timeseries/timeseries_mqlrates) and separate [Copy functions](/en/book/applications/timeseries/timeseries_copy_funcs_overview) for each field of the [MqlRates](/en/book/applications/timeseries/timeseries_mqlrates) structure.

bool matrix<T>::CopyRates(const string symbol, ENUM_TIMEFRAMES tf, ulong rates_mask,  

   ulong start, ulong count)

bool matrix<T>::CopyRates(const string symbol, ENUM_TIMEFRAMES tf, ulong rates_mask,  

   datetime from, ulong count)

bool matrix<T>::CopyRates(const string symbol, ENUM_TIMEFRAMES tf, ulong rates_mask,  

   datetime from, datetime to)

In the parameters, you need to specify the symbol, timeframe, and the range of requested bars: either by number and quantity, or by date range. The data is copied so that the oldest element is placed at the beginning of the matrix/vector.

The rates_mask parameter specifies a combination of flags from the ENUM_COPY_RATES enumeration with a set of available fields. The combination of flags allows you to get several timeseries from history in one request. In this case, the order of rows in the matrix will correspond to the order of values in the ENUM_COPY_RATES enumeration, in particular, the row with High data in the matrix will always be above the row with Low data.

When copying to a vector, only one value from the ENUM_COPY_RATES enumeration can be specified. Otherwise, an error will occur.

| Identifier | Value | Description |
| --- | --- | --- |
| COPY_RATES_OPEN | 1 | Open  prices |
| COPY_RATES_HIGH | 2 | High  prices |
| COPY_RATES_LOW | 4 | Low  prices |
| COPY_RATES_CLOSE | 8 | Close  prices |
| COPY_RATES_TIME | 16 | Bar opening times |
| COPY_RATES_VOLUME_TICK | 32 | Tick volumes |
| COPY_RATES_VOLUME_REAL | 64 | Real volumes |
| COPY_RATES_SPREAD | 128 | Spreads |
|  | Combinations |  |
| COPY_RATES_OHLC | 15 | Open, High, Low, Close |
| COPY_RATES_OHLCT | 31 | Open, High, Low, Close, Time |

We will view an example of using this function in the [Solving equations](/en/book/common/matrices/matrices_sle) section.
