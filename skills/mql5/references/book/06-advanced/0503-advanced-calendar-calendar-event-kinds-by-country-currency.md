# Querying event types by country and currency

The calendar of economic events and holidays has its own specifics in each country. An MQL program can query the types of events within a particular country, as well as the types of events associated with a particular currency. The latter is relevant in cases where several countries use the same currency, as, for example, most members of the European Union.

int CalendarEventByCountry(const string country, MqlCalendarEvent &events[])

The CalendarEventByCountry function fills an array of MqlCalendarEvent structures passed by reference with descriptions of all types of events available in the calendar for the country specified by the two-letter country code (according to the ISO 3166-1 alpha-2 standard). We saw examples of such codes in the previous section, in the log: EU for the European Union, US for the USA, DE for Germany, CN for China, and so on.

The receiving array can be dynamic or fixed of sufficient size.

The function returns the number of received descriptions and 0 in case of an error. In particular, if the fixed array is not able to contain all events, the function will fill it with the fit part of the available data and set the code _LastError, equal to CALENDAR_MORE_DATA (5400). Memory allocation errors (4004, ERR_NOT_ENOUGH_MEMORY) or calendar request timeout from the server (5401, ERR_CALENDAR_TIMEOUT) are also possible.

If the country with the given code does not exist, an INTERNAL_ERROR (4001) will occur.

By specifying NULL or an empty string "" instead of country, you can get a complete list of events for all countries.

Let's test the performance of the function using the simple script CalendarEventKindsByCountry.mq5. It has a single input parameter which is the code of the country we are interested in.

```
input string CountryCode = "HK";

```

Next, a request for event types is made by calling CalendarEventByCountry, and if successful, the resulting arrays are logged.

```
void OnStart()
{
   MqlCalendarEvent events[];
   if(PRTF(CalendarEventByCountry(CountryCode, events)))
   {
      Print("Event kinds for country: ", CountryCode);
      ArrayPrint(events);
   }
}

```

Here is an example of the result (due to the fact that the lines are long, they are artificially divided into 2 blocks for publication in the book: the first block contains the numeric fields of the structures MqlCalendarEvent, and the second block contains string fields).

```
CalendarEventByCountry(CountryCode,events)=26 / ok
Event kinds for country: HK
          [id] [type] [sector] [frequency] [time_mode] [country_id] [unit] [importance] [multiplier] [digits] »
[ 0] 344010001      1        5           2           0          344      6            1            3        1 »
[ 1] 344010002      1        5           2           0          344      1            1            0        1 »
[ 2] 344020001      1        4           2           0          344      1            1            0        1 »
[ 3] 344020002      1        2           3           0          344      1            3            0        1 »
[ 4] 344020003      1        2           3           0          344      1            2            0        1 »
[ 5] 344020004      1        6           2           0          344      1            1            0        1 »
[ 6] 344020005      1        6           2           0          344      1            1            0        1 »
[ 7] 344020006      1        6           2           0          344      2            2            3        3 »
[ 8] 344020007      1        9           2           0          344      1            1            0        1 »
[ 9] 344020008      1        3           2           0          344      1            2            0        1 »
[10] 344030001      2       12           0           1          344      0            0            0        0 »
[11] 344030002      2       12           0           1          344      0            0            0        0 »
[12] 344030003      2       12           0           1          344      0            0            0        0 »
[13] 344030004      2       12           0           1          344      0            0            0        0 »
[14] 344030005      2       12           0           1          344      0            0            0        0 »
[15] 344030006      2       12           0           1          344      0            0            0        0 »
[16] 344030007      2       12           0           1          344      0            0            0        0 »
[17] 344030008      2       12           0           1          344      0            0            0        0 »
[18] 344030009      2       12           0           1          344      0            0            0        0 »
[19] 344030010      2       12           0           1          344      0            0            0        0 »
[20] 344030011      2       12           0           1          344      0            0            0        0 »
[21] 344030012      2       12           0           1          344      0            0            0        0 »
[22] 344030013      2       12           0           1          344      0            0            0        0 »
[23] 344030014      2       12           0           1          344      0            0            0        0 »
[24] 344030015      2       12           0           1          344      0            0            0        0 »
[25] 344500001      1        8           2           0          344      0            1            0        1 »
 

```

Continuation of the log (right fragment).

```
    »                      [source_url]                        [event_code]                                  [name]
[ 0]» "https://www.hkma.gov.hk/eng/"    "foreign-exchange-reserves"         "Foreign Exchange Reserves"            
[ 1]» "https://www.hkma.gov.hk/eng/"    "hkma-m3-money-supply-yy"           "HKMA M3 Money Supply y/y"             
[ 2]» "https://www.censtatd.gov.hk/en/" "cpi-yy"                            "CPI y/y"                              
[ 3]» "https://www.censtatd.gov.hk/en/" "gdp-qq"                            "GDP q/q"                              
[ 4]» "https://www.censtatd.gov.hk/en/" "gdp-yy"                            "GDP y/y"                              
[ 5]» "https://www.censtatd.gov.hk/en/" "exports-mm"                        "Exports y/y"                          
[ 6]» "https://www.censtatd.gov.hk/en/" "imports-mm"                        "Imports y/y"                          
[ 7]» "https://www.censtatd.gov.hk/en/" "trade-balance"                     "Trade Balance"                        
[ 8]» "https://www.censtatd.gov.hk/en/" "retail-sales-yy"                   "Retail Sales y/y"                     
[ 9]» "https://www.censtatd.gov.hk/en/" "unemployment-rate-3-months"        "Unemployment Rate 3-Months"           
[10]» "https://publicholidays.hk/"      "new-years-day"                     "New Year's Day"                       
[11]» "https://publicholidays.hk/"      "lunar-new-year"                    "Lunar New Year"                       
[12]» "https://publicholidays.hk/"      "ching-ming-festival"               "Ching Ming Festival"                  
[13]» "https://publicholidays.hk/"      "good-friday"                       "Good Friday"                          
[14]» "https://publicholidays.hk/"      "easter-monday"                     "Easter Monday"                        
[15]» "https://publicholidays.hk/"      "birthday-of-buddha"                "The Birthday of the Buddha"           
[16]» "https://publicholidays.hk/"      "labor-day"                         "Labor Day"                            
[17]» "https://publicholidays.hk/"      "tuen-ng-festival"                  "Tuen Ng Festival"                     
[18]» "https://publicholidays.hk/"      "hksar-establishment-day"           "HKSAR Establishment Day"              
[19]» "https://publicholidays.hk/"      "day-following-mid-autumn-festival" "The Day Following Mid-Autumn Festival"
[20]» "https://publicholidays.hk/"      "national-day"                      "National Day"                         
[21]» "https://publicholidays.hk/"      "chung-yeung-festival"              "Chung Yeung Festival"                 
[22]» "https://publicholidays.hk/"      "christmas-day"                     "Christmas Day"                        
[23]» "https://publicholidays.hk/"      "first-weekday-after-christmas-day" "The First Weekday After Christmas Day"
[24]» "https://publicholidays.hk/"      "day-following-good-friday"         "The Day Following Good Friday"        
[25]» "https://www.markiteconomics.com" "nikkei-pmi"                        "S&P Global PMI"                       
 

```

int CalendarEventByCurrency(const string currency, MqlCalendarEvent &events[])

The CalendarEventByCurrency function fills the passed events array with descriptions of all kinds of events in the calendar that are associated with the specified currency. The three-letter designation of currencies is known to all Forex traders.

If an invalid currency code is specified, the function will return 0 (no error) and an empty array.

Specifying NULL or an empty string "" instead of currency, you can get a complete list of calendar events.

Let's test the function using the script CalendarEventKindsByCurrency.mq5. The input parameter specifies the currency code.

```
input string Currency = "CNY";

```

In the handler OnStart we request events and output them to the log.

```
void OnStart()
{
   MqlCalendarEvent events[];
   if(PRTF(CalendarEventByCurrency(Currency, events)))
   {
      Print("Event kinds for currency: ", Currency);
      ArrayPrint(events);
   }
}

```

Here is an example of the result (given with abbreviations).

```
CalendarEventByCurrency(Currency,events)=40 / ok
Event kinds for currency: CNY
          [id] [type] [sector] [frequency] [time_mode] [country_id] [unit] [importance] [multiplier] [digits] »
[ 0] 156010001      1        4           2           0          156      1            2            0        1 »
[ 1] 156010002      1        4           2           0          156      1            1            0        1 »
[ 2] 156010003      1        4           2           0          156      1            1            0        1 »
[ 3] 156010004      1        2           3           0          156      1            3            0        1 »
[ 4] 156010005      1        2           3           0          156      1            2            0        1 »
[ 5] 156010006      1        9           2           0          156      1            2            0        1 »
[ 6] 156010007      1        8           2           0          156      1            2            0        1 »
[ 7] 156010008      1        8           2           0          156      0            3            0        1 »
[ 8] 156010009      1        8           2           0          156      0            3            0        1 »
[ 9] 156010010      1        8           2           0          156      1            2            0        1 »
[10] 156010011      0        5           0           0          156      0            2            0        0 »
[11] 156010012      1        3           2           0          156      1            2            0        1 »
[12] 156010013      1        8           2           0          156      1            1            0        1 »
[13] 156010014      1        8           2           0          156      1            1            0        1 »
[14] 156010015      1        8           2           0          156      0            3            0        1 »
[15] 156010016      1        8           2           0          156      1            2            0        1 »
[16] 156010017      1        9           2           0          156      1            2            0        1 »
[17] 156010018      1        2           3           0          156      1            2            0        1 »
[18] 156020001      1        6           2           3          156      6            2            3        2 »
[19] 156020002      1        6           2           3          156      1            1            0        1 »
[20] 156020003      1        6           2           3          156      1            1            0        1 »
[21] 156020004      1        6           2           3          156      2            2            3        2 »
[22] 156020005      1        6           2           3          156      1            1            0        1 »
[23] 156020006      1        6           2           3          156      1            1            0        1 »
...

```

Right fragment.

```
    »                        [source_url]                                 [event_code]                                       [name]
[ 0]» "http://www.stats.gov.cn/english/"  "cpi-mm"                                     "CPI m/m"                                   
[ 1]» "http://www.stats.gov.cn/english/"  "cpi-yy"                                     "CPI y/y"                                   
[ 2]» "http://www.stats.gov.cn/english/"  "ppi-yy"                                     "PPI y/y"                                   
[ 3]» "http://www.stats.gov.cn/english/"  "gdp-qq"                                     "GDP q/q"                                   
[ 4]» "http://www.stats.gov.cn/english/"  "gdp-yy"                                     "GDP y/y"                                   
[ 5]» "http://www.stats.gov.cn/english/"  "retail-sales-yy"                            "Retail Sales y/y"                          
[ 6]» "http://www.stats.gov.cn/english/"  "industrial-production-yy"                   "Industrial Production y/y"                 
[ 7]» "http://www.stats.gov.cn/english/"  "manufacturing-pmi"                          "Manufacturing PMI"                         
[ 8]» "http://www.stats.gov.cn/english/"  "non-manufacturing-pmi"                      "Non-Manufacturing PMI"                     
[ 9]» "http://www.stats.gov.cn/english/"  "fixed-asset-investment-yy"                  "Fixed Asset Investment y/y"                
[10]» "http://www.stats.gov.cn/english/"  "nbs-press-conference-on-economic-situation" "NBS Press Conference on Economic Situation"
[11]» "http://www.stats.gov.cn/english/"  "unemployment-rate"                          "Unemployment Rate"                         
[12]» "http://www.stats.gov.cn/english/"  "industrial-profit-yy"                       "Industrial Profit y/y"                     
[13]» "http://www.stats.gov.cn/english/"  "industrial-profit-ytd-yy"                   "Industrial Profit YTD y/y"                 
[14]» "http://www.stats.gov.cn/english/"  "composite-pmi"                              "Composite PMI"                             
[15]» "http://www.stats.gov.cn/english/"  "industrial-production-ytd-yy"               "Industrial Production YTD y/y"             
[16]» "http://www.stats.gov.cn/english/"  "retail-sales-ytd-yy"                        "Retail Sales YTD y/y"                      
[17]» "http://www.stats.gov.cn/english/"  "gdp-ytd-yy"                                 "GDP YTD y/y"                               
[18]» "http://english.customs.gov.cn/"    "trade-balance-usd"                          "Trade Balance USD"                         
[19]» "http://english.customs.gov.cn/"    "imports-usd-yy"                             "Imports USD y/y"                           
[20]» "http://english.customs.gov.cn/"    "exports-usd-yy"                             "Exports USD y/y"                           
[21]» "http://english.customs.gov.cn/"    "trade-balance"                              "Trade Balance"                             
[22]» "http://english.customs.gov.cn/"    "imports-yy"                                 "Imports y/y"                               
[23]» "http://english.customs.gov.cn/"    "exports-yy"                                 "Exports y/y"                               
...

```

An attentive reader will notice that the event type identifier contains the country code, the number of the news source and the serial number within the source (numbering starts from 1). So, the general format of the event type identifier is: CCCSSNNNN, where CCC is the country code, SS is the source, NNNN is the number. For example, 156020001 is the first news from the second source for China and 344030010 is the tenth news from the third source for Hong Kong. The only exception is global news, for which the "country" code is not 000 but 1000.
