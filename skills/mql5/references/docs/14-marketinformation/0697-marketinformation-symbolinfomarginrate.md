# SymbolInfoMarginRate

Returns the margin rates depending on the order type and direction.

```
bool  SymbolInfoMarginRate(
   string             name,                     // symbol name
   ENUM_ORDER_TYPE    order_type,               // order type
   double&            initial_margin_rate,      // initial margin rate
   double&            maintenance_margin_rate   // maintenance margin rate
   );

```

Parameters

name

[in] Symbol name.

order_type

[in] Order type.

initial_margin_rate

[in] A [double](/en/docs/basis/types/double) type variable for receiving an initial margin rate. Initial margin is a security deposit for 1 lot deal in the appropriate direction. Multiplying the rate by the initial margin, we receive the amount of funds to be reserved on the account when placing an order of the specified type.

maintenance_margin_rate

[out] A [double](/en/docs/basis/types/double) type variable for receiving a maintenance margin rate. Maintenance margin is a minimum amount for maintaining an open position of 1 lot in the appropriate direction. Multiplying the rate by the maintenance margin, we receive the amount of funds to be reserved on the account after an order of the specified type is activated.

Return Value

Returns true if request for properties is successful, otherwise false.

Example:

```
#define SYMBOL_NAME Symbol()
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare the variables the ratios are set into
   double initial_margin_rate = 0;     // initial margin rate
   double maintenance_margin_rate = 0; // maintenance margin rate
   
//--- get and send the SYMBOL_NAME symbol ratios for the Buy market order to the journal
   SymbolInfoMarginRatePrint(SYMBOL_NAME, ORDER_TYPE_BUY, initial_margin_rate, maintenance_margin_rate);
   
//--- get and send the SYMBOL_NAME symbol ratios for the Sell market order to the journal
   SymbolInfoMarginRatePrint(SYMBOL_NAME, ORDER_TYPE_SELL, initial_margin_rate, maintenance_margin_rate);
 
   /*
   result:
   Initial margin rate for symbol AFKS for the Buy market order: 0.225600
   Maintenance margin rate for symbol AFKS for the Buy market order: 0.112800
   Initial margin rate for symbol AFKS for the Sell market order: 0.254400
   Maintenance margin rate for symbol AFKS for the Sell market order: 0.127200   
   */
  }
//+------------------------------------------------------------------+
//| Send the margin ratios to the journal                            |
//+------------------------------------------------------------------+
void SymbolInfoMarginRatePrint(const string symbol, const ENUM_ORDER_TYPE order_type, double &initial_margin_rate, double &maintenance_margin_rate)
  {
//--- get the 'symbol' ratios for the order_type market order
   ResetLastError();
   if(!SymbolInfoMarginRate(symbol, order_type, initial_margin_rate, maintenance_margin_rate))
     {
      Print("SymbolInfoMarginRate() failed. Error ", GetLastError());
      return;
     }
//--- print the obtained ratio values
   string type=(order_type==ORDER_TYPE_BUY ? "Buy" : order_type==ORDER_TYPE_SELL ? "Sell" : "Unknown");
   PrintFormat("Initial margin rate for symbol %s for the %s market order: %f\n"+
               "Maintenance margin rate for symbol %s for the %s market order: %f",
               SYMBOL_NAME, type, initial_margin_rate,
               SYMBOL_NAME, type, maintenance_margin_rate);
  }

```
