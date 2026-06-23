# Custom symbols

Functions for creating and editing the custom symbol properties.

When connecting the terminal to a certain trade server, a user is able to [work with time series](/en/docs/series) of the financial symbols provided by a broker. Available financial symbols are displayed as a list in the Market Watch window. A separate group of functions allows [receiving data on the symbol properties](/en/docs/marketinformation), trading sessions and market depth updates.

The group of functions described in this section allows creating custom symbols. To do this, users are able to apply the trade server's existing symbols, text files or external data sources.

| Function | Action |
| --- | --- |
| CustomSymbolCreate | Create a custom symbol with the specified name in the specified group |
| CustomSymbolDelete | Delete a custom symbol with the specified name |
| CustomSymbolSetInteger | Set the integer type property value for a custom symbol |
| CustomSymbolSetDouble | Set the real type property value for a custom symbol |
| CustomSymbolSetString | Set the string type property value for a custom symbol |
| CustomSymbolSetMarginRate | Set the margin rates depending on the order type and direction for a custom symbol |
| CustomSymbolSetSessionQuote | Set the start and end time of the specified quotation session for the specified symbol and week day |
| CustomSymbolSetSessionTrade | Set the start and end time of the specified trading session for the specified symbol and week day |
| CustomRatesDelete | Delete all bars from the price history of the custom symbol in the specified time interval |
| CustomRatesReplace | Fully replace the price history of the custom symbol within the specified time interval with the data from the MqlRates type array |
| CustomRatesUpdate | Add missing bars to the custom symbol history and replace existing data with the ones from the MqlRates type array |
| CustomTicksAdd | Adds data from an array of the MqlTick type to the price history of a custom symbol. The custom symbol must be selected in the Market Watch window |
| CustomTicksDelete | Delete all ticks from the price history of the custom symbol in the specified time interval |
| CustomTicksReplace | Fully replace the price history of the custom symbol within the specified time interval with the data from the MqlTick type array |
| CustomBookAdd | Passes  the status of the Depth of Market for a custom symbol |
