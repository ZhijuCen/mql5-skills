# Account Properties

To obtain information about the current account there are several functions: [AccountInfoInteger()](/en/docs/account/accountinfointeger), [AccountInfoDouble()](/en/docs/account/accountinfodouble) and [AccountInfoString()](/en/docs/account/accountinfostring). The function parameter values can accept values from the corresponding ENUM_ACCOUNT_INFO enumerations.

For the function [AccountInfoInteger()](/en/docs/account/accountinfointeger)

ENUM_ACCOUNT_INFO_INTEGER

| Identifier | Description | Type |
| --- | --- | --- |
| ACCOUNT_LOGIN | Account number | long |
| ACCOUNT_TRADE_MODE | Account trade mode | ENUM_ACCOUNT_TRADE_MODE |
| ACCOUNT_LEVERAGE | Account leverage | long |
| ACCOUNT_LIMIT_ORDERS | Maximum allowed number of active pending orders | int |
| ACCOUNT_MARGIN_SO_MODE | Mode for setting the minimal allowed margin | ENUM_ACCOUNT_STOPOUT_MODE |
| ACCOUNT_TRADE_ALLOWED | Allowed trade  for the current account | bool |
| ACCOUNT_TRADE_EXPERT | Allowed trade  for an Expert Advisor | bool |
| ACCOUNT_MARGIN_MODE | Margin calculation mode | ENUM_ACCOUNT_MARGIN_MODE |
| ACCOUNT_CURRENCY_DIGITS | The number of decimal places in the account currency, which are required for an accurate display of trading results | int |
| ACCOUNT_FIFO_CLOSE | An indication showing that positions can only be closed by FIFO rule. If the property value is set to  true , then each symbol positions will be closed in the same order, in which they are opened, starting with the oldest one. In case of an attempt to close positions in a different order, the trader will receive an appropriate error. 
   
 For accounts with the non-hedging position accounting mode ( ACCOUNT_MARGIN_MODE != ACCOUNT_MARGIN_MODE_RETAIL_HEDGING ), the property value is always  false . | bool |
| ACCOUNT_HEDGE_ALLOWED | Allowed opposite positions on a single symbol | bool |

For the function [AccountInfoDouble()](/en/docs/account/accountinfodouble)

ENUM_ACCOUNT_INFO_DOUBLE

| Identifier | Description | Type |
| --- | --- | --- |
| ACCOUNT_BALANCE | Account balance in the deposit currency | double |
| ACCOUNT_CREDIT | Account credit in the deposit currency | double |
| ACCOUNT_PROFIT | Current profit of an account in the deposit currency | double |
| ACCOUNT_EQUITY | Account equity in the deposit currency | double |
| ACCOUNT_MARGIN | Account margin used in the deposit currency | double |
| ACCOUNT_MARGIN_FREE | Free margin of an account in the deposit currency | double |
| ACCOUNT_MARGIN_LEVEL | Account margin level in percents | double |
| ACCOUNT_MARGIN_SO_CALL | Margin call level. Depending on the set ACCOUNT_MARGIN_SO_MODE is expressed in percents or in the deposit currency | double |
| ACCOUNT_MARGIN_SO_SO | Margin stop out level. Depending on the set ACCOUNT_MARGIN_SO_MODE is expressed in percents or in the deposit currency | double |
| ACCOUNT_MARGIN_INITIAL | Initial margin. The amount reserved on an account to cover the margin of all pending orders | double |
| ACCOUNT_MARGIN_MAINTENANCE | Maintenance margin. The minimum equity reserved on an account to cover the minimum amount of all open positions | double |
| ACCOUNT_ASSETS | The current assets of an account | double |
| ACCOUNT_LIABILITIES | The current liabilities on an account | double |
| ACCOUNT_COMMISSION_BLOCKED | The current blocked commission amount on an account | double |

For function [AccountInfoString()](/en/docs/account/accountinfostring)

ENUM_ACCOUNT_INFO_STRING

| Identifier | Description | Type |
| --- | --- | --- |
| ACCOUNT_NAME | Client name | string |
| ACCOUNT_SERVER | Trade server name | string |
| ACCOUNT_CURRENCY | Account currency | string |
| ACCOUNT_COMPANY | Name of a company that serves the account | string |

There are several types of accounts that can be opened on a trade server. The type of account on which an MQL5 program is running can be found out using the ENUM_ACCOUNT_TRADE_MODE enumeration.

ENUM_ACCOUNT_TRADE_MODE

| Identifier | Description |
| --- | --- |
| ACCOUNT_TRADE_MODE_DEMO | Demo account |
| ACCOUNT_TRADE_MODE_CONTEST | Contest account |
| ACCOUNT_TRADE_MODE_REAL | Real account |

In case equity is not enough for maintaining open positions, the Stop Out situation, i.e. forced closing occurs. The minimum margin level at which Stop Out occurs can be set in percentage or in monetary terms. To find out the mode set for the account use the ENUM_ACCOUNT_STOPOUT_MODE enumeration.

ENUM_ACCOUNT_STOPOUT_MODE

| Identifier | Description |
| --- | --- |
| ACCOUNT_STOPOUT_MODE_PERCENT | Account stop out mode in percents |
| ACCOUNT_STOPOUT_MODE_MONEY | Account stop out mode in money |

ENUM_ACCOUNT_MARGIN_MODE

| Identifier | Description |
| --- | --- |
| ACCOUNT_MARGIN_MODE_RETAIL_NETTING | Used for the OTC markets to interpret positions in the "netting" mode (only one position can exist for one symbol). The margin is calculated based on the symbol type ( SYMBOL_TRADE_CALC_MODE ). |
| ACCOUNT_MARGIN_MODE_EXCHANGE | Used for the exchange markets. Margin is calculated based on the discounts specified in symbol settings. Discounts are set by the broker, but not less than the values set by the exchange. |
| ACCOUNT_MARGIN_MODE_RETAIL_HEDGING | Used for the exchange markets where individual positions are possible (hedging, multiple positions can exist for one symbol). The margin is calculated based on the symbol type ( SYMBOL_TRADE_CALC_MODE ) taking into account the hedged margin ( SYMBOL_MARGIN_HEDGED ). |

An example of the script that outputs a brief account information.

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- Name of the company
   string company=AccountInfoString(ACCOUNT_COMPANY);
//--- Name of the client
   string name=AccountInfoString(ACCOUNT_NAME);
//--- Account number
   long login=AccountInfoInteger(ACCOUNT_LOGIN);
//--- Name of the server
   string server=AccountInfoString(ACCOUNT_SERVER);
//--- Account currency
   string currency=AccountInfoString(ACCOUNT_CURRENCY);
//--- Demo, contest or real account
   ENUM_ACCOUNT_TRADE_MODE account_type=(ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE);
//--- Now transform the value of  the enumeration into an understandable form
   string trade_mode;
   switch(account_type)
     {
      case  ACCOUNT_TRADE_MODE_DEMO:
         trade_mode="demo";
         break;
      case  ACCOUNT_TRADE_MODE_CONTEST:
         trade_mode="contest";
         break;
      default:
         trade_mode="real";
         break;
     }
//--- Stop Out is set in percentage or money
   ENUM_ACCOUNT_STOPOUT_MODE stop_out_mode=(ENUM_ACCOUNT_STOPOUT_MODE)AccountInfoInteger(ACCOUNT_MARGIN_SO_MODE);
//--- Get the value of the levels when Margin Call and Stop Out occur
   double margin_call=AccountInfoDouble(ACCOUNT_MARGIN_SO_CALL);
   double stop_out=AccountInfoDouble(ACCOUNT_MARGIN_SO_SO);
//--- Show brief account information
   PrintFormat("The account of the client '%s' #%d %s opened in '%s' on the server '%s'",
               name,login,trade_mode,company,server);
   PrintFormat("Account currency - %s, MarginCall and StopOut levels are set in %s",
               currency,(stop_out_mode==ACCOUNT_STOPOUT_MODE_PERCENT)?"percentage":" money");
   PrintFormat("MarginCall=%G, StopOut=%G",margin_call,stop_out);
  }

```
