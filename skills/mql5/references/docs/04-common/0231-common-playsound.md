# PlaySound

It plays a sound file.

```
bool  PlaySound(
   string  filename      // file name
   );

```

Parameters

filename

[in]  Path to a sound file. If filename=NULL, the playback is stopped.

Return Value

true – if the file is found, otherwise - false.

Note

The file must be located in terminal_directory\Sounds or its sub-directory. Only WAV files are played.

Call of PlaySound() with NULL parameter stops playback.

PlaySound() function does not work in the [Strategy Tester](/en/docs/runtime/testing#alert_etc).

Example:

```
#include <Trade\Trade.mqh>
#define MAGIC (123)
 
//--- input parameters
input string          InpFileNameOK  = "ok.wav";               // success audio file
input string          InpFileNameErr = "timeout.wav";          // error audio file
input ENUM_ORDER_TYPE InpOrderType   = ORDER_TYPE_BUY_LIMIT;   // order type
input double          InpLots        = 0.1;                    // lots
 
//--- global variables
CTrade ExtTrade;
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- set the magic and order type by execution according to the symbol settings
   ExtTrade.SetExpertMagicNumber(MAGIC);
   ExtTrade.SetTypeFillingBySymbol(Symbol());
//--- call the function of placing an order or opening a position with sound playback
   OrderSendWithAudio();
  }
//+------------------------------------------------------------------+
//| The function places an order or opens a position                 |
//| and plays the sound of success or error                          |
//+------------------------------------------------------------------+
void OrderSendWithAudio(void)
  {
   bool    res=true;
   MqlTick tick= {};
 
   ResetLastError();
   if(!SymbolInfoTick(Symbol(),tick))
     {
      Print("SymbolInfoTick() failed. Error code: ",GetLastError());
      PlaySound(InpFileNameErr);
      return;
     }
//--- send a request to the server
   switch(InpOrderType)
     {
      case ORDER_TYPE_BUY :
         res=ExtTrade.Buy(InpLots);
         break;
      case ORDER_TYPE_BUY_LIMIT :
         res=ExtTrade.BuyLimit(InpLots,NormalizeDouble(tick.ask-100*Point(),Digits()));
         break;
      case ORDER_TYPE_BUY_STOP :
         res=ExtTrade.BuyStop(InpLots,NormalizeDouble(tick.ask+100*Point(),Digits()));
         break;
      case ORDER_TYPE_SELL :
         res=ExtTrade.Sell(InpLots);
         break;
      case ORDER_TYPE_SELL_LIMIT :
         res=ExtTrade.SellLimit(InpLots,NormalizeDouble(tick.bid+100*Point(),Digits()));
         break;
      case ORDER_TYPE_SELL_STOP :
         res=ExtTrade.SellStop(InpLots,NormalizeDouble(tick.bid-100*Point(),Digits()));
         break;
      default :
         res=false;
     }
   if(!res)
      Print("Error ",GetLastError());
   Print(ExtTrade.ResultRetcodeDescription());
 
//--- if the request is accepted, play the ok.wav sound
   if(ExtTrade.ResultRetcode()==TRADE_RETCODE_DONE)
      PlaySound(InpFileNameOK);
   else
      PlaySound(InpFileNameErr);
  }

```

See also

[Resources](/en/docs/runtime/resources)
