# MqlBookInfo

It provides information about the market depth data.

```
struct MqlBookInfo
  {
   ENUM_BOOK_TYPE   type;            // Order type from ENUM_BOOK_TYPE enumeration
   double           price;           // Price
   long             volume;          // Volume
   double           volume_real;     // Volume with greater accuracy
  };

```

Note

The MqlBookInfo  structure is predefined, thus it doesn't require any declaration and description. To use the structure, just declare a variable of this type.

The DOM is available only for some symbols.

Example:

```
   MqlBookInfo priceArray[];
   bool getBook=MarketBookGet(NULL,priceArray);
   if(getBook)
     {
      int size=ArraySize(priceArray);
      Print("MarketBookInfo about ",Symbol());
     }
   else
     {
      Print("Failed to receive DOM for the symbol ",Symbol());
     }

```

See also

[MarketBookAdd](/en/docs/marketinformation/marketbookadd), [MarketBookRelease](/en/docs/marketinformation/marketbookrelease), [MarketBookGet](/en/docs/marketinformation/marketbookget), [Trade Orders in DOM](/en/docs/constants/tradingconstants/enum_trade_request_actions), [Data Types](/en/docs/basis/types)
