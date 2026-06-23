# Restrictions and permissions for account operations

Among the properties of the account, there are restrictions on trading operations, including completely disabled trading. All of these properties belong to the ENUM_ACCOUNT_INFO_INTEGER enumeration and are boolean flags, except ACCOUNT_LIMIT_ORDERS.

| Identifier | Description |
| --- | --- |
| ACCOUNT_TRADE_ALLOWED | Permission to trade on a current account |
| ACCOUNT_TRADE_EXPERT | Permission for algorithmic trading using Expert Advisors and scripts |
| ACCOUNT_LIMIT_ORDERS | Maximum allowed number of valid pending orders |
| ACCOUNT_FIFO_CLOSE | Requirement to close positions only according to the FIFO rule |

Since our book is about MQL5 programming, which includes algorithmic trading, it should be noted that the disabled ACCOUNT_TRADE_EXPERT permission is just as critical as the general prohibition to trade when ACCOUNT_TRADE_ALLOWED is equal to false. The broker has the ability to prohibit trading using Expert Advisors and scripts while allowing manual trading.

The ACCOUNT_TRADE_ALLOWED property is usually equal to false if the connection to the account was made using the investment password.

If the value of the ACCOUNT_FIFO_CLOSE property is true, positions for each symbol can only be closed in the same order in which they were opened, that is, first you close the oldest order, then the newer one, and so on until the last one. If you try to close positions in a different order, you will receive an error. For accounts without position hedging, that is, if the ACCOUNT_MARGIN_MODE property is not equal to ACCOUNT_MARGIN_MODE_RETAIL_HEDGING, the ACCOUNT_FIFO_CLOSE property is always false.

In the [Permissions](/en/book/common/environment/env_permissions) and [Schedules of trading and quoting sessions](/en/book/automation/symbols/symbols_sessions) sections, we have already started developing a class for detecting trade operations available to the MQL program. Now we can supplement it with account permission checks and bring it to the final version (Permissions.mqh).

Restriction levels are provided in the TRADE_RESTRICTIONS enumeration, which, after adding two new elements related to account properties, takes the following form.

```
class Permissions
{
   enum TRADE_RESTRICTIONS
   {
      NO_RESTRICTIONS = 0,
      TERMINAL_RESTRICTION = 1, // user's restriction for all programs
      PROGRAM_RESTRICTION = 2,  // user's restriction for a specific program
      SYMBOL_RESTRICTION = 4,   // the symbol is not traded according to the specification
      SESSION_RESTRICTION = 8,  // the market is closed according to the session schedule
      ACCOUNT_RESTRICTION = 16, // investor password or broker restriction
      EXPERTS_RESTRICTION = 32, // broker restricted algorithmic trading
   };
   ...

```

During the check, the MQL program may detect several restrictions for various reasons, and therefore the elements are encoded by separate bits. The final result can represent their superposition.

The last two restrictions just correspond to the new properties and are set in the getTradeRestrictionsOnAccount method. The general bitmask of detected restrictions (if any) is formed in the lastRestrictionBitMask variable.

```
private:
   static uint lastRestrictionBitMask;
   static bool pass(const uint bitflag) 
   {
      lastRestrictionBitMask |= bitflag;
      return lastRestrictionBitMask == 0;
   }
   
public:
   static uint getTradeRestrictionsOnAccount()
   {
      return (AccountInfoInteger(ACCOUNT_TRADE_ALLOWED) ? 0 : ACCOUNT_RESTRICTION)
         | (AccountInfoInteger(ACCOUNT_TRADE_EXPERT) ? 0 : EXPERTS_RESTRICTION);
   }
   
   static bool isTradeOnAccountEnabled()
   {
      lastRestrictionBitMask = 0;
      return pass(getTradeRestrictionsOnAccount());
   }
   ... 

```

If the calling code is not interested in the reason for restriction but only needs to determine the possibility of performing trading operations, it is more convenient to use the isTradeOnAccountEnabled method which returns a boolean sign (true/false).

Checks of symbol and terminal properties have been reorganized according to a similar principle. For example, the getTradeRestrictionsOnSymbol method contains the source code already familiar from the previous version of the class (checking the symbol's trading sessions and trading modes) but returns a flags mask. If at least one bit is set, it describes the source of the restriction.

```
   static uint getTradeRestrictionsOnSymbol(const string symbol, datetime now = 0,
      const ENUM_SYMBOL_TRADE_MODE mode = SYMBOL_TRADE_MODE_FULL)
   {
      if(now == 0) now = TimeTradeServer();
      bool found = false;
      // checking the symbol trading sessions and setting 'found' to 'true',
      // if the 'now' time is inside one of the sessions
      ...
      
      // in addition to sessions, check the trading mode
      const ENUM_SYMBOL_TRADE_MODE m = (ENUM_SYMBOL_TRADE_MODE)SymbolInfoInteger(symbol, SYMBOL_TRADE_MODE);
      return (found ? 0 : SESSION_RESTRICTION)
         | (((m & mode) != 0) || (m == SYMBOL_TRADE_MODE_FULL) ? 0 : SYMBOL_RESTRICTION);
   }
   
   static bool isTradeOnSymbolEnabled(const string symbol, const datetime now = 0,
      const ENUM_SYMBOL_TRADE_MODE mode = SYMBOL_TRADE_MODE_FULL)
   {
      lastRestrictionBitMask = 0;
      return pass(getTradeRestrictionsOnSymbol(symbol, now, mode));
   }
   ...

```

Finally, a general check of all potential "instances", including (in addition to the previous levels) the settings of the terminal and the program, is performed in the getTradeRestrictions and isTradeEnabled methods.

```
   static uint getTradeRestrictions(const string symbol = NULL, const datetime now = 0,
      const ENUM_SYMBOL_TRADE_MODE mode = SYMBOL_TRADE_MODE_FULL)
   {
      return (TerminalInfoInteger(TERMINAL_TRADE_ALLOWED) ? 0 : TERMINAL_RESTRICTION)
          | (MQLInfoInteger(MQL_TRADE_ALLOWED) ? 0 : PROGRAM_RESTRICTION)
          | getTradeRestrictionsOnSymbol(symbol == NULL ? _Symbol : symbol, now, mode)
          | getTradeRestrictionsOnAccount();
   }
   
   static bool isTradeEnabled(const string symbol = NULL, const datetime now = 0,
      const ENUM_SYMBOL_TRADE_MODE mode = SYMBOL_TRADE_MODE_FULL)
   {
      lastRestrictionBitMask = 0;
      return pass(getTradeRestrictions(symbol, now, mode));
   }

```

A comprehensive check of trade permissions with a new class is demonstrated by the script AccountPermissions.mq5.

```
#include <MQL5Book/Permissions.mqh>
   
void OnStart()
{
   PrintFormat("Run on %s", _Symbol);
   if(!Permissions::isTradeEnabled()) // checking for current character, default
   {
      Print("Trade is disabled for the following reasons:");
      Print(Permissions::explainLastRestrictionBitMask());
   }
   else
   {
      Print("Trade is enabled");
   }
}

```

If restrictions are found, their bit mask can be displayed in a clear string representation using the explainLastRestrictionBitMask method.

Here are some script results. In the first two cases, trading was disabled in the global settings of the terminal (properties TERMINAL_TRADE_ALLOWED and MQL_TRADE_ALLOWED were equal to false, which corresponds to the TERMINAL_RESTRICTION and PROGRAM_RESTRICTION bits).

When run on USDRUB during the hours when the market is closed, we will additionally receive SESSION_RESTRICTION:

```
Trade is disabled for USDRUB following reasons:
TERMINAL_RESTRICTION PROGRAM_RESTRICTION SESSION_RESTRICTION 

```

For the symbol SP500m, for which trading is totally disabled, the SYMBOL_RESTRICTION flag appears.

```
Trade is disabled for SP500m following reasons:
TERMINAL_RESTRICTION PROGRAM_RESTRICTION SYMBOL_RESTRICTION SESSION_RESTRICTION 

```

Finally, having allowed trading in the terminal but having logged into the account under the investor's password, we will see ACCOUNT_RESTRICTION on any symbol.

```
Run on XAUUSD
Trade is disabled for following reasons:
ACCOUNT_RESTRICTION 

```

Early check of permissions in the MQL program helps avoid serial unsuccessful attempts to send trading orders.
