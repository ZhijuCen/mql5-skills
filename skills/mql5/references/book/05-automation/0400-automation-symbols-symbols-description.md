# Descriptive symbol properties

The platform provides a group of text properties for MQL programs that describe important qualitative characteristics. For example, when developing indicators or trading strategies based on a basket of financial instruments, it may be necessary to select symbols by country of origin, economic sector, or name of the underlying asset (if the instrument is a derivative).

| Identifier | Description |
| --- | --- |
| SYMBOL_BASIS | The name of the underlying asset for the derivative |
| SYMBOL_CATEGORY | The name of the category to which the financial instrument belongs |
| SYMBOL_COUNTRY | The country to which the financial instrument is assigned |
| SYMBOL_SECTOR_NAME | The sector of the economy to which the financial instrument belongs |
| SYMBOL_INDUSTRY_NAME | The branch of the economy or type of industry to which the financial instrument belongs |
| SYMBOL_BANK | Current quote source |
| SYMBOL_DESCRIPTION | String description of the symbol |
| SYMBOL_EXCHANGE | The name of the exchange or marketplace where the symbol is traded |
| SYMBOL_ISIN | A unique 12-digit alphanumeric code in the system of international securities identification codes - ISIN (International Securities Identification Number) |
| SYMBOL_PAGE | Internet page address with information on the symbol |
| SYMBOL_PATH | Path in symbol tree |

Another case where the program can apply the analysis of these properties occurs when looking for a conversion rate from one currency to another. We already know how to find a symbol with the right combination of [base and quote currency](/en/book/automation/symbols/symbols_currencies), but the difficulty is that there may be several such symbols. Reading properties like SYMBOL_SECTOR_NAME (you need to look for "Currency" or a synonym; check with your broker's specification) or SYMBOL_PATH can help in such cases.

The SYMBOL_PATH contains the entire hierarchy of folders in the symbols directory that contain the specific symbol: folder names are separated by backslashes ('\\') in the same way as the file system. The last element of the path is the name of the symbol itself.

Some string properties have integer counterparts. In particular, instead of SYMBOL_SECTOR_NAME, you can use the SYMBOL_SECTOR property, which returns an enumeration member [ENUM_SYMBOL_SECTOR](https://www.mql5.com/ru/docs/constants/environment_state/marketinfoconstants#enum_symbol_sector) with all supported sectors. By analogy, for SYMBOL_INDUSTRY_NAME there is a similar property SYMBOL_INDUSTRY with the [ENUM_SYMBOL_INDUSTRY](https://www.mql5.com/ru/docs/constants/environment_state/marketinfoconstants#enum_symbol_industry) enumeration type.

If necessary, an MQL program can even find the background color used when displaying a symbol in the Market Watch by simply reading the SYMBOL_BACKGROUND_COLOR property. This will allow those programs that create their own interface on the chart using [graphic objects](/en/book/applications/objects) (dialog boxes, lists, etc.), to make it unified with the native terminal controls.

Consider the example script SymbolFilterDescription.mq5, which outputs four predefined text properties for Market Watch symbols. The first of them is SYMBOL_DESCRIPTION (not to be confused with the name of the symbol itself), and it is by it that the resulting list will be sorted. The other three are purely for reference: SYMBOL_SECTOR_NAME, SYMBOL_COUNTRY, SYMBOL_PATH. All values are filled in in a specific way for each broker (there may be discrepancies for the same ticker).

We haven't mentioned it, but our SymbolFilter class implements a special overload of the equal method to compare strings. It supports searching for the occurrence of a substring with a pattern in which the wildcard character '*' stands for 0 or more arbitrary characters. For example, "*ian*" will find all characters that contain the substring "ian" (anywhere), and "*Index" will only find strings ending in "Index".

This feature resembles a substring search in the Symbols dialog available to users. However, there is no need to specify a wildcard character, because a substring is always searched for. In the algorithm which can be found in the source codes (SymbolFilter.mqh), we left the possibility to search for either a full match (there are no '*' characters) or a substring (there is at least one asterisk).

The comparison is case-sensitive. If necessary, it is easy to adapt the code for comparison without distinguishing between lowercase and uppercase letters.

Given the new feature, let's define an input variable for the search string in the description of the symbols. If the variable is empty, all symbols from the Market Watch window will be displayed.

```
input string SearchPattern = "";

```

Further, everything is as usual.

```
void OnStart()
{
   SymbolFilter f;                      // filter object
   string symbols[];                    // array of names
   string text[][4];                    // array of vectors with data
   
   // properties to read
   ENUM_SYMBOL_INFO_STRING fields[] =
   {
      SYMBOL_DESCRIPTION,
      SYMBOL_SECTOR_NAME,
      SYMBOL_COUNTRY,
      SYMBOL_PATH
   };
   
   if(SearchPattern != "")
   {
      f.let(SYMBOL_DESCRIPTION, SearchPattern);
   }
   
   // apply the filter and get arrays sorted by description
   f.select(true, fields, symbols, text, true);
   
   const int n = ArraySize(symbols);
   PrintFormat("===== Text fields for symbols (%d) =====", n);
   for(int i = 0; i < n; ++i)
   {
      Print(symbols[i] + ":");
      ArrayPrint(text, 0, NULL, i, 1, 0);
   }
}

```

Here is a possible version of the list (with abbreviations).

```
===== Text fields for symbols (16) =====
AUDUSD:
"Australian Dollar vs US Dollar" "Currency"   ""   "Forex\AUDUSD"
EURUSD:
"Euro vs US Dollar" "Currency"   ""   "Forex\EURUSD"     
UK100:
"FTSE 100 Index" "Undefined"   ""   "Indexes\UK100" 
XAUUSD:
"Gold vs US Dollar" "Commodities"   ""   "Metals\XAUUSD"    
JAGG:
    "JPMorgan U.S. Aggregate Bond ETF"  "Financial"
    "USA"   "ETF\United States\NYSE\JPMorgan\JAGG"
NZDUSD:
"New Zealand Dollar vs US Dollar" "Currency"   ""   "Forex\NZDUSD"
GBPUSD:
"Pound Sterling vs US Dollar" "Currency"   ""   "Forex\GBPUSD"
SP500m:
"Standard & Poor's 500" "Undefined"   ""   "Indexes\SP500m"
FIHD:
    "UBS AG FI Enhanced Global High Yield ETN" "Financial"
    "USA"   "ETF\United States\NYSE\UBS\FIHD"         
...

```

If we enter the search string "*ian*" into the input variable SearchPattern, we get the following result.

```
===== Text fields for symbols (3) =====
AUDUSD:
"Australian Dollar vs US Dollar" "Currency"   ""   "Forex\AUDUSD"
USDCAD:
"US Dollar vs Canadian Dollar" "Currency"   ""   "Forex\USDCAD"
USDRUB:
"US Dollar vs Russian Ruble" "Currency"   ""   "Forex\USDRUB"

```
