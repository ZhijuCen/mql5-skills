# Account type: netting or hedging

MetaTrader 5 supports several types of accounts, in particular, [netting and hedging](https://www.metatrader5.com/en/terminal/help/trading/general_concept#position_type). For netting, it is allowed to have only one [position](/en/book/automation/experts/experts_order_deal_position) for each symbol. For hedging, you can open several positions for a symbol, including multidirectional ones. Orders, trades, and positions will be discussed in detail in the following chapters.

An MQL program determines the account type by querying the ACCOUNT_MARGIN_MODE property using the AccountInfoInteger function. As you can understand from the name of the property, it describes not only the account type but also the margin calculation mode. Its possible values are specified in the ENUM_ACCOUNT_MARGIN_MODE enumeration.

| Identifier | Description |
| --- | --- |
| ACCOUNT_MARGIN_MODE_RETAIL_NETTING | OTC market, considering positions in the netting mode. Margin calculation is based on the  SYMBOL_TRADE_CALC_MODE  property. |
| ACCOUNT_MARGIN_MODE_EXCHANGE | Exchange market, considering positions in the netting mode. The margin is calculated based on the rules of the exchange with the possibility of discounts specified by the broker in the instrument settings. |
| ACCOUNT_MARGIN_MODE_RETAIL_HEDGING | OTC market with independent consideration of positions in the hedging mode. Margin calculation is based on the  SYMBOL_TRADE_CALC_MODE  symbol property while considering the size of the hedged margin  SYMBOL_MARGIN_HEDGED . |

For example, running the AccountInfo script in the section [Account identification](/en/book/automation/account/account_number_identity) showed that the account is of type ACCOUNT_MARGIN_MODE_RETAIL_HEDGING.
