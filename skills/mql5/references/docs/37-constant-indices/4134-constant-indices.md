# List of MQL5 Constants

All MQL5 constants in alphabetical order.

| Constant | Description | Usage |
| --- | --- | --- |
| __DATE__ | File compilation date without time (hours, minutes and seconds are equal to 0) | Print |
| __DATETIME__ | File compilation date and time | Print |
| __FILE__ | Name of the currently compiled file | Print |
| __FUNCSIG__ | Signature of the function in whose body the macro is located. Logging of the full description of functions can be useful in the identification of  overloaded functions | Print |
| __FUNCTION__ | Name of the function, in whose body the macro is located | Print |
| __LINE__ | Line number in the source code, in which the macro is located | Print |
| __MQLBUILD__, __MQL5BUILD__ | Compiler build number | Print |
| __PATH__ | An absolute path to the file that is currently being compiled | Print |
| ACCOUNT_ASSETS | The current assets of an account | AccountInfoDouble |
| ACCOUNT_BALANCE | Account balance in the deposit currency | AccountInfoDouble |
| ACCOUNT_COMMISSION_BLOCKED | The current blocked commission amount on an account | AccountInfoDouble |
| ACCOUNT_COMPANY | Name of a company that serves the account | AccountInfoString |
| ACCOUNT_CREDIT | Account credit in the deposit currency | AccountInfoDouble |
| ACCOUNT_CURRENCY | Account currency | AccountInfoString |
| ACCOUNT_EQUITY | Account equity in the deposit currency | AccountInfoDouble |
| ACCOUNT_LEVERAGE | Account leverage | AccountInfoInteger |
| ACCOUNT_LIABILITIES | The current liabilities on an account | AccountInfoDouble |
| ACCOUNT_LIMIT_ORDERS | Maximum allowed number of active pending orders | AccountInfoInteger |
| ACCOUNT_LOGIN | Account number | AccountInfoInteger |
| ACCOUNT_MARGIN | Account margin used in the deposit currency | AccountInfoDouble |
| ACCOUNT_MARGIN_FREE | Free margin of an account in the deposit currency | AccountInfoDouble |
| ACCOUNT_MARGIN_INITIAL | Initial margin. The amount reserved on an account to cover the margin of all pending orders | AccountInfoDouble |
| ACCOUNT_MARGIN_LEVEL | Account margin level in percents | AccountInfoDouble |
| ACCOUNT_MARGIN_MAINTENANCE | Maintenance margin. The minimum equity reserved on an account to cover the minimum amount of all open positions | AccountInfoDouble |
| ACCOUNT_MARGIN_SO_CALL | Margin call level. Depending on the set ACCOUNT_MARGIN_SO_MODE is expressed in percents or in the deposit currency | AccountInfoDouble |
| ACCOUNT_MARGIN_SO_MODE | Mode for setting the minimal allowed margin | AccountInfoInteger |
| ACCOUNT_MARGIN_SO_SO | Margin stop out level. Depending on the set ACCOUNT_MARGIN_SO_MODE is expressed in percents or in the deposit currency | AccountInfoDouble |
| ACCOUNT_NAME | Client name | AccountInfoString |
| ACCOUNT_PROFIT | Current profit of an account in the deposit currency | AccountInfoDouble |
| ACCOUNT_SERVER | Trade server name | AccountInfoString |
| ACCOUNT_STOPOUT_MODE_MONEY | Account stop out mode in money | AccountInfoInteger |
| ACCOUNT_STOPOUT_MODE_PERCENT | Account stop out mode in percents | AccountInfoInteger |
| ACCOUNT_TRADE_ALLOWED | Allowed trade  for the current account | AccountInfoInteger |
| ACCOUNT_TRADE_EXPERT | Allowed trade  for an Expert Advisor | AccountInfoInteger |
| ACCOUNT_TRADE_MODE | Account trade mode | AccountInfoInteger |
| ACCOUNT_TRADE_MODE_CONTEST | Contest account | AccountInfoInteger |
| ACCOUNT_TRADE_MODE_DEMO | Demo account | AccountInfoInteger |
| ACCOUNT_TRADE_MODE_REAL | Real account | AccountInfoInteger |
| ALIGN_CENTER | Centered (only for the Edit object) | ObjectSetInteger ,  ObjectGetInteger ,  ChartScreenShot |
| ALIGN_LEFT | Left alignment | ObjectSetInteger ,  ObjectGetInteger ,  ChartScreenShot |
| ALIGN_RIGHT | Right alignment | ObjectSetInteger ,  ObjectGetInteger ,  ChartScreenShot |
| ANCHOR_CENTER | Anchor point strictly in the center of the object | ObjectSetInteger ,  ObjectGetInteger |
| ANCHOR_LEFT | Anchor point to the left in the center | ObjectSetInteger ,  ObjectGetInteger |
| ANCHOR_LEFT_LOWER | Anchor point at the lower left corner | ObjectSetInteger ,  ObjectGetInteger |
| ANCHOR_LEFT_UPPER | Anchor point at the upper left corner | ObjectSetInteger ,  ObjectGetInteger |
| ANCHOR_LOWER | Anchor point below in the center | ObjectSetInteger ,  ObjectGetInteger |
| ANCHOR_RIGHT | Anchor point to the right in the center | ObjectSetInteger ,  ObjectGetInteger |
| ANCHOR_RIGHT_LOWER | Anchor point at the lower right corner | ObjectSetInteger ,  ObjectGetInteger |
| ANCHOR_RIGHT_UPPER | Anchor point at the upper right corner | ObjectSetInteger ,  ObjectGetInteger |
| ANCHOR_UPPER | Anchor point above in the center | ObjectSetInteger ,  ObjectGetInteger |
| BASE_LINE | Main line | Indicators Lines |
| BOOK_TYPE_BUY | Buy order (Bid) | MqlBookInfo |
| BOOK_TYPE_BUY_MARKET | Buy order by Market | MqlBookInfo |
| BOOK_TYPE_SELL | Sell order (Offer) | MqlBookInfo |
| BOOK_TYPE_SELL_MARKET | Sell order by Market | MqlBookInfo |
| BORDER_FLAT | Flat form | ObjectSetInteger ,  ObjectGetInteger |
| BORDER_RAISED | Prominent form | ObjectSetInteger ,  ObjectGetInteger |
| BORDER_SUNKEN | Concave form | ObjectSetInteger ,  ObjectGetInteger |
| CHAR_MAX | Maximal value, which can be represented by char type | Numerical Type Constants |
| CHAR_MIN | Minimal value, which can be represented by char type | Numerical Type Constants |
| CHART_AUTOSCROLL | Mode of automatic moving to the right border of the chart | ChartSetInteger ,  ChartGetInteger |
| CHART_BARS | Display as a sequence of bars | ChartSetInteger |
| CHART_BEGIN | Chart beginning (the oldest prices) | ChartNavigate |
| CHART_BRING_TO_TOP | Show chart on top of other charts | ChartSetInteger ,  ChartGetInteger |
| CHART_CANDLES | Display as Japanese candlesticks | ChartSetInteger |
| CHART_COLOR_ASK | Ask price level color | ChartSetInteger ,  ChartGetInteger |
| CHART_COLOR_BACKGROUND | Chart background color | ChartSetInteger ,  ChartGetInteger |
| CHART_COLOR_BID | Bid price level color | ChartSetInteger ,  ChartGetInteger |
| CHART_COLOR_CANDLE_BEAR | Body color of a bear candlestick | ChartSetInteger ,  ChartGetInteger |
| CHART_COLOR_CANDLE_BULL | Body color of a bull candlestick | ChartSetInteger ,  ChartGetInteger |
| CHART_COLOR_CHART_DOWN | Color for the down bar, shadows and body borders of bear candlesticks | ChartSetInteger ,  ChartGetInteger |
| CHART_COLOR_CHART_LINE | Line chart color and color of "Doji" Japanese candlesticks | ChartSetInteger ,  ChartGetInteger |
| CHART_COLOR_CHART_UP | Color for the up bar, shadows and body borders of bull candlesticks | ChartSetInteger ,  ChartGetInteger |
| CHART_COLOR_FOREGROUND | Color of axes, scales and OHLC line | ChartSetInteger ,  ChartGetInteger |
| CHART_COLOR_GRID | Grid color | ChartSetInteger ,  ChartGetInteger |
| CHART_COLOR_LAST | Line color of the last executed deal price (Last) | ChartSetInteger ,  ChartGetInteger |
| CHART_COLOR_STOP_LEVEL | Color of stop order levels (Stop Loss and Take Profit) | ChartSetInteger ,  ChartGetInteger |
| CHART_COLOR_VOLUME | Color of volumes and position opening levels | ChartSetInteger ,  ChartGetInteger |
| CHART_COMMENT | Text of a comment in a chart | ChartSetString ,  ChartGetString |
| CHART_CURRENT_POS | Current position | ChartNavigate |
| CHART_DRAG_TRADE_LEVELS | Permission to drag trading levels on a chart with a mouse. The drag mode is enabled by default (true value) | ChartSetInteger ,  ChartGetInteger |
| CHART_EVENT_MOUSE_MOVE | Send notifications of mouse move and mouse click events ( CHARTEVENT_MOUSE_MOVE ) to all mql5 programs on a chart | ChartSetInteger ,  ChartGetInteger |
| CHART_EVENT_OBJECT_CREATE | Send a notification of an event of new object creation ( CHARTEVENT_OBJECT_CREATE ) to all mql5-programs on a chart | ChartSetInteger ,  ChartGetInteger |
| CHART_EVENT_OBJECT_DELETE | Send a notification of an event of object deletion ( CHARTEVENT_OBJECT_DELETE ) to all mql5-programs on a chart | ChartSetInteger ,  ChartGetInteger |
| CHART_FIRST_VISIBLE_BAR | Number of the first visible bar in the chart. Indexing of bars is the same as for  timeseries . | ChartSetInteger ,  ChartGetInteger |
| CHART_FIXED_MAX | Fixed  chart maximum | ChartSetDouble ,  ChartGetDouble |
| CHART_FIXED_MIN | Fixed  chart minimum | ChartSetDouble ,  ChartGetDouble |
| CHART_FIXED_POSITION | Chart fixed position from the left border in percent value. Chart fixed position is marked by a small gray triangle on the horizontal time axis. It is displayed only if the automatic chart scrolling to the right on tick incoming is disabled (see CHART_AUTOSCROLL property). The bar on a fixed position remains in the same place when zooming in and out. | ChartSetDouble ,  ChartGetDouble |
| CHART_FOREGROUND | Price chart in the foreground | ChartSetInteger ,  ChartGetInteger |
| CHART_HEIGHT_IN_PIXELS | Chart height in pixels | ChartSetInteger ,  ChartGetInteger |
| CHART_IS_OBJECT | Identifying "Chart" ( OBJ_CHART)  object – returns true for a graphical object. Returns false for a real chart | ChartSetInteger ,  ChartGetInteger |
| CHART_LINE | Display as a line drawn by Close prices | ChartSetInteger |
| CHART_MODE | Chart type (candlesticks, bars or line) | ChartSetInteger ,  ChartGetInteger |
| CHART_MOUSE_SCROLL | Scrolling the chart horizontally using the left mouse button. Vertical scrolling is also available if the value of any following properties is set to true: CHART_SCALEFIX, CHART_SCALEFIX_11 or CHART_SCALE_PT_PER_BAR | ChartSetInteger ,  ChartGetInteger |
| CHART_POINTS_PER_BAR | Scale in points per bar | ChartSetDouble ,  ChartGetDouble |
| CHART_PRICE_MAX | Chart maximum | ChartSetDouble ,  ChartGetDouble |
| CHART_PRICE_MIN | Chart minimum | ChartSetDouble ,  ChartGetDouble |
| CHART_SCALE | Scale | ChartSetInteger ,  ChartGetInteger |
| CHART_SCALE_PT_PER_BAR | Scale to be specified in points per bar | ChartSetInteger ,  ChartGetInteger |
| CHART_SCALEFIX | Fixed scale mode | ChartSetInteger ,  ChartGetInteger |
| CHART_SCALEFIX_11 | Scale 1:1 mode | ChartSetInteger ,  ChartGetInteger |
| CHART_SHIFT | Mode of price chart indent from the right border | ChartSetInteger ,  ChartGetInteger |
| CHART_SHIFT_SIZE | The size of the zero bar indent from the right border in percents | ChartSetDouble ,  ChartGetDouble |
| CHART_SHOW_ASK_LINE | Display Ask values as a horizontal line in a chart | ChartSetInteger ,  ChartGetInteger |
| CHART_SHOW_BID_LINE | Display Bid values as a horizontal line in a chart | ChartSetInteger ,  ChartGetInteger |
| CHART_SHOW_DATE_SCALE | Showing the time scale on a chart | ChartSetInteger ,  ChartGetInteger |
| CHART_SHOW_GRID | Display grid in the chart | ChartSetInteger ,  ChartGetInteger |
| CHART_SHOW_LAST_LINE | Display Last values as a horizontal line in a chart | ChartSetInteger ,  ChartGetInteger |
| CHART_SHOW_OBJECT_DESCR | Pop-up descriptions of graphical objects | ChartSetInteger ,  ChartGetInteger |
| CHART_SHOW_OHLC | Show OHLC values in the upper left corner | ChartSetInteger ,  ChartGetInteger |
| CHART_SHOW_ONE_CLICK | Showing the  "One click trading"  panel on a chart | ChartSetInteger ,  ChartGetInteger |
| CHART_SHOW_PERIOD_SEP | Display vertical separators between adjacent periods | ChartSetInteger ,  ChartGetInteger |
| CHART_SHOW_PRICE_SCALE | Showing the price scale on a chart | ChartSetInteger ,  ChartGetInteger |
| CHART_SHOW_TRADE_LEVELS | Displaying trade levels in the chart (levels of open positions, Stop Loss, Take Profit and pending orders) | ChartSetInteger ,  ChartGetInteger |
| CHART_SHOW_VOLUMES | Display volume in the chart | ChartSetInteger ,  ChartGetInteger |
| CHART_VISIBLE_BARS | The number of bars on the chart that can be displayed | ChartSetInteger ,  ChartGetInteger |
| CHART_VOLUME_HIDE | Volumes are not shown | ChartSetInteger |
| CHART_VOLUME_REAL | Trade volumes | ChartSetInteger |
| CHART_VOLUME_TICK | Tick volumes | ChartSetInteger |
| CHART_WIDTH_IN_BARS | Chart width in bars | ChartSetInteger ,  ChartGetInteger |
| CHART_WIDTH_IN_PIXELS | Chart width in pixels | ChartSetInteger ,  ChartGetInteger |
| CHART_WINDOW_HANDLE | Chart window handle (HWND) | ChartSetInteger ,  ChartGetInteger |
| CHART_WINDOW_IS_VISIBLE | Visibility of subwindows | ChartSetInteger ,  ChartGetInteger |
| CHART_WINDOW_YDISTANCE | The distance between the upper frame of the indicator subwindow and the upper frame of the main chart window, along the vertical Y axis, in pixels. In case of a mouse event, the cursor coordinates are passed in terms of the coordinates of the main chart window, while the coordinates of graphical objects in an indicator subwindow are set relative to the upper left corner of the subwindow.  
 The value is required for converting the absolute coordinates of the main chart to the local coordinates of a subwindow for correct work with the graphical objects, whose coordinates are set relative to  the upper left corner of the subwindow frame. | ChartSetInteger ,  ChartGetInteger |
| CHART_WINDOWS_TOTAL | The total number of chart windows, including indicator subwindows | ChartSetInteger ,  ChartGetInteger |
| CHARTEVENT_CHART_CHANGE | Change of the chart size or modification of chart properties through the Properties dialog | OnChartEvent |
| CHARTEVENT_CLICK | Clicking on a chart | OnChartEvent |
| CHARTEVENT_CUSTOM | Initial number of an event from a range of custom events | OnChartEvent |
| CHARTEVENT_CUSTOM_LAST | The final number of an event from a range of custom events | OnChartEvent |
| CHARTEVENT_KEYDOWN | Keystrokes | OnChartEvent |
| CHARTEVENT_MOUSE_MOVE | Mouse move, mouse clicks (if  CHART_EVENT_MOUSE_MOVE =true is set for the chart) | OnChartEvent |
| CHARTEVENT_OBJECT_CHANGE | Graphical object  property changed via the properties dialog | OnChartEvent |
| CHARTEVENT_OBJECT_CLICK | Clicking on a  graphical object | OnChartEvent |
| CHARTEVENT_OBJECT_CREATE | Graphical object  created (if  CHART_EVENT_OBJECT_CREATE =true is set for the chart) | OnChartEvent |
| CHARTEVENT_OBJECT_DELETE | Graphical object  deleted (if  CHART_EVENT_OBJECT_DELETE =true is set for the chart) | OnChartEvent |
| CHARTEVENT_OBJECT_DRAG | Drag and drop of a  graphical object | OnChartEvent |
| CHARTEVENT_OBJECT_ENDEDIT | End of text editing in the graphical object Edit | OnChartEvent |
| CHARTS_MAX | The maximum possible number of simultaneously open charts in the terminal | Other Constants |
| CHIKOUSPAN_LINE | Chikou Span line | Indicators Lines |
| clrAliceBlue | Alice Blue | Web Colors |
| clrAntiqueWhite | Antique White | Web Colors |
| clrAqua | Aqua | Web Colors |
| clrAquamarine | Aquamarine | Web Colors |
| clrBeige | Beige | Web Colors |
| clrBisque | Bisque | Web Colors |
| clrBlack | Black | Web Colors |
| clrBlanchedAlmond | Blanched Almond | Web Colors |
| clrBlue | Blue | Web Colors |
| clrBlueViolet | Blue Violet | Web Colors |
| clrBrown | Brown | Web Colors |
| clrBurlyWood | Burly Wood | Web Colors |
| clrCadetBlue | Cadet Blue | Web Colors |
| clrChartreuse | Chartreuse | Web Colors |
| clrChocolate | Chocolate | Web Colors |
| clrCoral | Coral | Web Colors |
| clrCornflowerBlue | Cornflower Blue | Web Colors |
| clrCornsilk | Cornsilk | Web Colors |
| clrCrimson | Crimson | Web Colors |
| clrDarkBlue | Dark Blue | Web Colors |
| clrDarkGoldenrod | Dark Goldenrod | Web Colors |
| clrDarkGray | Dark Gray | Web Colors |
| clrDarkGreen | Dark Green | Web Colors |
| clrDarkKhaki | Dark Khaki | Web Colors |
| clrDarkOliveGreen | Dark Olive Green | Web Colors |
| clrDarkOrange | Dark Orange | Web Colors |
| clrDarkOrchid | Dark Orchid | Web Colors |
| clrDarkSalmon | Dark Salmon | Web Colors |
| clrDarkSeaGreen | Dark Sea Green | Web Colors |
| clrDarkSlateBlue | Dark Slate Blue | Web Colors |
| clrDarkSlateGray | Dark Slate Gray | Web Colors |
| clrDarkTurquoise | Dark Turquoise | Web Colors |
| clrDarkViolet | Dark Violet | Web Colors |
| clrDeepPink | Deep Pink | Web Colors |
| clrDeepSkyBlue | Deep Sky Blue | Web Colors |
| clrDimGray | Dim Gray | Web Colors |
| clrDodgerBlue | Dodger Blue | Web Colors |
| clrFireBrick | Fire Brick | Web Colors |
| clrForestGreen | Forest Green | Web Colors |
| clrGainsboro | Gainsboro | Web Colors |
| clrGold | Gold | Web Colors |
| clrGoldenrod | Goldenrod | Web Colors |
| clrGray | Gray | Web Colors |
| clrGreen | Green | Web Colors |
| clrGreenYellow | Green Yellow | Web Colors |
| clrHoneydew | Honeydew | Web Colors |
| clrHotPink | Hot Pink | Web Colors |
| clrIndianRed | Indian Red | Web Colors |
| clrIndigo | Indigo | Web Colors |
| clrIvory | Ivory | Web Colors |
| clrKhaki | Khaki | Web Colors |
| clrLavender | Lavender | Web Colors |
| clrLavenderBlush | Lavender Blush | Web Colors |
| clrLawnGreen | Lawn Green | Web Colors |
| clrLemonChiffon | Lemon Chiffon | Web Colors |
| clrLightBlue | Light Blue | Web Colors |
| clrLightCoral | Light Coral | Web Colors |
| clrLightCyan | Light Cyan | Web Colors |
| clrLightGoldenrod | Light Goldenrod | Web Colors |
| clrLightGray | Light Gray | Web Colors |
| clrLightGreen | Light Green | Web Colors |
| clrLightPink | Light Pink | Web Colors |
| clrLightSalmon | Light Salmon | Web Colors |
| clrLightSeaGreen | Light Sea Green | Web Colors |
| clrLightSkyBlue | Light Sky Blue | Web Colors |
| clrLightSlateGray | Light Slate Gray | Web Colors |
| clrLightSteelBlue | Light Steel Blue | Web Colors |
| clrLightYellow | Light Yellow | Web Colors |
| clrLime | Lime | Web Colors |
| clrLimeGreen | Lime Green | Web Colors |
| clrLinen | Linen | Web Colors |
| clrMagenta | Magenta | Web Colors |
| clrMaroon | Maroon | Web Colors |
| clrMediumAquamarine | Medium Aquamarine | Web Colors |
| clrMediumBlue | Medium Blue | Web Colors |
| clrMediumOrchid | Medium Orchid | Web Colors |
| clrMediumPurple | Medium Purple | Web Colors |
| clrMediumSeaGreen | Medium Sea Green | Web Colors |
| clrMediumSlateBlue | Medium Slate Blue | Web Colors |
| clrMediumSpringGreen | Medium Spring Green | Web Colors |
| clrMediumTurquoise | Medium Turquoise | Web Colors |
| clrMediumVioletRed | Medium Violet Red | Web Colors |
| clrMidnightBlue | Midnight Blue | Web Colors |
| clrMintCream | Mint Cream | Web Colors |
| clrMistyRose | Misty Rose | Web Colors |
| clrMoccasin | Moccasin | Web Colors |
| clrNavajoWhite | Navajo White | Web Colors |
| clrNavy | Navy | Web Colors |
| clrNONE | Absence of color | Other Constants |
| clrOldLace | Old Lace | Web Colors |
| clrOlive | Olive | Web Colors |
| clrOliveDrab | Olive Drab | Web Colors |
| clrOrange | Orange | Web Colors |
| clrOrangeRed | Orange Red | Web Colors |
| clrOrchid | Orchid | Web Colors |
| clrPaleGoldenrod | Pale Goldenrod | Web Colors |
| clrPaleGreen | Pale Green | Web Colors |
| clrPaleTurquoise | Pale Turquoise | Web Colors |
| clrPaleVioletRed | Pale Violet Red | Web Colors |
| clrPapayaWhip | Papaya Whip | Web Colors |
| clrPeachPuff | Peach Puff | Web Colors |
| clrPeru | Peru | Web Colors |
| clrPink | Pink | Web Colors |
| clrPlum | Plum | Web Colors |
| clrPowderBlue | Powder Blue | Web Colors |
| clrPurple | Purple | Web Colors |
| clrRed | Red | Web Colors |
| clrRosyBrown | Rosy Brown | Web Colors |
| clrRoyalBlue | Royal Blue | Web Colors |
| clrSaddleBrown | Saddle Brown | Web Colors |
| clrSalmon | Salmon | Web Colors |
| clrSandyBrown | Sandy Brown | Web Colors |
| clrSeaGreen | Sea Green | Web Colors |
| clrSeashell | Seashell | Web Colors |
| clrSienna | Sienna | Web Colors |
| clrSilver | Silver | Web Colors |
| clrSkyBlue | Sky Blue | Web Colors |
| clrSlateBlue | Slate Blue | Web Colors |
| clrSlateGray | Slate Gray | Web Colors |
| clrSnow | Snow | Web Colors |
| clrSpringGreen | Spring Green | Web Colors |
| clrSteelBlue | Steel Blue | Web Colors |
| clrTan | Tan | Web Colors |
| clrTeal | Teal | Web Colors |
| clrThistle | Thistle | Web Colors |
| clrTomato | Tomato | Web Colors |
| clrTurquoise | Turquoise | Web Colors |
| clrViolet | Violet | Web Colors |
| clrWheat | Wheat | Web Colors |
| clrWhite | White | Web Colors |
| clrWhiteSmoke | White Smoke | Web Colors |
| clrYellow | Yellow | Web Colors |
| clrYellowGreen | Yellow Green | Web Colors |
| CORNER_LEFT_LOWER | Center of coordinates is in the lower left corner of the chart | ObjectSetInteger ,  ObjectGetInteger |
| CORNER_LEFT_UPPER | Center of coordinates is in the upper left corner of the chart | ObjectSetInteger ,  ObjectGetInteger |
| CORNER_RIGHT_LOWER | Center of coordinates is in the lower right corner of the chart | ObjectSetInteger ,  ObjectGetInteger |
| CORNER_RIGHT_UPPER | Center of coordinates is in the upper right corner of the chart | ObjectSetInteger ,  ObjectGetInteger |
| CP_ACP | The current Windows ANSI code page. | CharArrayToString ,  StringToCharArray ,  FileOpen |
| CP_MACCP | The current system Macintosh code page. 
 Note: This value is mostly used in earlier created program codes and is of no use now, since modern Macintosh computers use Unicode for encoding. | CharArrayToString ,  StringToCharArray ,  FileOpen |
| CP_OEMCP | The current system OEM code page. | CharArrayToString ,  StringToCharArray ,  FileOpen |
| CP_SYMBOL | Symbol code page | CharArrayToString ,  StringToCharArray ,  FileOpen |
| CP_THREAD_ACP | The Windows ANSI code page for the current thread. | CharArrayToString ,  StringToCharArray ,  FileOpen |
| CP_UTF7 | UTF-7 code page. | CharArrayToString ,  StringToCharArray ,  FileOpen |
| CP_UTF8 | UTF-8 code page. | CharArrayToString ,  StringToCharArray ,  FileOpen |
| CRYPT_AES128 | AES encryption with 128 bit key (16 bytes) | CryptEncode ,  CryptDecode |
| CRYPT_AES256 | AES encryption with 256 bit key (32 bytes) | CryptEncode ,  CryptDecode |
| CRYPT_ARCH_ZIP | ZIP archives | CryptEncode ,  CryptDecode |
| CRYPT_BASE64 | BASE64 | CryptEncode ,  CryptDecode |
| CRYPT_DES | DES encryption with 56 bit key (7 bytes) | CryptEncode ,  CryptDecode |
| CRYPT_HASH_MD5 | MD5 HASH calculation | CryptEncode ,  CryptDecode |
| CRYPT_HASH_SHA1 | SHA1 HASH calculation | CryptEncode ,  CryptDecode |
| CRYPT_HASH_SHA256 | SHA256 HASH calculation | CryptEncode ,  CryptDecode |
| DBL_DIG | Number of significant decimal digits for double type | Numerical Type Constants |
| DBL_EPSILON | Minimal value, which satisfies the condition: 
 1.0+DBL_EPSILON != 1.0 (for double type) | Numerical Type Constants |
| DBL_MANT_DIG | Bits count in a mantissa for double type | Numerical Type Constants |
| DBL_MAX | Maximal value, which can be represented by double type | Numerical Type Constants |
| DBL_MAX_10_EXP | Maximal decimal value of exponent degree for double type | Numerical Type Constants |
| DBL_MAX_EXP | Maximal binary value of exponent degree for double type | Numerical Type Constants |
| DBL_MIN | Minimal positive value, which can be represented by double type | Numerical Type Constants |
| DBL_MIN_10_EXP | Minimal decimal value of exponent degree for double type | Numerical Type Constants |
| DBL_MIN_EXP | Minimal binary value of exponent degree for double type | Numerical Type Constants |
| DEAL_COMMENT | Deal comment | HistoryDealGetString |
| DEAL_COMMISSION | Deal commission | HistoryDealGetDouble |
| DEAL_ENTRY | Deal entry - entry in, entry out, reverse | HistoryDealGetInteger |
| DEAL_ENTRY_IN | Entry in | HistoryDealGetInteger |
| DEAL_ENTRY_INOUT | Reverse | HistoryDealGetInteger |
| DEAL_ENTRY_OUT | Entry out | HistoryDealGetInteger |
| DEAL_MAGIC | Deal magic number (see  ORDER_MAGIC ) | HistoryDealGetInteger |
| DEAL_ORDER | Deal  order number | HistoryDealGetInteger |
| DEAL_POSITION_ID | Identifier of a position , in the opening, modification or change of which this deal took part. Each position has a unique identifier that is assigned to all deals executed for the symbol during the entire lifetime of the position. | HistoryDealGetInteger |
| DEAL_PRICE | Deal price | HistoryDealGetDouble |
| DEAL_PROFIT | Deal profit | HistoryDealGetDouble |
| DEAL_SWAP | Cumulative swap on close | HistoryDealGetDouble |
| DEAL_SYMBOL | Deal symbol | HistoryDealGetString |
| DEAL_TIME | Deal time | HistoryDealGetInteger |
| DEAL_TIME_MSC | The time of a deal execution in milliseconds since 01.01.1970 | HistoryDealGetInteger |
| DEAL_TYPE | Deal type | HistoryDealGetInteger |
| DEAL_TYPE_BALANCE | Balance | HistoryDealGetInteger |
| DEAL_TYPE_BONUS | Bonus | HistoryDealGetInteger |
| DEAL_TYPE_BUY | Buy | HistoryDealGetInteger |
| DEAL_TYPE_BUY_CANCELED | Canceled buy deal. There can be a situation when a previously executed buy deal is canceled. In this case, the type of the previously executed deal (DEAL_TYPE_BUY) is changed to DEAL_TYPE_BUY_CANCELED, and its profit/loss is zeroized. Previously obtained profit/loss is charged/withdrawn using a separated balance operation | HistoryDealGetInteger |
| DEAL_TYPE_CHARGE | Additional charge | HistoryDealGetInteger |
| DEAL_TYPE_COMMISSION | Additional commission | HistoryDealGetInteger |
| DEAL_TYPE_COMMISSION_AGENT_DAILY | Daily agent commission | HistoryDealGetInteger |
| DEAL_TYPE_COMMISSION_AGENT_MONTHLY | Monthly agent commission | HistoryDealGetInteger |
| DEAL_TYPE_COMMISSION_DAILY | Daily commission | HistoryDealGetInteger |
| DEAL_TYPE_COMMISSION_MONTHLY | Monthly commission | HistoryDealGetInteger |
| DEAL_TYPE_CORRECTION | Correction | HistoryDealGetInteger |
| DEAL_TYPE_CREDIT | Credit | HistoryDealGetInteger |
| DEAL_TYPE_INTEREST | Interest rate | HistoryDealGetInteger |
| DEAL_TYPE_SELL | Sell | HistoryDealGetInteger |
| DEAL_TYPE_SELL_CANCELED | Canceled sell deal. There can be a situation when a previously executed sell deal is canceled. In this case, the type of the previously executed deal (DEAL_TYPE_SELL) is changed to DEAL_TYPE_SELL_CANCELED, and its profit/loss is zeroized. Previously obtained profit/loss is charged/withdrawn using a separated balance operation | HistoryDealGetInteger |
| DEAL_VOLUME | Deal volume | HistoryDealGetDouble |
| DRAW_ARROW | Drawing arrows | Drawing Styles |
| DRAW_BARS | Display as a sequence of bars | Drawing Styles |
| DRAW_CANDLES | Display as a sequence of candlesticks | Drawing Styles |
| DRAW_COLOR_ARROW | Drawing multicolored arrows | Drawing Styles |
| DRAW_COLOR_BARS | Multicolored bars | Drawing Styles |
| DRAW_COLOR_CANDLES | Multicolored candlesticks | Drawing Styles |
| DRAW_COLOR_HISTOGRAM | Multicolored histogram from the zero line | Drawing Styles |
| DRAW_COLOR_HISTOGRAM2 | Multicolored histogram of the two indicator buffers | Drawing Styles |
| DRAW_COLOR_LINE | Multicolored line | Drawing Styles |
| DRAW_COLOR_SECTION | Multicolored section | Drawing Styles |
| DRAW_COLOR_ZIGZAG | Multicolored ZigZag | Drawing Styles |
| DRAW_FILLING | Color fill between the two levels | Drawing Styles |
| DRAW_HISTOGRAM | Histogram from the zero line | Drawing Styles |
| DRAW_HISTOGRAM2 | Histogram of the two indicator buffers | Drawing Styles |
| DRAW_LINE | Line | Drawing Styles |
| DRAW_NONE | Not drawn | Drawing Styles |
| DRAW_SECTION | Section | Drawing Styles |
| DRAW_ZIGZAG | Style Zigzag allows vertical section on the bar | Drawing Styles |
| ELLIOTT_CYCLE | Cycle | ObjectSetInteger ,  ObjectGetInteger |
| ELLIOTT_GRAND_SUPERCYCLE | Grand Supercycle | ObjectSetInteger ,  ObjectGetInteger |
| ELLIOTT_INTERMEDIATE | Intermediate | ObjectSetInteger ,  ObjectGetInteger |
| ELLIOTT_MINOR | Minor | ObjectSetInteger ,  ObjectGetInteger |
| ELLIOTT_MINUETTE | Minuette | ObjectSetInteger ,  ObjectGetInteger |
| ELLIOTT_MINUTE | Minute | ObjectSetInteger ,  ObjectGetInteger |
| ELLIOTT_PRIMARY | Primary | ObjectSetInteger ,  ObjectGetInteger |
| ELLIOTT_SUBMINUETTE | Subminuette | ObjectSetInteger ,  ObjectGetInteger |
| ELLIOTT_SUPERCYCLE | Supercycle | ObjectSetInteger ,  ObjectGetInteger |
| EMPTY_VALUE | Empty value in an indicator buffer | Other Constants |
| ERR_ACCOUNT_WRONG_PROPERTY | Wrong account property ID | GetLastError |
| ERR_ARRAY_BAD_SIZE | Requested array size exceeds 2 GB | GetLastError |
| ERR_ARRAY_RESIZE_ERROR | Not enough memory for the relocation of an array, or an attempt to change the size of a static array | GetLastError |
| ERR_BOOKS_CANNOT_ADD | Depth Of Market can not be added | GetLastError |
| ERR_BOOKS_CANNOT_DELETE | Depth Of Market can not be removed | GetLastError |
| ERR_BOOKS_CANNOT_GET | The data from Depth Of Market can not be obtained | GetLastError |
| ERR_BOOKS_CANNOT_SUBSCRIBE | Error in subscribing to receive new data from Depth Of Market | GetLastError |
| ERR_BUFFERS_NO_MEMORY | Not enough memory for the distribution of indicator buffers | GetLastError |
| ERR_BUFFERS_WRONG_INDEX | Wrong indicator buffer index | GetLastError |
| ERR_CANNOT_CLEAN_DIRECTORY | Failed to clear the directory (probably one or more files are blocked and removal operation failed) | GetLastError |
| ERR_CANNOT_DELETE_DIRECTORY | The directory cannot be removed | GetLastError |
| ERR_CANNOT_DELETE_FILE | File deleting error | GetLastError |
| ERR_CANNOT_OPEN_FILE | File opening error | GetLastError |
| ERR_CHAR_ARRAY_ONLY | Must be an array of type char | GetLastError |
| ERR_CHART_CANNOT_CHANGE | Failed to change chart symbol and period | GetLastError |
| ERR_CHART_CANNOT_CREATE_TIMER | Failed to create timer | GetLastError |
| ERR_CHART_CANNOT_OPEN | Chart opening error | GetLastError |
| ERR_CHART_INDICATOR_CANNOT_ADD | Error adding an indicator to chart | GetLastError |
| ERR_CHART_INDICATOR_CANNOT_DEL | Error deleting an indicator from the chart | GetLastError |
| ERR_CHART_INDICATOR_NOT_FOUND | Indicator not found on the specified chart | GetLastError |
| ERR_CHART_NAVIGATE_FAILED | Error navigating through chart | GetLastError |
| ERR_CHART_NO_EXPERT | No Expert Advisor in the chart that could handle the event | GetLastError |
| ERR_CHART_NO_REPLY | Chart does not respond | GetLastError |
| ERR_CHART_NOT_FOUND | Chart not found | GetLastError |
| ERR_CHART_SCREENSHOT_FAILED | Error creating screenshots | GetLastError |
| ERR_CHART_TEMPLATE_FAILED | Error applying template | GetLastError |
| ERR_CHART_WINDOW_NOT_FOUND | Subwindow containing the indicator was not found | GetLastError |
| ERR_CHART_WRONG_ID | Wrong chart ID | GetLastError |
| ERR_CHART_WRONG_PARAMETER | Error value of the parameter for the  function of working with charts | GetLastError |
| ERR_CHART_WRONG_PROPERTY | Wrong chart property ID | GetLastError |
| ERR_CUSTOM_WRONG_PROPERTY | Wrong ID of the custom indicator property | GetLastError |
| ERR_DIRECTORY_NOT_EXIST | Directory does not exist | GetLastError |
| ERR_DOUBLE_ARRAY_ONLY | Must be an array of type double | GetLastError |
| ERR_FILE_BINSTRINGSIZE | String size must be specified, because the file is opened as binary | GetLastError |
| ERR_FILE_CACHEBUFFER_ERROR | Not enough memory for cache to read | GetLastError |
| ERR_FILE_CANNOT_REWRITE | File can not be rewritten | GetLastError |
| ERR_FILE_IS_DIRECTORY | This is not a file, this is a directory | GetLastError |
| ERR_FILE_ISNOT_DIRECTORY | This is a file, not a directory | GetLastError |
| ERR_FILE_NOT_EXIST | File does not exist | GetLastError |
| ERR_FILE_NOTBIN | The file must be opened as a binary one | GetLastError |
| ERR_FILE_NOTCSV | The file must be opened as CSV | GetLastError |
| ERR_FILE_NOTTOREAD | The file must be opened for reading | GetLastError |
| ERR_FILE_NOTTOWRITE | The file must be opened for writing | GetLastError |
| ERR_FILE_NOTTXT | The file must be opened as a text | GetLastError |
| ERR_FILE_NOTTXTORCSV | The file must be opened as a text or CSV | GetLastError |
| ERR_FILE_READERROR | File reading error | GetLastError |
| ERR_FILE_WRITEERROR | Failed to write a resource to a file | GetLastError |
| ERR_FLOAT_ARRAY_ONLY | Must be an array of type float | GetLastError |
| ERR_FTP_SEND_FAILED | File sending via ftp failed | GetLastError |
| ERR_FUNCTION_NOT_ALLOWED | Function is not allowed for call | GetLastError |
| ERR_GLOBALVARIABLE_EXISTS | Global variable of the client terminal with the same name already exists | GetLastError |
| ERR_GLOBALVARIABLE_NOT_FOUND | Global variable of the client terminal is not found | GetLastError |
| ERR_HISTORY_NOT_FOUND | Requested history not found | GetLastError |
| ERR_HISTORY_WRONG_PROPERTY | Wrong ID of the history property | GetLastError |
| ERR_INCOMPATIBLE_ARRAYS | Copying incompatible arrays. String array can be copied only to a string array, and a numeric array - in numeric array only | GetLastError |
| ERR_INCOMPATIBLE_FILE | A text file must be for string arrays, for other arrays - binary | GetLastError |
| ERR_INDICATOR_CANNOT_ADD | Error applying an indicator to chart | GetLastError |
| ERR_INDICATOR_CANNOT_APPLY | The indicator cannot be applied to another indicator | GetLastError |
| ERR_INDICATOR_CANNOT_CREATE | Indicator cannot be created | GetLastError |
| ERR_INDICATOR_CUSTOM_NAME | The first parameter in the array must be the name of the custom indicator | GetLastError |
| ERR_INDICATOR_DATA_NOT_FOUND | Requested data not found | GetLastError |
| ERR_INDICATOR_NO_MEMORY | Not enough memory to add the indicator | GetLastError |
| ERR_INDICATOR_PARAMETER_TYPE | Invalid parameter type in the array when creating an indicator | GetLastError |
| ERR_INDICATOR_PARAMETERS_MISSING | No parameters when creating an indicator | GetLastError |
| ERR_INDICATOR_UNKNOWN_SYMBOL | Unknown symbol | GetLastError |
| ERR_INDICATOR_WRONG_HANDLE | Wrong indicator handle | GetLastError |
| ERR_INDICATOR_WRONG_INDEX | Wrong index of the requested indicator buffer | GetLastError |
| ERR_INDICATOR_WRONG_PARAMETERS | Wrong number of parameters when creating an indicator | GetLastError |
| ERR_INT_ARRAY_ONLY | Must be an array of type int | GetLastError |
| ERR_INTERNAL_ERROR | Unexpected internal error | GetLastError |
| ERR_INVALID_ARRAY | Array of a wrong type, wrong size, or a damaged object of a dynamic array | GetLastError |
| ERR_INVALID_DATETIME | Invalid date and/or time | GetLastError |
| ERR_INVALID_FILEHANDLE | A file with this handle was closed, or was not opening at all | GetLastError |
| ERR_INVALID_PARAMETER | Wrong parameter when calling the system function | GetLastError |
| ERR_INVALID_POINTER | Wrong pointer | GetLastError |
| ERR_INVALID_POINTER_TYPE | Wrong type of pointer | GetLastError |
| ERR_LONG_ARRAY_ONLY | Must be an array of type long | GetLastError |
| ERR_MAIL_SEND_FAILED | Email sending failed | GetLastError |
| ERR_MARKET_LASTTIME_UNKNOWN | Time of the last tick is not known (no ticks) | GetLastError |
| ERR_MARKET_NOT_SELECTED | Symbol is not selected in MarketWatch | GetLastError |
| ERR_MARKET_SELECT_ERROR | Error adding or deleting a symbol in MarketWatch | GetLastError |
| ERR_MARKET_UNKNOWN_SYMBOL | Unknown symbol | GetLastError |
| ERR_MARKET_WRONG_PROPERTY | Wrong identifier of a symbol property | GetLastError |
| ERR_MQL5_WRONG_PROPERTY | Wrong identifier of the program property | GetLastError |
| ERR_NO_STRING_DATE | No date in the string | GetLastError |
| ERR_NOT_ENOUGH_MEMORY | Not enough memory to perform the system function | GetLastError |
| ERR_NOTIFICATION_SEND_FAILED | Failed to send a  notification | GetLastError |
| ERR_NOTIFICATION_TOO_FREQUENT | Too frequent sending of notifications | GetLastError |
| ERR_NOTIFICATION_WRONG_PARAMETER | Invalid parameter for sending a notification – an empty string or  NULL  has been passed to the  SendNotification()  function | GetLastError |
| ERR_NOTIFICATION_WRONG_SETTINGS | Wrong settings of notifications in the terminal (ID is not specified or permission is not set) | GetLastError |
| ERR_NOTINITIALIZED_STRING | Not initialized string | GetLastError |
| ERR_NUMBER_ARRAYS_ONLY | Must be a numeric array | GetLastError |
| ERR_OBJECT_ERROR | Error working with a graphical object | GetLastError |
| ERR_OBJECT_GETDATE_FAILED | Unable to get date corresponding to the value | GetLastError |
| ERR_OBJECT_GETVALUE_FAILED | Unable to get value corresponding to the date | GetLastError |
| ERR_OBJECT_NOT_FOUND | Graphical object was not found | GetLastError |
| ERR_OBJECT_WRONG_PROPERTY | Wrong ID of a graphical object property | GetLastError |
| ERR_ONEDIM_ARRAYS_ONLY | Must be a one-dimensional array | GetLastError |
| ERR_OPENCL_BUFFER_CREATE | Failed to create an  OpenCL buffer | GetLastError |
| ERR_OPENCL_CONTEXT_CREATE | Error creating the  OpenCL context | GetLastError |
| ERR_OPENCL_EXECUTE | OpenCL program  runtime error | GetLastError |
| ERR_OPENCL_INTERNAL | Internal error occurred when  running OpenCL | GetLastError |
| ERR_OPENCL_INVALID_HANDLE | Invalid  OpenCL handle | GetLastError |
| ERR_OPENCL_KERNEL_CREATE | Error creating an  OpenCL kernel | GetLastError |
| ERR_OPENCL_NOT_SUPPORTED | OpenCL functions  are not supported on this computer | GetLastError |
| ERR_OPENCL_PROGRAM_CREATE | Error occurred when  compiling an OpenCL program | GetLastError |
| ERR_OPENCL_QUEUE_CREATE | Failed to create a run queue in OpenCL | GetLastError |
| ERR_OPENCL_SET_KERNEL_PARAMETER | Error occurred when  setting parameters  for the OpenCL kernel | GetLastError |
| ERR_OPENCL_TOO_LONG_KERNEL_NAME | Too long kernel name  (OpenCL kernel) | GetLastError |
| ERR_OPENCL_WRONG_BUFFER_OFFSET | Invalid offset in the OpenCL buffer | GetLastError |
| ERR_OPENCL_WRONG_BUFFER_SIZE | Invalid size of the OpenCL buffer | GetLastError |
| ERR_PLAY_SOUND_FAILED | Sound playing failed | GetLastError |
| ERR_RESOURCE_NAME_DUPLICATED | The names of the  dynamic  and the  static  resource match | GetLastError |
| ERR_RESOURCE_NAME_IS_TOO_LONG | The resource name exceeds 63 characters | GetLastError |
| ERR_RESOURCE_NOT_FOUND | Resource with this name has not been found in EX5 | GetLastError |
| ERR_RESOURCE_UNSUPPORTED_TYPE | Unsupported resource type or its size exceeds 16 Mb | GetLastError |
| ERR_SERIES_ARRAY | Timeseries cannot be used | GetLastError |
| ERR_SHORT_ARRAY_ONLY | Must be an array of type short | GetLastError |
| ERR_SMALL_ARRAY | Too small array, the starting position is outside the array | GetLastError |
| ERR_SMALL_ASSERIES_ARRAY | The receiving array is declared as AS_SERIES, and it is of insufficient size | GetLastError |
| ERR_STRING_OUT_OF_MEMORY | Not enough memory for the string | GetLastError |
| ERR_STRING_RESIZE_ERROR | Not enough memory for the relocation of string | GetLastError |
| ERR_STRING_SMALL_LEN | The string length is less than expected | GetLastError |
| ERR_STRING_TIME_ERROR | Error converting string to date | GetLastError |
| ERR_STRING_TOO_BIGNUMBER | Too large number, more than ULONG_MAX | GetLastError |
| ERR_STRING_UNKNOWNTYPE | Unknown data type when converting to a string | GetLastError |
| ERR_STRING_ZEROADDED | 0 added to the string end, a useless operation | GetLastError |
| ERR_STRINGPOS_OUTOFRANGE | Position outside the string | GetLastError |
| ERR_STRUCT_WITHOBJECTS_ORCLASS | The structure contains objects of strings and/or dynamic arrays and/or structure of such objects and/or classes | GetLastError |
| ERR_SUCCESS | The operation completed successfully | GetLastError |
| ERR_TERMINAL_WRONG_PROPERTY | Wrong identifier of the terminal property | GetLastError |
| ERR_TOO_LONG_FILENAME | Too long file name | GetLastError |
| ERR_TOO_MANY_FILES | More than 64 files cannot be opened at the same time | GetLastError |
| ERR_TOO_MANY_FORMATTERS | Amount of format specifiers more than the parameters | GetLastError |
| ERR_TOO_MANY_PARAMETERS | Amount of parameters more than the format specifiers | GetLastError |
| ERR_TRADE_DEAL_NOT_FOUND | Deal not found | GetLastError |
| ERR_TRADE_DISABLED | Trading by Expert Advisors prohibited | GetLastError |
| ERR_TRADE_ORDER_NOT_FOUND | Order not found | GetLastError |
| ERR_TRADE_POSITION_NOT_FOUND | Position not found | GetLastError |
| ERR_TRADE_SEND_FAILED | Trade request sending failed | GetLastError |
| ERR_TRADE_WRONG_PROPERTY | Wrong trade property ID | GetLastError |
| ERR_USER_ERROR_FIRST | User defined  errors start with this code | GetLastError |
| ERR_WEBREQUEST_CONNECT_FAILED | Failed to connect to specified URL | GetLastError |
| ERR_WEBREQUEST_INVALID_ADDRESS | Invalid URL | GetLastError |
| ERR_WEBREQUEST_REQUEST_FAILED | HTTP request failed | GetLastError |
| ERR_WEBREQUEST_TIMEOUT | Timeout exceeded | GetLastError |
| ERR_WRONG_DIRECTORYNAME | Wrong directory name | GetLastError |
| ERR_WRONG_FILEHANDLE | Wrong file handle | GetLastError |
| ERR_WRONG_FILENAME | Invalid file name | GetLastError |
| ERR_WRONG_FORMATSTRING | Invalid format string | GetLastError |
| ERR_WRONG_INTERNAL_PARAMETER | Wrong parameter in the inner call of the client terminal function | GetLastError |
| ERR_WRONG_STRING_DATE | Wrong date in the string | GetLastError |
| ERR_WRONG_STRING_OBJECT | Damaged string object | GetLastError |
| ERR_WRONG_STRING_PARAMETER | Damaged parameter of string type | GetLastError |
| ERR_WRONG_STRING_TIME | Wrong time in the string | GetLastError |
| ERR_ZEROSIZE_ARRAY | An array of zero length | GetLastError |
| FILE_ACCESS_DATE | Date of the last access to the file | FileGetInteger |
| FILE_ANSI | Strings of ANSI type (one byte symbols). Flag is used in  FileOpen() . | FileOpen |
| FILE_BIN | Binary read/write mode (without string to string conversion). Flag is used in  FileOpen() . | FileOpen |
| FILE_COMMON | The file path in the common folder of all client terminals \Terminal\Common\Files. Flag is used in  FileOpen() ,  FileCopy() ,  FileMove()  and in  FileIsExist()  functions. | FileOpen ,  FileCopy ,  FileMove ,  FileIsExist |
| FILE_CREATE_DATE | Date of creation | FileGetInteger |
| FILE_CSV | CSV file (all its elements are converted to strings of the appropriate type, Unicode or ANSI, and separated by separator). Flag is used in  FileOpen() . | FileOpen |
| FILE_END | Get the end of file sign | FileGetInteger |
| FILE_EXISTS | Check the existence | FileGetInteger |
| FILE_IS_ANSI | The file is opened as ANSI (see  FILE_ANSI ) | FileGetInteger |
| FILE_IS_BINARY | The file is opened as a binary file (see  FILE_BIN ) | FileGetInteger |
| FILE_IS_COMMON | The file is opened in a shared folder of all terminals (see  FILE_COMMON ) | FileGetInteger |
| FILE_IS_CSV | The file is opened as CSV (see  FILE_CSV ) | FileGetInteger |
| FILE_IS_READABLE | The opened file is readable (see  FILE_READ ) | FileGetInteger |
| FILE_IS_TEXT | The file is opened as a text file (see  FILE_TXT ) | FileGetInteger |
| FILE_IS_WRITABLE | The opened file is writable (see  FILE_WRITE ) | FileGetInteger |
| FILE_LINE_END | Get the end of line sign | FileGetInteger |
| FILE_MODIFY_DATE | Date of the last modification | FileGetInteger |
| FILE_POSITION | Position of a pointer in the file | FileGetInteger |
| FILE_READ | File is opened for reading. Flag is used in  FileOpen() . When opening a file specification of FILE_WRITE and/or FILE_READ is required. | FileOpen |
| FILE_REWRITE | Possibility for the file rewrite using functions  FileCopy()  and  FileMove() . The file should exist or should be opened for writing, otherwise the file will not be opened. | FileCopy ,  FileMove |
| FILE_SHARE_READ | Shared access for reading from several programs. Flag is used in  FileOpen() , but it does not replace the necessity to indicate FILE_WRITE and/or the FILE_READ flag when opening a file. | FileOpen |
| FILE_SHARE_WRITE | Shared access for writing from several programs. Flag is used in  FileOpen() , but it does not replace the necessity to indicate FILE_WRITE and/or the FILE_READ flag when opening a file. | FileOpen |
| FILE_SIZE | File size in bytes | FileGetInteger |
| FILE_TXT | Simple text file (the same as csv file, but without taking into account the separators). Flag is used in  FileOpen() . | FileOpen |
| FILE_UNICODE | Strings of UNICODE type (two byte symbols). Flag is used in  FileOpen() . | FileOpen |
| FILE_WRITE | File is opened for writing. Flag is used in  FileOpen() . When opening a file specification of FILE_WRITE and/or FILE_READ is required. | FileOpen |
| FLT_DIG | Number of significant decimal digits for float type | Numerical Type Constants |
| FLT_EPSILON | Minimal value, which satisfies the condition: 
 1.0+DBL_EPSILON != 1.0 (for float type) | Numerical Type Constants |
| FLT_MANT_DIG | Bits count in a mantissa for float type | Numerical Type Constants |
| FLT_MAX | Maximal value, which can be represented by float type | Numerical Type Constants |
| FLT_MAX_10_EXP | Maximal decimal value of exponent degree for float type | Numerical Type Constants |
| FLT_MAX_EXP | Maximal binary value of exponent degree for float type | Numerical Type Constants |
| FLT_MIN | Minimal positive value, which can be represented by float type | Numerical Type Constants |
| FLT_MIN_10_EXP | Minimal decimal value of exponent degree for float type | Numerical Type Constants |
| FLT_MIN_EXP | Minimal binary value of exponent degree for float type | Numerical Type Constants |
| FRIDAY | Friday | SymbolInfoInteger ,  SymbolInfoSessionQuote ,  SymbolInfoSessionTrade |
| GANN_DOWN_TREND | Line corresponding to the downward trend | ObjectSetInteger ,  ObjectGetInteger |
| GANN_UP_TREND | Line corresponding to the uptrend line | ObjectSetInteger ,  ObjectGetInteger |
| GATORJAW_LINE | Jaw line | Indicators Lines |
| GATORLIPS_LINE | Lips line | Indicators Lines |
| GATORTEETH_LINE | Teeth line | Indicators Lines |
| IDABORT | "Abort" button has been pressed | MessageBox |
| IDCANCEL | "Cancel" button has been pressed | MessageBox |
| IDCONTINUE | "Continue" button has been pressed | MessageBox |
| IDIGNORE | "Ignore" button has been pressed | MessageBox |
| IDNO | "No" button has been pressed | MessageBox |
| IDOK | "OK" button has been pressed | MessageBox |
| IDRETRY | "Retry" button has been pressed | MessageBox |
| IDTRYAGAIN | "Try Again" button has been pressed | MessageBox |
| IDYES | "Yes" button has been pressed | MessageBox |
| IND_AC | Accelerator Oscillator | IndicatorCreate ,  IndicatorParameters |
| IND_AD | Accumulation/Distribution | IndicatorCreate ,  IndicatorParameters |
| IND_ADX | Average Directional Index | IndicatorCreate ,  IndicatorParameters |
| IND_ADXW | ADX by Welles Wilder | IndicatorCreate ,  IndicatorParameters |
| IND_ALLIGATOR | Alligator | IndicatorCreate ,  IndicatorParameters |
| IND_AMA | Adaptive Moving Average | IndicatorCreate ,  IndicatorParameters |
| IND_AO | Awesome Oscillator | IndicatorCreate ,  IndicatorParameters |
| IND_ATR | Average True Range | IndicatorCreate ,  IndicatorParameters |
| IND_BANDS | Bollinger Bands® | IndicatorCreate ,  IndicatorParameters |
| IND_BEARS | Bears Power | IndicatorCreate ,  IndicatorParameters |
| IND_BULLS | Bulls Power | IndicatorCreate ,  IndicatorParameters |
| IND_BWMFI | Market Facilitation Index | IndicatorCreate ,  IndicatorParameters |
| IND_CCI | Commodity Channel Index | IndicatorCreate ,  IndicatorParameters |
| IND_CHAIKIN | Chaikin Oscillator | IndicatorCreate ,  IndicatorParameters |
| IND_CUSTOM | Custom indicator | IndicatorCreate ,  IndicatorParameters |
| IND_DEMA | Double Exponential Moving Average | IndicatorCreate ,  IndicatorParameters |
| IND_DEMARKER | DeMarker | IndicatorCreate ,  IndicatorParameters |
| IND_ENVELOPES | Envelopes | IndicatorCreate ,  IndicatorParameters |
| IND_FORCE | Force Index | IndicatorCreate ,  IndicatorParameters |
| IND_FRACTALS | Fractals | IndicatorCreate ,  IndicatorParameters |
| IND_FRAMA | Fractal Adaptive Moving Average | IndicatorCreate ,  IndicatorParameters |
| IND_GATOR | Gator Oscillator | IndicatorCreate ,  IndicatorParameters |
| IND_ICHIMOKU | Ichimoku Kinko Hyo | IndicatorCreate ,  IndicatorParameters |
| IND_MA | Moving Average | IndicatorCreate ,  IndicatorParameters |
| IND_MACD | MACD | IndicatorCreate ,  IndicatorParameters |
| IND_MFI | Money Flow Index | IndicatorCreate ,  IndicatorParameters |
| IND_MOMENTUM | Momentum | IndicatorCreate ,  IndicatorParameters |
| IND_OBV | On Balance Volume | IndicatorCreate ,  IndicatorParameters |
| IND_OSMA | OsMA | IndicatorCreate ,  IndicatorParameters |
| IND_RSI | Relative Strength Index | IndicatorCreate ,  IndicatorParameters |
| IND_RVI | Relative Vigor Index | IndicatorCreate ,  IndicatorParameters |
| IND_SAR | Parabolic SAR | IndicatorCreate ,  IndicatorParameters |
| IND_STDDEV | Standard Deviation | IndicatorCreate ,  IndicatorParameters |
| IND_STOCHASTIC | Stochastic Oscillator | IndicatorCreate ,  IndicatorParameters |
| IND_TEMA | Triple Exponential Moving Average | IndicatorCreate ,  IndicatorParameters |
| IND_TRIX | Triple Exponential Moving Averages Oscillator | IndicatorCreate ,  IndicatorParameters |
| IND_VIDYA | Variable Index Dynamic Average | IndicatorCreate ,  IndicatorParameters |
| IND_VOLUMES | Volumes | IndicatorCreate ,  IndicatorParameters |
| IND_WPR | Williams' Percent Range | IndicatorCreate ,  IndicatorParameters |
| INDICATOR_CALCULATIONS | Auxiliary buffers for intermediate calculations | SetIndexBuffer |
| INDICATOR_COLOR_INDEX | Color | SetIndexBuffer |
| INDICATOR_DATA | Data to draw | SetIndexBuffer |
| INDICATOR_DIGITS | Accuracy of drawing of indicator values | IndicatorSetInteger |
| INDICATOR_HEIGHT | Fixed height of the indicator's window (the preprocessor command  #property indicator_height ) | IndicatorSetInteger |
| INDICATOR_LEVELCOLOR | Color of the level line | IndicatorSetInteger |
| INDICATOR_LEVELS | Number of levels in the indicator window | IndicatorSetInteger |
| INDICATOR_LEVELSTYLE | Style of the level line | IndicatorSetInteger |
| INDICATOR_LEVELTEXT | Level description | IndicatorSetString |
| INDICATOR_LEVELVALUE | Level value | IndicatorSetDouble |
| INDICATOR_LEVELWIDTH | Thickness of the level line | IndicatorSetInteger |
| INDICATOR_MAXIMUM | Maximum of the indicator window | IndicatorSetDouble |
| INDICATOR_MINIMUM | Minimum of the indicator window | IndicatorSetDouble |
| INDICATOR_SHORTNAME | Short indicator name | IndicatorSetString |
| INT_MAX | Maximal value, which can be represented by int type | Numerical Type Constants |
| INT_MIN | Minimal value, which can be represented by int type | Numerical Type Constants |
| INVALID_HANDLE | Incorrect handle | Other Constants |
| IS_DEBUG_MODE | Flag that a mq5-program operates in debug mode | Other Constants |
| IS_PROFILE_MODE | Flag that a mq5-program operates in profiling mode | Other Constants |
| KIJUNSEN_LINE | Kijun-sen line | Indicators Lines |
| LICENSE_DEMO | A trial version of a paid product from the Market. It works only in the strategy tester | MQLInfoInteger |
| LICENSE_FREE | A free unlimited version | MQLInfoInteger |
| LICENSE_FULL | A purchased licensed version allows at least 5 activations. The number of activations is specified by seller. Seller may increase the allowed number of activations | MQLInfoInteger |
| LICENSE_TIME | A version with a limited term license | MQLInfoInteger |
| LONG_MAX | Maximal value, which can be represented by long type | Numerical Type Constants |
| LONG_MIN | Minimal value, which can be represented by long type | Numerical Type Constants |
| LOWER_BAND | Lower limit | Indicators Lines |
| LOWER_HISTOGRAM | Bottom histogram | Indicators Lines |
| LOWER_LINE | Bottom line | Indicators Lines |
| M_1_PI | 1/pi | Mathematical Constants |
| M_2_PI | 2/pi | Mathematical Constants |
| M_2_SQRTPI | 2/sqrt(pi) | Mathematical Constants |
| M_E | e | Mathematical Constants |
| M_LN10 | ln(10) | Mathematical Constants |
| M_LN2 | ln(2) | Mathematical Constants |
| M_LOG10E | log10(e) | Mathematical Constants |
| M_LOG2E | log2(e) | Mathematical Constants |
| M_PI | pi | Mathematical Constants |
| M_PI_2 | pi/2 | Mathematical Constants |
| M_PI_4 | pi/4 | Mathematical Constants |
| M_SQRT1_2 | 1/sqrt(2) | Mathematical Constants |
| M_SQRT2 | sqrt(2) | Mathematical Constants |
| MAIN_LINE | Main line | Indicators Lines |
| MB_ABORTRETRYIGNORE | Message window contains three buttons: Abort, Retry and Ignore | MessageBox |
| MB_CANCELTRYCONTINUE | Message window contains three buttons: Cancel, Try Again, Continue | MessageBox |
| MB_DEFBUTTON1 | The first button MB_DEFBUTTON1 - is default, if the other buttons MB_DEFBUTTON2, MB_DEFBUTTON3, or MB_DEFBUTTON4 are not specified | MessageBox |
| MB_DEFBUTTON2 | The second button is default | MessageBox |
| MB_DEFBUTTON3 | The third button is default | MessageBox |
| MB_DEFBUTTON4 | The fourth button is default | MessageBox |
| MB_ICONEXCLAMATION,  
 MB_ICONWARNING | The exclamation/warning sign icon | MessageBox |
| MB_ICONINFORMATION,  
 MB_ICONASTERISK | The encircled i sign | MessageBox |
| MB_ICONQUESTION | The question sign icon | MessageBox |
| MB_ICONSTOP,  
 MB_ICONERROR,  
 MB_ICONHAND | The STOP sign icon | MessageBox |
| MB_OK | Message window contains only one button: OK. Default | MessageBox |
| MB_OKCANCEL | Message window contains two buttons: OK and Cancel | MessageBox |
| MB_RETRYCANCEL | Message window contains two buttons: Retry and Cancel | MessageBox |
| MB_YESNO | Message window contains two buttons: Yes and No | MessageBox |
| MB_YESNOCANCEL | Message window contains three buttons: Yes, No and Cancel | MessageBox |
| MINUSDI_LINE | Line –DI | Indicators Lines |
| MODE_EMA | Exponential averaging | Smoothing Methods |
| MODE_LWMA | Linear-weighted averaging | Smoothing Methods |
| MODE_SMA | Simple averaging | Smoothing Methods |
| MODE_SMMA | Smoothed averaging | Smoothing Methods |
| MONDAY | Monday | SymbolInfoInteger ,  SymbolInfoSessionQuote ,  SymbolInfoSessionTrade |
| MQL_DEBUG | The flag, that indicates the debug mode | MQLInfoInteger |
| MQL_DLLS_ALLOWED | The permission to use DLL for the given executed program | MQLInfoInteger |
| MQL_FRAME_MODE | The flag, that indicates the Expert Advisor operating in  gathering optimization result frames mode | MQLInfoInteger |
| MQL_LICENSE_TYPE | Type of license of the EX5 module. The license refers to the EX5 module, from which a request is made using MQLInfoInteger(MQL_LICENSE_TYPE). | MQLInfoInteger |
| MQL_MEMORY_LIMIT | Maximum possible amount of dynamic memory for MQL5 program in MB | MQLInfoInteger |
| MQL_MEMORY_USED | The memory size used by MQL5 program in MB | MQLInfoInteger |
| MQL_OPTIMIZATION | The flag, that indicates the optimization process | MQLInfoInteger |
| MQL_PROFILER | The flag, that indicates the program operating in the code profiling mode | MQLInfoInteger |
| MQL_PROGRAM_NAME | Name of the mql5-program executed | MQLInfoString |
| MQL_PROGRAM_PATH | Path for the given executed program | MQLInfoString |
| MQL_PROGRAM_TYPE | Type of the mql5 program | MQLInfoInteger |
| MQL_SIGNALS_ALLOWED | The permission to modify the Signals for the given executed program | MQLInfoInteger |
| MQL_TESTER | The flag, that indicates the tester process | MQLInfoInteger |
| MQL_TRADE_ALLOWED | The  permission to trade  for the given executed program | MQLInfoInteger |
| MQL_VISUAL_MODE | The flag, that indicates the visual tester process | MQLInfoInteger |
| NULL | Zero for any types | Other Constants |
| OBJ_ALL_PERIODS | The object is drawn in all timeframes | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_ARROW | Arrow | Object Types |
| OBJ_ARROW_BUY | Buy Sign | Object Types |
| OBJ_ARROW_CHECK | Check Sign | Object Types |
| OBJ_ARROW_DOWN | Arrow Down | Object Types |
| OBJ_ARROW_LEFT_PRICE | Left Price Label | Object Types |
| OBJ_ARROW_RIGHT_PRICE | Right Price Label | Object Types |
| OBJ_ARROW_SELL | Sell Sign | Object Types |
| OBJ_ARROW_STOP | Stop Sign | Object Types |
| OBJ_ARROW_THUMB_DOWN | Thumbs Down | Object Types |
| OBJ_ARROW_THUMB_UP | Thumbs Up | Object Types |
| OBJ_ARROW_UP | Arrow Up | Object Types |
| OBJ_ARROWED_LINE | Arrowed Line | Object Types |
| OBJ_BITMAP | Bitmap | Object Types |
| OBJ_BITMAP_LABEL | Bitmap Label | Object Types |
| OBJ_BUTTON | Button | Object Types |
| OBJ_CHANNEL | Equidistant Channel | Object Types |
| OBJ_CHART | Chart | Object Types |
| OBJ_CYCLES | Cycle Lines | Object Types |
| OBJ_EDIT | Edit | Object Types |
| OBJ_ELLIOTWAVE3 | Elliott Correction Wave | Object Types |
| OBJ_ELLIOTWAVE5 | Elliott Motive Wave | Object Types |
| OBJ_ELLIPSE | Ellipse | Object Types |
| OBJ_EVENT | The "Event" object corresponding to an event in the economic calendar | Object Types |
| OBJ_EXPANSION | Fibonacci Expansion | Object Types |
| OBJ_FIBO | Fibonacci Retracement | Object Types |
| OBJ_FIBOARC | Fibonacci Arcs | Object Types |
| OBJ_FIBOCHANNEL | Fibonacci Channel | Object Types |
| OBJ_FIBOFAN | Fibonacci Fan | Object Types |
| OBJ_FIBOTIMES | Fibonacci Time Zones | Object Types |
| OBJ_GANNFAN | Gann Fan | Object Types |
| OBJ_GANNGRID | Gann Grid | Object Types |
| OBJ_GANNLINE | Gann Line | Object Types |
| OBJ_HLINE | Horizontal Line | Object Types |
| OBJ_LABEL | Label | Object Types |
| OBJ_NO_PERIODS | The object is not drawn in all timeframes | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_D1 | The object is drawn in day charts | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_H1 | The object is drawn in 1-hour chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_H12 | The object is drawn in 12-hour chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_H2 | The object is drawn in 2-hour chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_H3 | The object is drawn in 3-hour chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_H4 | The object is drawn in 4-hour chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_H6 | The object is drawn in 6-hour chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_H8 | The object is drawn in 8-hour chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_M1 | The object is drawn in 1-minute chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_M10 | The object is drawn in 10-minute chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_M12 | The object is drawn in 12-minute chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_M15 | The object is drawn in 15-minute chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_M2 | The object is drawn in 2-minute chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_M20 | The object is drawn in 20-minute chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_M3 | The object is drawn in 3-minute chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_M30 | The object is drawn in 30-minute chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_M4 | The object is drawn in 4-minute chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_M5 | The object is drawn in 5-minute chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_M6 | The object is drawn in 6-minute chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_MN1 | The object is drawn in month charts | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PERIOD_W1 | The object is drawn in week charts | ObjectSetInteger ,  ObjectGetInteger |
| OBJ_PITCHFORK | Andrews’ Pitchfork | Object Types |
| OBJ_RECTANGLE | Rectangle | Object Types |
| OBJ_RECTANGLE_LABEL | The "Rectangle label" object for creating and designing the custom graphical interface. | Object Types |
| OBJ_REGRESSION | Linear Regression Channel | Object Types |
| OBJ_STDDEVCHANNEL | Standard Deviation Channel | Object Types |
| OBJ_TEXT | Text | Object Types |
| OBJ_TREND | Trend Line | Object Types |
| OBJ_TRENDBYANGLE | Trend Line By Angle | Object Types |
| OBJ_TRIANGLE | Triangle | Object Types |
| OBJ_VLINE | Vertical Line | Object Types |
| OBJPROP_ALIGN | Horizontal text alignment in the "Edit" object (OBJ_EDIT) | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_ANCHOR | Location of the anchor point of a graphical object | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_ANGLE | Angle.  For the objects with no angle specified, created from a program, the value is equal to  EMPTY_VALUE | ObjectSetDouble ,  ObjectGetDouble |
| OBJPROP_ARROWCODE | Arrow code for the Arrow object | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_BACK | Object in the background | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_BGCOLOR | The background color for  OBJ_EDIT, OBJ_BUTTON, OBJ_RECTANGLE_LABEL | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_BMPFILE | The name of BMP-file for Bitmap Label. See also  Resources | ObjectSetString ,  ObjectGetString |
| OBJPROP_BORDER_COLOR | Border color for the OBJ_EDIT and OBJ_BUTTON objects | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_BORDER_TYPE | Border type for the "Rectangle label" object | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_CHART_ID | ID of the "Chart" object ( OBJ_CHART ). It allows working with the properties of this object like with a normal chart using the functions described in  Chart Operations , but there some  exceptions . | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_CHART_SCALE | The scale for the Chart object | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_COLOR | Color | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_CORNER | The corner of the chart to link a graphical object | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_CREATETIME | Time of object creation | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_DATE_SCALE | Displaying the time scale for the Chart object | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_DEGREE | Level of the Elliott Wave Marking | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_DEVIATION | Deviation for the Standard Deviation Channel | ObjectSetDouble ,  ObjectGetDouble |
| OBJPROP_DIRECTION | Trend of the Gann object | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_DRAWLINES | Displaying lines for marking the Elliott Wave | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_ELLIPSE | Showing the full ellipse of the Fibonacci Arc object ( OBJ_FIBOARC ) | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_FILL | Fill an object with color (for OBJ_RECTANGLE, OBJ_TRIANGLE, OBJ_ELLIPSE, OBJ_CHANNEL, OBJ_STDDEVCHANNEL, OBJ_REGRESSION) | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_FONT | Font | ObjectSetString ,  ObjectGetString |
| OBJPROP_FONTSIZE | Font size | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_HIDDEN | Prohibit showing of the name of a graphical object in the list of objects from the terminal menu "Charts" - "Objects" - "List of objects". The true value allows to hide an object from the list. By default, true is set to the objects that display calendar events, trading history and to the objects  created from MQL5 programs . To see such  graphical objects  and access their properties, click on the "All" button in the "List of objects" window. | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_LEVELCOLOR | Color of the line-level | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_LEVELS | Number of levels | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_LEVELSTYLE | Style of the line-level | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_LEVELTEXT | Level description | ObjectSetString ,  ObjectGetString |
| OBJPROP_LEVELVALUE | Level value | ObjectSetDouble ,  ObjectGetDouble |
| OBJPROP_LEVELWIDTH | Thickness of the line-level | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_NAME | Object name | ObjectSetString ,  ObjectGetString |
| OBJPROP_PERIOD | Timeframe for the Chart object | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_PRICE | Price coordinate | ObjectSetDouble ,  ObjectGetDouble |
| OBJPROP_PRICE_SCALE | Displaying the price scale for the Chart object | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_RAY | A vertical line goes through all the windows of a chart | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_RAY_LEFT | Ray goes to the left | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_RAY_RIGHT | Ray goes to the right | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_READONLY | Ability to edit text in the Edit object | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_SCALE | Scale (properties of Gann objects and Fibonacci Arcs) | ObjectSetDouble ,  ObjectGetDouble |
| OBJPROP_SELECTABLE | Object availability | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_SELECTED | Object is selected | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_STATE | Button state (pressed / depressed) | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_STYLE | Style | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_SYMBOL | Symbol for the Chart object | ObjectSetString ,  ObjectGetString |
| OBJPROP_TEXT | Description of the object (the text contained in the object) | ObjectSetString ,  ObjectGetString |
| OBJPROP_TIME | Time coordinate | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_TIMEFRAMES | Visibility of an object at timeframes | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_TOOLTIP | The text of a tooltip. If the property is not set, then the tooltip generated automatically by the terminal is shown. A tooltip can be disabled by setting the "\n" (line feed) value to it | ObjectSetString ,  ObjectGetString |
| OBJPROP_TYPE | Object type | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_WIDTH | Line thickness | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_XDISTANCE | The distance in pixels along the X axis from the binding corner (see  note ) | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_XOFFSET | The X coordinate of the upper left corner of the  rectangular visible area  in the graphical objects "Bitmap Label" and "Bitmap" (OBJ_BITMAP_LABEL and OBJ_BITMAP). The value is set in pixels relative to the upper left corner of the original image. | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_XSIZE | The object's width along the X axis in pixels. Specified for  OBJ_LABEL (read only), OBJ_BUTTON, OBJ_CHART, OBJ_BITMAP, OBJ_BITMAP_LABEL, OBJ_EDIT, OBJ_RECTANGLE_LABEL objects. | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_YDISTANCE | The distance in pixels along the Y axis from the binding corner (see  note ) | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_YOFFSET | The Y coordinate of the upper left corner of the  rectangular visible area  in the graphical objects "Bitmap Label" and "Bitmap" (OBJ_BITMAP_LABEL and OBJ_BITMAP). The value is set in pixels relative to the upper left corner of the original image. | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_YSIZE | The object's height along the Y axis in pixels. Specified for  OBJ_LABEL (read only), OBJ_BUTTON, OBJ_CHART, OBJ_BITMAP, OBJ_BITMAP_LABEL, OBJ_EDIT, OBJ_RECTANGLE_LABEL objects. | ObjectSetInteger ,  ObjectGetInteger |
| OBJPROP_ZORDER | Priority of a graphical object for receiving events of clicking on a chart ( CHARTEVENT_CLICK ). The default zero value is set when creating an object; the priority can be increased if necessary. When applying objects one over another, only one of them with the highest priority will receive the CHARTEVENT_CLICK event. | ObjectSetInteger ,  ObjectGetInteger |
| ORDER_COMMENT | Order comment | OrderGetString ,  HistoryOrderGetString |
| ORDER_FILLING_FOK | This filling policy means that an order can be filled only in the specified amount. If the necessary amount of a financial instrument is currently unavailable in the market, the order will not be executed. The required volume can be filled using several offers available on the market at the moment. | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_FILLING_IOC | This mode means that a trader agrees to execute a deal with the volume maximally available in the market within that indicated in the order. In case the the entire volume of an order cannot be filled, the available volume of it will be filled, and the remaining volume will be canceled. | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_FILLING_RETURN | This policy is used only for market orders (ORDER_TYPE_BUY and ORDER_TYPE_SELL), limit and stop limit orders (ORDER_TYPE_BUY_LIMIT, ORDER_TYPE_SELL_LIMIT, ORDER_TYPE_BUY_STOP_LIMIT and ORDER_TYPE_SELL_STOP_LIMIT ) and only for the symbols with Market or Exchange  execution . In case of partial filling a market or limit order with remaining volume is not canceled but processed further. 
 For the activation of the ORDER_TYPE_BUY_STOP_LIMIT and ORDER_TYPE_SELL_STOP_LIMIT orders, a corresponding limit order ORDER_TYPE_BUY_LIMIT/ORDER_TYPE_SELL_LIMIT with the ORDER_FILLING_RETURN execution type is created. | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_MAGIC | ID of an Expert Advisor that has placed the order (designed to ensure that each Expert Advisor places its own unique number) | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_POSITION_ID | Position identifier  that is set to an order as soon as it is executed. Each executed order results in a  deal  that opens or modifies an already existing position. The identifier of exactly this position is set to the executed order at this moment. | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_PRICE_CURRENT | The current price of the order symbol | OrderGetDouble ,  HistoryOrderGetDouble |
| ORDER_PRICE_OPEN | Price specified in the order | OrderGetDouble ,  HistoryOrderGetDouble |
| ORDER_PRICE_STOPLIMIT | The Limit order price for the StopLimit order | OrderGetDouble ,  HistoryOrderGetDouble |
| ORDER_SL | Stop Loss value | OrderGetDouble ,  HistoryOrderGetDouble |
| ORDER_STATE | Order state | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_STATE_CANCELED | Order canceled by client | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_STATE_EXPIRED | Order expired | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_STATE_FILLED | Order fully executed | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_STATE_PARTIAL | Order partially executed | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_STATE_PLACED | Order accepted | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_STATE_REJECTED | Order rejected | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_STATE_REQUEST_ADD | Order is being registered (placing to the trading system) | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_STATE_REQUEST_CANCEL | Order is being deleted (deleting from the trading system) | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_STATE_REQUEST_MODIFY | Order is being modified (changing its parameters) | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_STATE_STARTED | Order checked, but not yet accepted by broker | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_SYMBOL | Symbol of the order | OrderGetString ,  HistoryOrderGetString |
| ORDER_TIME_DAY | Good till current trade day order | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TIME_DONE | Order execution or cancellation time | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TIME_DONE_MSC | Order execution/cancellation time in milliseconds since 01.01.1970 | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TIME_EXPIRATION | Order expiration time | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TIME_GTC | Good till cancel order | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TIME_SETUP | Order setup time | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TIME_SETUP_MSC | The time of placing an order for execution in milliseconds since 01.01.1970 | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TIME_SPECIFIED | Good till expired order | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TIME_SPECIFIED_DAY | The order will be effective till 23:59:59 of the specified day. If this time is outside a trading session, the order expires in the nearest trading time. | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TP | Take Profit value | OrderGetDouble ,  HistoryOrderGetDouble |
| ORDER_TYPE | Order type | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TYPE_BUY | Market Buy order | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TYPE_BUY_LIMIT | Buy Limit pending order | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TYPE_BUY_STOP | Buy Stop pending order | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TYPE_BUY_STOP_LIMIT | Upon reaching the order price, a pending Buy Limit order is placed at the StopLimit price | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TYPE_FILLING | Order filling type | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TYPE_SELL | Market Sell order | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TYPE_SELL_LIMIT | Sell Limit pending order | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TYPE_SELL_STOP | Sell Stop pending order | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TYPE_SELL_STOP_LIMIT | Upon reaching the order price, a pending Sell Limit order is placed at the StopLimit price | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_TYPE_TIME | Order lifetime | OrderGetInteger ,  HistoryOrderGetInteger |
| ORDER_VOLUME_CURRENT | Order current volume | OrderGetDouble ,  HistoryOrderGetDouble |
| ORDER_VOLUME_INITIAL | Order initial volume | OrderGetDouble ,  HistoryOrderGetDouble |
| PERIOD_CURRENT | Current timeframe | Chart Timeframes |
| PERIOD_D1 | 1 day | Chart Timeframes |
| PERIOD_H1 | 1 hour | Chart Timeframes |
| PERIOD_H12 | 12 hours | Chart Timeframes |
| PERIOD_H2 | 2 hours | Chart Timeframes |
| PERIOD_H3 | 3 hours | Chart Timeframes |
| PERIOD_H4 | 4 hours | Chart Timeframes |
| PERIOD_H6 | 6 hours | Chart Timeframes |
| PERIOD_H8 | 8 hours | Chart Timeframes |
| PERIOD_M1 | 1 minute | Chart Timeframes |
| PERIOD_M10 | 10 minutes | Chart Timeframes |
| PERIOD_M12 | 12 minutes | Chart Timeframes |
| PERIOD_M15 | 15 minutes | Chart Timeframes |
| PERIOD_M2 | 2 minutes | Chart Timeframes |
| PERIOD_M20 | 20 minutes | Chart Timeframes |
| PERIOD_M3 | 3 minutes | Chart Timeframes |
| PERIOD_M30 | 30 minutes | Chart Timeframes |
| PERIOD_M4 | 4 minutes | Chart Timeframes |
| PERIOD_M5 | 5 minutes | Chart Timeframes |
| PERIOD_M6 | 6 minutes | Chart Timeframes |
| PERIOD_MN1 | 1 month | Chart Timeframes |
| PERIOD_W1 | 1 week | Chart Timeframes |
| PLOT_ARROW | Arrow code for style DRAW_ARROW | PlotIndexSetInteger ,  PlotIndexGetInteger |
| PLOT_ARROW_SHIFT | Vertical shift of arrows for style DRAW_ARROW | PlotIndexSetInteger ,  PlotIndexGetInteger |
| PLOT_COLOR_INDEXES | The number of colors | PlotIndexSetInteger ,  PlotIndexGetInteger |
| PLOT_DRAW_BEGIN | Number of initial bars without drawing and values in the DataWindow | PlotIndexSetInteger ,  PlotIndexGetInteger |
| PLOT_DRAW_TYPE | Type of graphical construction | PlotIndexSetInteger ,  PlotIndexGetInteger |
| PLOT_EMPTY_VALUE | An empty value for plotting, for which there is no drawing | PlotIndexSetDouble |
| PLOT_LABEL | The name of the indicator graphical series to display in the DataWindow. When working with complex graphical styles requiring several indicator buffers for display, the names for each buffer can be specified using ";" as a separator. Sample code is shown in  DRAW_CANDLES | PlotIndexSetString |
| PLOT_LINE_COLOR | The index of a buffer containing the drawing color | PlotIndexSetInteger ,  PlotIndexGetInteger |
| PLOT_LINE_STYLE | Drawing line style | PlotIndexSetInteger ,  PlotIndexGetInteger |
| PLOT_LINE_WIDTH | The thickness of the drawing line | PlotIndexSetInteger ,  PlotIndexGetInteger |
| PLOT_SHIFT | Shift of indicator plotting along the time axis in bars | PlotIndexSetInteger ,  PlotIndexGetInteger |
| PLOT_SHOW_DATA | Sign of display of construction values in the DataWindow | PlotIndexSetInteger ,  PlotIndexGetInteger |
| PLUSDI_LINE | Line +DI | Indicators Lines |
| POINTER_AUTOMATIC | Pointer of any objects created automatically (not using new()) | CheckPointer |
| POINTER_DYNAMIC | Pointer of the object created by the  new()  operator | CheckPointer |
| POINTER_INVALID | Incorrect pointer | CheckPointer |
| POSITION_COMMENT | Position comment | PositionGetString |
| POSITION_COMMISSION | Commission | PositionGetDouble |
| POSITION_IDENTIFIER | Position identifier is a unique number that is assigned to every newly opened position and doesn't change during the entire lifetime of the position. Position turnover doesn't change its identifier. | PositionGetInteger |
| POSITION_MAGIC | Position magic number (see  ORDER_MAGIC ) | PositionGetInteger |
| POSITION_PRICE_CURRENT | Current price of the position symbol | PositionGetDouble |
| POSITION_PRICE_OPEN | Position open price | PositionGetDouble |
| POSITION_PROFIT | Current profit | PositionGetDouble |
| POSITION_SL | Stop Loss level of opened position | PositionGetDouble |
| POSITION_SWAP | Cumulative swap | PositionGetDouble |
| POSITION_SYMBOL | Symbol of the position | PositionGetString |
| POSITION_TIME | Position open time | PositionGetInteger |
| POSITION_TIME_MSC | Position opening time in milliseconds since 01.01.1970 | PositionGetInteger |
| POSITION_TIME_UPDATE | Position changing time in seconds since 01.01.1970 | PositionGetInteger |
| POSITION_TIME_UPDATE_MSC | Position changing time in milliseconds since 01.01.1970 | PositionGetInteger |
| POSITION_TP | Take Profit level of opened position | PositionGetDouble |
| POSITION_TYPE | Position type | PositionGetInteger |
| POSITION_TYPE_BUY | Buy | PositionGetInteger |
| POSITION_TYPE_SELL | Sell | PositionGetInteger |
| POSITION_VOLUME | Position volume | PositionGetDouble |
| PRICE_CLOSE | Close price | Price Constants |
| PRICE_HIGH | The maximum price for the period | Price Constants |
| PRICE_LOW | The minimum price for the period | Price Constants |
| PRICE_MEDIAN | Median price, (high + low)/2 | Price Constants |
| PRICE_OPEN | Open price | Price Constants |
| PRICE_TYPICAL | Typical price, (high + low + close)/3 | Price Constants |
| PRICE_WEIGHTED | Average price, (high + low + close + close)/4 | Price Constants |
| PROGRAM_EXPERT | Expert | MQLInfoInteger |
| PROGRAM_INDICATOR | Indicator | MQLInfoInteger |
| PROGRAM_SCRIPT | Script | MQLInfoInteger |
| REASON_ACCOUNT | Another account has been activated or reconnection to the trade server has occurred due to changes in the account settings | UninitializeReason ,  OnDeinit |
| REASON_CHARTCHANGE | Symbol or chart period has been changed | UninitializeReason ,  OnDeinit |
| REASON_CHARTCLOSE | Chart has been closed | UninitializeReason ,  OnDeinit |
| REASON_CLOSE | Terminal has been closed | UninitializeReason ,  OnDeinit |
| REASON_INITFAILED | This value means that  OnInit()  handler has returned a nonzero value | UninitializeReason ,  OnDeinit |
| REASON_PARAMETERS | Input parameters have been changed by a user | UninitializeReason ,  OnDeinit |
| REASON_PROGRAM | Expert Advisor terminated its operation by calling the  ExpertRemove()  function | UninitializeReason ,  OnDeinit |
| REASON_RECOMPILE | Program has been recompiled | UninitializeReason ,  OnDeinit |
| REASON_REMOVE | Program has been deleted from the chart | UninitializeReason ,  OnDeinit |
| REASON_TEMPLATE | A new template has been applied | UninitializeReason ,  OnDeinit |
| SATURDAY | Saturday | SymbolInfoInteger ,  SymbolInfoSessionQuote ,  SymbolInfoSessionTrade |
| SEEK_CUR | Current position of a file pointer | FileSeek |
| SEEK_END | File end | FileSeek |
| SEEK_SET | File beginning | FileSeek |
| SENKOUSPANA_LINE | Senkou Span A line | Indicators Lines |
| SENKOUSPANB_LINE | Senkou Span B line | Indicators Lines |
| SERIES_BARS_COUNT | Bars count for the symbol-period for the current moment | SeriesInfoInteger |
| SERIES_FIRSTDATE | The very first date for the symbol-period for the current moment | SeriesInfoInteger |
| SERIES_LASTBAR_DATE | Open time of the last bar of the symbol-period | SeriesInfoInteger |
| SERIES_SERVER_FIRSTDATE | The very first date in the history of the symbol on the server regardless of the timeframe | SeriesInfoInteger |
| SERIES_SYNCHRONIZED | Symbol/period data synchronization flag for the current moment | SeriesInfoInteger |
| SERIES_TERMINAL_FIRSTDATE | The very first date in the history of the symbol in the client terminal, regardless of the timeframe | SeriesInfoInteger |
| SHORT_MAX | Maximal value, which can be represented by short type | Numerical Type Constants |
| SHORT_MIN | Minimal value, which can be represented by short type | Numerical Type Constants |
| SIGNAL_BASE_AUTHOR_LOGIN | Author login | SignalBaseGetString |
| SIGNAL_BASE_BALANCE | Account balance | SignalBaseGetDouble |
| SIGNAL_BASE_BROKER | Broker name (company) | SignalBaseGetString |
| SIGNAL_BASE_BROKER_SERVER | Broker server | SignalBaseGetString |
| SIGNAL_BASE_CURRENCY | Signal base currency | SignalBaseGetString |
| SIGNAL_BASE_DATE_PUBLISHED | Publication date (date when it become available for subscription) | SignalBaseGetInteger |
| SIGNAL_BASE_DATE_STARTED | Monitoring starting date | SignalBaseGetInteger |
| SIGNAL_BASE_EQUITY | Account equity | SignalBaseGetDouble |
| SIGNAL_BASE_GAIN | Account gain | SignalBaseGetDouble |
| SIGNAL_BASE_ID | Signal ID | SignalBaseGetInteger |
| SIGNAL_BASE_LEVERAGE | Account leverage | SignalBaseGetInteger |
| SIGNAL_BASE_MAX_DRAWDOWN | Account maximum drawdown | SignalBaseGetDouble |
| SIGNAL_BASE_NAME | Signal name | SignalBaseGetString |
| SIGNAL_BASE_PIPS | Profit in pips | SignalBaseGetInteger |
| SIGNAL_BASE_PRICE | Signal subscription price | SignalBaseGetDouble |
| SIGNAL_BASE_RATING | Position in rating | SignalBaseGetInteger |
| SIGNAL_BASE_ROI | Return on Investment (%) | SignalBaseGetDouble |
| SIGNAL_BASE_SUBSCRIBERS | Number of subscribers | SignalBaseGetInteger |
| SIGNAL_BASE_TRADE_MODE | Account type (0-real, 1-demo, 2-contest) | SignalBaseGetInteger |
| SIGNAL_BASE_TRADES | Number of trades | SignalBaseGetInteger |
| SIGNAL_INFO_CONFIRMATIONS_DISABLED | The flag enables synchronization without confirmation dialog | SignalInfoGetInteger ,  SignalInfoSetInteger |
| SIGNAL_INFO_COPY_SLTP | Copy Stop Loss and Take Profit flag | SignalInfoGetInteger ,  SignalInfoSetInteger |
| SIGNAL_INFO_DEPOSIT_PERCENT | Deposit percent (%) | SignalInfoGetInteger ,  SignalInfoSetInteger |
| SIGNAL_INFO_EQUITY_LIMIT | Equity limit | SignalInfoGetDouble ,  SignalInfoSetDouble |
| SIGNAL_INFO_ID | Signal id, r/o | SignalInfoGetInteger ,  SignalInfoSetInteger |
| SIGNAL_INFO_NAME | Signal name, r/o | SignalInfoGetString |
| SIGNAL_INFO_SLIPPAGE | Slippage (used when placing market orders in synchronization of positions and copying of trades) | SignalInfoGetDouble ,  SignalInfoSetDouble |
| SIGNAL_INFO_SUBSCRIPTION_ENABLED | "Copy trades by subscription" permission flag | SignalInfoGetInteger ,  SignalInfoSetInteger |
| SIGNAL_INFO_TERMS_AGREE | "Agree to terms of use of Signals service" flag, r/o | SignalInfoGetInteger ,  SignalInfoSetInteger |
| SIGNAL_INFO_VOLUME_PERCENT | Maximum percent of deposit used (%), r/o | SignalInfoGetDouble ,  SignalInfoSetDouble |
| SIGNAL_LINE | Signal line | Indicators Lines |
| STAT_BALANCE_DD | Maximum balance drawdown in monetary terms. In the process of trading, a balance may have numerous drawdowns; here the largest value is taken | TesterStatistics |
| STAT_BALANCE_DD_RELATIVE | Balance drawdown in monetary terms that was recorded at the moment of the maximum balance drawdown as a percentage (STAT_BALANCE_DDREL_PERCENT). | TesterStatistics |
| STAT_BALANCE_DDREL_PERCENT | Maximum balance drawdown as a percentage. In the process of trading, a balance may have numerous drawdowns, for each of which the relative drawdown value in percents is calculated. The greatest value is returned | TesterStatistics |
| STAT_BALANCEDD_PERCENT | Balance drawdown as a percentage that was recorded at the moment of the maximum balance drawdown in monetary terms (STAT_BALANCE_DD). | TesterStatistics |
| STAT_BALANCEMIN | Minimum balance value | TesterStatistics |
| STAT_CONLOSSMAX | Maximum loss in a series of losing trades. The value is less than or equal to zero | TesterStatistics |
| STAT_CONLOSSMAX_TRADES | The number of trades that have formed STAT_CONLOSSMAX (maximum loss in a series of losing trades) | TesterStatistics |
| STAT_CONPROFITMAX | Maximum profit in a series of profitable trades. The value is greater than or equal to zero | TesterStatistics |
| STAT_CONPROFITMAX_TRADES | The number of trades that have formed STAT_CONPROFITMAX (maximum profit in a series of profitable trades) | TesterStatistics |
| STAT_CUSTOM_ONTESTER | The value of the calculated custom optimization criterion returned by the  OnTester()  function | TesterStatistics |
| STAT_DEALS | The number of deals | TesterStatistics |
| STAT_EQUITY_DD | Maximum equity drawdown in monetary terms. In the process of trading, numerous drawdowns may appear on the equity; here the largest value is taken | TesterStatistics |
| STAT_EQUITY_DD_RELATIVE | Equity drawdown in monetary terms that was recorded at the moment of the maximum equity drawdown in percent (STAT_EQUITY_DDREL_PERCENT). | TesterStatistics |
| STAT_EQUITY_DDREL_PERCENT | Maximum equity drawdown as a percentage. In the process of trading, an equity may have numerous drawdowns, for each of which the relative drawdown value in percents is calculated. The greatest value is returned | TesterStatistics |
| STAT_EQUITYDD_PERCENT | Drawdown in percent that was recorded at the moment of the maximum equity drawdown in monetary terms (STAT_EQUITY_DD). | TesterStatistics |
| STAT_EQUITYMIN | Minimum equity value | TesterStatistics |
| STAT_EXPECTED_PAYOFF | Expected payoff | TesterStatistics |
| STAT_GROSS_LOSS | Total loss, the sum of all negative trades. The value is less than or equal to zero | TesterStatistics |
| STAT_GROSS_PROFIT | Total profit, the sum of all profitable (positive) trades. The value is greater than or equal to zero | TesterStatistics |
| STAT_INITIAL_DEPOSIT | The value of the initial deposit | TesterStatistics |
| STAT_LONG_TRADES | Long trades | TesterStatistics |
| STAT_LOSS_TRADES | Losing trades | TesterStatistics |
| STAT_LOSSTRADES_AVGCON | Average length of a losing series of trades | TesterStatistics |
| STAT_MAX_CONLOSS_TRADES | The number of trades in the longest series of losing trades STAT_MAX_CONLOSSES | TesterStatistics |
| STAT_MAX_CONLOSSES | The total loss of the longest series of losing trades | TesterStatistics |
| STAT_MAX_CONPROFIT_TRADES | The number of trades in the longest series of profitable trades STAT_MAX_CONWINS | TesterStatistics |
| STAT_MAX_CONWINS | The total profit of the longest series of profitable trades | TesterStatistics |
| STAT_MAX_LOSSTRADE | Maximum loss – the lowest value of all losing trades. The value is less than or equal to zero | TesterStatistics |
| STAT_MAX_PROFITTRADE | Maximum profit – the largest value of all profitable trades. The value is greater than or equal to zero | TesterStatistics |
| STAT_MIN_MARGINLEVEL | Minimum value of the margin level | TesterStatistics |
| STAT_PROFIT | Net profit after testing, the sum of STAT_GROSS_PROFIT and STAT_GROSS_LOSS (STAT_GROSS_LOSS is always less than or equal to zero) | TesterStatistics |
| STAT_PROFIT_FACTOR | Profit factor, equal to  the ratio of STAT_GROSS_PROFIT/STAT_GROSS_LOSS. If STAT_GROSS_LOSS=0, the profit factor is equal to  DBL_MAX | TesterStatistics |
| STAT_PROFIT_LONGTRADES | Profitable long trades | TesterStatistics |
| STAT_PROFIT_SHORTTRADES | Profitable short trades | TesterStatistics |
| STAT_PROFIT_TRADES | Profitable trades | TesterStatistics |
| STAT_PROFITTRADES_AVGCON | Average length of a profitable series of trades | TesterStatistics |
| STAT_RECOVERY_FACTOR | Recovery factor, equal to the ratio of STAT_PROFIT/STAT_BALANCE_DD | TesterStatistics |
| STAT_SHARPE_RATIO | Sharpe ratio | TesterStatistics |
| STAT_SHORT_TRADES | Short trades | TesterStatistics |
| STAT_TRADES | The number of trades | TesterStatistics |
| STAT_WITHDRAWAL | Money withdrawn from an account | TesterStatistics |
| STO_CLOSECLOSE | Calculation is based on Close/Close prices | Price Constants |
| STO_LOWHIGH | Calculation is based on Low/High prices | Price Constants |
| STYLE_DASH | Broken line | Drawing Styles |
| STYLE_DASHDOT | Dash-dot line | Drawing Styles |
| STYLE_DASHDOTDOT | Dash - two points | Drawing Styles |
| STYLE_DOT | Dotted line | Drawing Styles |
| STYLE_SOLID | Solid line | Drawing Styles |
| SUNDAY | Sunday | SymbolInfoInteger ,  SymbolInfoSessionQuote ,  SymbolInfoSessionTrade |
| SYMBOL_ASK | Ask - best buy offer | SymbolInfoDouble |
| SYMBOL_ASKHIGH | Maximal Ask of the day | SymbolInfoDouble |
| SYMBOL_ASKLOW | Minimal Ask of the day | SymbolInfoDouble |
| SYMBOL_BANK | Feeder of the current quote | SymbolInfoString |
| SYMBOL_BASIS | The underlying asset of a derivative | SymbolInfoString |
| SYMBOL_BID | Bid - best sell offer | SymbolInfoDouble |
| SYMBOL_BIDHIGH | Maximal Bid of the day | SymbolInfoDouble |
| SYMBOL_BIDLOW | Minimal Bid of the day | SymbolInfoDouble |
| SYMBOL_CALC_MODE_CFD | CFD mode - calculation of margin and profit for CFD | SymbolInfoInteger |
| SYMBOL_CALC_MODE_CFDINDEX | CFD index mode - calculation of margin and profit for CFD by indexes | SymbolInfoInteger |
| SYMBOL_CALC_MODE_CFDLEVERAGE | CFD Leverage mode - calculation of margin and profit for CFD at leverage trading | SymbolInfoInteger |
| SYMBOL_CALC_MODE_EXCH_FUTURES | Futures mode –  calculation of margin and profit for trading futures contracts on a stock exchange | SymbolInfoInteger |
| SYMBOL_CALC_MODE_EXCH_FUTURES_FORTS | FORTS Futures mode –  calculation of margin and profit for trading futures contracts on FORTS. | SymbolInfoInteger |
| SYMBOL_CALC_MODE_EXCH_STOCKS | Exchange mode – calculation of margin and profit for trading securities on a stock exchange | SymbolInfoInteger |
| SYMBOL_CALC_MODE_FOREX | Forex mode - calculation of profit and margin for Forex | SymbolInfoInteger |
| SYMBOL_CALC_MODE_FUTURES | Futures mode - calculation of margin and profit for futures | SymbolInfoInteger |
| SYMBOL_CALC_MODE_SERV_COLLATERAL | Collateral mode - a symbol is used as a non-tradable asset on a trading account. | SymbolInfoInteger |
| SYMBOL_CURRENCY_BASE | Basic currency of a symbol | SymbolInfoString |
| SYMBOL_CURRENCY_MARGIN | Margin currency | SymbolInfoString |
| SYMBOL_CURRENCY_PROFIT | Profit currency | SymbolInfoString |
| SYMBOL_DESCRIPTION | Symbol description | SymbolInfoString |
| SYMBOL_DIGITS | Digits after a decimal point | SymbolInfoInteger |
| SYMBOL_EXPIRATION_DAY | The order is valid till the end of the day | SymbolInfoInteger |
| SYMBOL_EXPIRATION_GTC | The order is valid during the unlimited time period, until it is explicitly canceled | SymbolInfoInteger |
| SYMBOL_EXPIRATION_MODE | Flags of allowed order  expiration modes | SymbolInfoInteger |
| SYMBOL_EXPIRATION_SPECIFIED | The expiration time is specified in the order | SymbolInfoInteger |
| SYMBOL_EXPIRATION_SPECIFIED_DAY | The expiration date is specified in the order | SymbolInfoInteger |
| SYMBOL_EXPIRATION_TIME | Date of the symbol trade end (usually used for futures) | SymbolInfoInteger |
| SYMBOL_FILLING_FOK | This policy means that a deal can be executed only with the specified volume. If the necessary amount of a financial instrument is currently unavailable in the market, the order will not be executed. The required volume can be filled using several offers available on the market at the moment. | SymbolInfoInteger |
| SYMBOL_FILLING_IOC | In this case a trader agrees to execute a deal with the volume maximally available in the market within that indicated in the order. In case the order cannot be filled completely, the available volume of the order will be filled, and the remaining volume will be canceled. The possibility of using IOC orders is determined at the trade server. | SymbolInfoInteger |
| SYMBOL_FILLING_MODE | Flags of allowed order  filling modes | SymbolInfoInteger |
| SYMBOL_ISIN | The name of a symbol in the ISIN system (International Securities Identification Number). The International Securities Identification Number is a 12-digit alphanumeric code that uniquely identifies a security. The presence of this symbol property is determined on the side of a trade server. | SymbolInfoString |
| SYMBOL_LAST | Price of the last deal | SymbolInfoDouble |
| SYMBOL_LASTHIGH | Maximal Last of the day | SymbolInfoDouble |
| SYMBOL_LASTLOW | Minimal Last of the day | SymbolInfoDouble |
| SYMBOL_MARGIN_INITIAL | Initial margin means the amount in the margin currency required for opening a position with the volume of one lot. It is used for checking a client's assets when he or she enters the market. | SymbolInfoDouble |
| SYMBOL_MARGIN_MAINTENANCE | The maintenance margin. If it is set, it sets the margin amount in the margin currency of the symbol, charged from one lot. It is used for checking a client's assets when his/her account state changes. If the maintenance margin is equal to 0, the initial margin is used. | SymbolInfoDouble |
| SYMBOL_OPTION_MODE | Option type | SymbolInfoInteger |
| SYMBOL_OPTION_MODE_EUROPEAN | European option may only be exercised on a specified date (expiration, execution date, delivery date) | SymbolInfoInteger |
| SYMBOL_OPTION_MODE_AMERICAN | American option may be exercised on any trading day on or before expiry. The period within which a buyer can exercise the option is specified for it | SymbolInfoInteger |
| SYMBOL_OPTION_RIGHT | Option right (Call/Put) | SymbolInfoInteger |
| SYMBOL_OPTION_RIGHT_CALL | A call option gives you the right to buy an asset at a specified price | SymbolInfoInteger |
| SYMBOL_OPTION_RIGHT_PUT | A put option gives you the right to sell an asset at a specified price | SymbolInfoInteger |
| SYMBOL_OPTION_STRIKE | The strike price of an option. The price at which an option buyer can buy (in a Call option) or sell (in a Put option) the underlying asset, and the option seller is obliged to sell or buy the appropriate amount of the underlying asset. | SymbolInfoDouble |
| SYMBOL_ORDER_LIMIT | Limit orders are allowed (Buy Limit and Sell Limit) | SymbolInfoInteger |
| SYMBOL_ORDER_MARKET | Market orders are allowed (Buy and Sell) | SymbolInfoInteger |
| SYMBOL_ORDER_MODE | Flags of allowed  order types | SymbolInfoInteger |
| SYMBOL_ORDER_SL | Stop Loss is allowed | SymbolInfoInteger |
| SYMBOL_ORDER_STOP | Stop orders are allowed (Buy Stop and Sell Stop) | SymbolInfoInteger |
| SYMBOL_ORDER_STOP_LIMIT | Stop-limit orders are allowed (Buy Stop Limit and Sell Stop Limit) | SymbolInfoInteger |
| SYMBOL_ORDER_TP | Take Profit is allowed | SymbolInfoInteger |
| SYMBOL_PATH | Path in the symbol tree | SymbolInfoString |
| SYMBOL_POINT | Symbol point value | SymbolInfoDouble |
| SYMBOL_SELECT | Symbol is selected in Market Watch | SymbolInfoInteger |
| SYMBOL_SESSION_AW | Average weighted price of the current session | SymbolInfoDouble |
| SYMBOL_SESSION_BUY_ORDERS | Number of Buy orders at the moment | SymbolInfoInteger |
| SYMBOL_SESSION_BUY_ORDERS_VOLUME | Current volume of Buy orders | SymbolInfoDouble |
| SYMBOL_SESSION_CLOSE | Close price of the current session | SymbolInfoDouble |
| SYMBOL_SESSION_DEALS | Number of deals in the current session | SymbolInfoInteger |
| SYMBOL_SESSION_INTEREST | Summary open interest | SymbolInfoDouble |
| SYMBOL_SESSION_OPEN | Open price of the current session | SymbolInfoDouble |
| SYMBOL_SESSION_PRICE_LIMIT_MAX | Maximal price of the current session | SymbolInfoDouble |
| SYMBOL_SESSION_PRICE_LIMIT_MIN | Minimal price of the current session | SymbolInfoDouble |
| SYMBOL_SESSION_PRICE_SETTLEMENT | Settlement price of the current session | SymbolInfoDouble |
| SYMBOL_SESSION_SELL_ORDERS | Number of Sell orders at the moment | SymbolInfoInteger |
| SYMBOL_SESSION_SELL_ORDERS_VOLUME | Current volume of Sell orders | SymbolInfoDouble |
| SYMBOL_SESSION_TURNOVER | Summary turnover of the current session | SymbolInfoDouble |
| SYMBOL_SESSION_VOLUME | Summary volume of current session deals | SymbolInfoDouble |
| SYMBOL_SPREAD | Spread value in points | SymbolInfoInteger |
| SYMBOL_SPREAD_FLOAT | Indication of a floating spread | SymbolInfoInteger |
| SYMBOL_START_TIME | Date of the symbol trade beginning (usually used for futures) | SymbolInfoInteger |
| SYMBOL_SWAP_LONG | Long swap value | SymbolInfoDouble |
| SYMBOL_SWAP_MODE | Swap calculation model | SymbolInfoInteger |
| SYMBOL_SWAP_MODE_CURRENCY_DEPOSIT | Swaps are charged in money, in client deposit currency | SymbolInfoInteger |
| SYMBOL_SWAP_MODE_CURRENCY_MARGIN | Swaps are charged in money in margin currency of the symbol | SymbolInfoInteger |
| SYMBOL_SWAP_MODE_CURRENCY_SYMBOL | Swaps are charged in money in base currency of the symbol | SymbolInfoInteger |
| SYMBOL_SWAP_MODE_DISABLED | Swaps disabled (no swaps) | SymbolInfoInteger |
| SYMBOL_SWAP_MODE_INTEREST_CURRENT | Swaps are charged as the specified annual interest from the instrument price at calculation of swap (standard bank year is 360 days) | SymbolInfoInteger |
| SYMBOL_SWAP_MODE_INTEREST_OPEN | Swaps are charged as the specified annual interest from the open price of position (standard bank year is 360 days) | SymbolInfoInteger |
| SYMBOL_SWAP_MODE_POINTS | Swaps are charged in points | SymbolInfoInteger |
| SYMBOL_SWAP_MODE_REOPEN_BID | Swaps are charged by reopening positions. At the end of a trading day the position is closed. Next day it is reopened by the current Bid price +/- specified number of points (parameters SYMBOL_SWAP_LONG and SYMBOL_SWAP_SHORT) | SymbolInfoInteger |
| SYMBOL_SWAP_MODE_REOPEN_CURRENT | Swaps are charged by reopening positions. At the end of a trading day the position is closed. Next day it is reopened by the close price +/- specified number of points (parameters SYMBOL_SWAP_LONG and SYMBOL_SWAP_SHORT) | SymbolInfoInteger |
| SYMBOL_SWAP_ROLLOVER3DAYS | Day of week to charge 3 days swap rollover | SymbolInfoInteger |
| SYMBOL_SWAP_SHORT | Short swap value | SymbolInfoDouble |
| SYMBOL_TICKS_BOOKDEPTH | Maximal number of requests shown in  Depth of Market . For symbols that have no queue of requests, the value is equal to zero. | SymbolInfoInteger |
| SYMBOL_TIME | Time of the last quote | SymbolInfoInteger |
| SYMBOL_TRADE_CALC_MODE | Contract price calculation mode | SymbolInfoInteger |
| SYMBOL_TRADE_CONTRACT_SIZE | Trade contract size | SymbolInfoDouble |
| SYMBOL_TRADE_EXECUTION_EXCHANGE | Exchange execution | SymbolInfoInteger |
| SYMBOL_TRADE_EXECUTION_INSTANT | Instant execution | SymbolInfoInteger |
| SYMBOL_TRADE_EXECUTION_MARKET | Market execution | SymbolInfoInteger |
| SYMBOL_TRADE_EXECUTION_REQUEST | Execution by request | SymbolInfoInteger |
| SYMBOL_TRADE_EXEMODE | Deal execution mode | SymbolInfoInteger |
| SYMBOL_TRADE_FREEZE_LEVEL | Distance to freeze trade operations in points | SymbolInfoInteger |
| SYMBOL_TRADE_MODE | Order execution type | SymbolInfoInteger |
| SYMBOL_TRADE_MODE_CLOSEONLY | Allowed only position close operations | SymbolInfoInteger |
| SYMBOL_TRADE_MODE_DISABLED | Trade is disabled for the symbol | SymbolInfoInteger |
| SYMBOL_TRADE_MODE_FULL | No trade restrictions | SymbolInfoInteger |
| SYMBOL_TRADE_MODE_LONGONLY | Allowed only long positions | SymbolInfoInteger |
| SYMBOL_TRADE_MODE_SHORTONLY | Allowed only short positions | SymbolInfoInteger |
| SYMBOL_TRADE_STOPS_LEVEL | Minimal indention in points from the current close price to place Stop orders | SymbolInfoInteger |
| SYMBOL_TRADE_TICK_SIZE | Minimal price change | SymbolInfoDouble |
| SYMBOL_TRADE_TICK_VALUE | Value of SYMBOL_TRADE_TICK_VALUE_PROFIT | SymbolInfoDouble |
| SYMBOL_TRADE_TICK_VALUE_LOSS | Calculated tick price for a losing position | SymbolInfoDouble |
| SYMBOL_TRADE_TICK_VALUE_PROFIT | Calculated tick price for a profitable position | SymbolInfoDouble |
| SYMBOL_VOLUME | Volume of the last deal | SymbolInfoInteger |
| SYMBOL_VOLUME_LIMIT | Maximum allowed aggregate volume of an open position and pending orders in one direction (buy or sell) for the symbol. For example, with the limitation of 5 lots, you can have an open buy position with the volume of 5 lots and place a pending order Sell Limit with the volume of 5 lots. But in this case you cannot place a Buy Limit pending order (since the total volume in one direction will exceed the limitation) or place Sell Limit with the volume more than 5 lots. | SymbolInfoDouble |
| SYMBOL_VOLUME_MAX | Maximal volume for a deal | SymbolInfoDouble |
| SYMBOL_VOLUME_MIN | Minimal volume for a deal | SymbolInfoDouble |
| SYMBOL_VOLUME_STEP | Minimal volume change step for deal execution | SymbolInfoDouble |
| SYMBOL_VOLUMEHIGH | Maximal day volume | SymbolInfoInteger |
| SYMBOL_VOLUMELOW | Minimal day volume | SymbolInfoInteger |
| TENKANSEN_LINE | Tenkan-sen line | Indicators Lines |
| TERMINAL_BUILD | The client terminal build number | TerminalInfoInteger |
| TERMINAL_CODEPAGE | Number of  the code page of the language  installed in the client terminal | TerminalInfoInteger |
| TERMINAL_COMMONDATA_PATH | Common path for all of the terminals installed on a computer | TerminalInfoString |
| TERMINAL_COMMUNITY_ACCOUNT | The flag indicates the presence of MQL5.community authorization data in the terminal | TerminalInfoInteger |
| TERMINAL_COMMUNITY_BALANCE | Balance in MQL5.community | TerminalInfoDouble |
| TERMINAL_COMMUNITY_CONNECTION | Connection to MQL5.community | TerminalInfoInteger |
| TERMINAL_COMPANY | Company name | TerminalInfoString |
| TERMINAL_CONNECTED | Connection to a trade server | TerminalInfoInteger |
| TERMINAL_CPU_CORES | The number of CPU cores in the system | TerminalInfoInteger |
| TERMINAL_DATA_PATH | Folder in which terminal data are stored | TerminalInfoString |
| TERMINAL_DISK_SPACE | Free disk space for the MQL5\Files folder of the terminal (agent), MB | TerminalInfoInteger |
| TERMINAL_DLLS_ALLOWED | Permission to use DLL | TerminalInfoInteger |
| TERMINAL_EMAIL_ENABLED | Permission to send e-mails using SMTP-server and login, specified in the terminal settings | TerminalInfoInteger |
| TERMINAL_FTP_ENABLED | Permission to send reports using FTP-server and login, specified in the terminal settings | TerminalInfoInteger |
| TERMINAL_LANGUAGE | Language of the terminal | TerminalInfoString |
| TERMINAL_MAXBARS | The maximal bars count on the chart | TerminalInfoInteger |
| TERMINAL_MEMORY_AVAILABLE | Free memory of the terminal (agent) process, MB | TerminalInfoInteger |
| TERMINAL_MEMORY_PHYSICAL | Physical memory in the system, MB | TerminalInfoInteger |
| TERMINAL_MEMORY_TOTAL | Memory available to the process of the terminal (agent), MB | TerminalInfoInteger |
| TERMINAL_MEMORY_USED | Memory used by the terminal (agent), MB | TerminalInfoInteger |
| TERMINAL_MQID | The flag indicates the presence of MetaQuotes ID data for  Push notifications | TerminalInfoInteger |
| TERMINAL_NAME | Terminal name | TerminalInfoString |
| TERMINAL_NOTIFICATIONS_ENABLED | Permission to send notifications to smartphone | TerminalInfoInteger |
| TERMINAL_OPENCL_SUPPORT | The version of the supported OpenCL in the format of 0x00010002 = 1.2.  "0" means that OpenCL is not supported | TerminalInfoInteger |
| TERMINAL_PATH | Folder from which the terminal is started | TerminalInfoString |
| TERMINAL_PING_LAST | The last known value of a ping to a trade server in microseconds. One second comprises of one million microseconds | TerminalInfoInteger |
| TERMINAL_SCREEN_DPI | The resolution of information display on the screen is measured as number of Dots in a line per Inch (DPI). | TerminalInfoInteger |
| TERMINAL_TRADE_ALLOWED | Permission to trade | TerminalInfoInteger |
| TERMINAL_X64 | Indication of the "64-bit terminal" | TerminalInfoInteger |
| THURSDAY | Thursday | SymbolInfoInteger ,  SymbolInfoSessionQuote ,  SymbolInfoSessionTrade |
| TRADE_ACTION_DEAL | Place a trade order for an immediate execution with the specified parameters (market order) | MqlTradeRequest |
| TRADE_ACTION_MODIFY | Modify the parameters of the order placed previously | MqlTradeRequest |
| TRADE_ACTION_PENDING | Place a trade order for the execution under specified conditions (pending order) | MqlTradeRequest |
| TRADE_ACTION_REMOVE | Delete the pending order placed previously | MqlTradeRequest |
| TRADE_ACTION_SLTP | Modify Stop Loss and Take Profit values of an opened position | MqlTradeRequest |
| TRADE_RETCODE_CANCEL | Request canceled by trader | MqlTradeResult |
| TRADE_RETCODE_CLIENT_DISABLES_AT | Autotrading disabled by client terminal | MqlTradeResult |
| TRADE_RETCODE_CONNECTION | No connection with the trade server | MqlTradeResult |
| TRADE_RETCODE_DONE | Request completed | MqlTradeResult |
| TRADE_RETCODE_DONE_PARTIAL | Only part of the request was completed | MqlTradeResult |
| TRADE_RETCODE_ERROR | Request processing error | MqlTradeResult |
| TRADE_RETCODE_FROZEN | Order or position frozen | MqlTradeResult |
| TRADE_RETCODE_INVALID | Invalid request | MqlTradeResult |
| TRADE_RETCODE_INVALID_EXPIRATION | Invalid order expiration date in the request | MqlTradeResult |
| TRADE_RETCODE_INVALID_FILL | Invalid  order filling type | MqlTradeResult |
| TRADE_RETCODE_INVALID_ORDER | Incorrect or prohibited  order type | MqlTradeResult |
| TRADE_RETCODE_INVALID_PRICE | Invalid price in the request | MqlTradeResult |
| TRADE_RETCODE_INVALID_STOPS | Invalid stops in the request | MqlTradeResult |
| TRADE_RETCODE_INVALID_VOLUME | Invalid volume in the request | MqlTradeResult |
| TRADE_RETCODE_LIMIT_ORDERS | The number of pending orders has reached the limit | MqlTradeResult |
| TRADE_RETCODE_LIMIT_VOLUME | The volume of orders and positions for the symbol has reached the limit | MqlTradeResult |
| TRADE_RETCODE_LOCKED | Request locked for processing | MqlTradeResult |
| TRADE_RETCODE_MARKET_CLOSED | Market is closed | MqlTradeResult |
| TRADE_RETCODE_NO_CHANGES | No changes in request | MqlTradeResult |
| TRADE_RETCODE_NO_MONEY | There is not enough money to complete the request | MqlTradeResult |
| TRADE_RETCODE_ONLY_REAL | Operation is allowed only for live accounts | MqlTradeResult |
| TRADE_RETCODE_ORDER_CHANGED | Order state changed | MqlTradeResult |
| TRADE_RETCODE_PLACED | Order placed | MqlTradeResult |
| TRADE_RETCODE_POSITION_CLOSED | Position with the specified  POSITION_IDENTIFIER  has already been closed | MqlTradeResult |
| TRADE_RETCODE_PRICE_CHANGED | Prices changed | MqlTradeResult |
| TRADE_RETCODE_PRICE_OFF | There are no quotes to process the request | MqlTradeResult |
| TRADE_RETCODE_REJECT | Request rejected | MqlTradeResult |
| TRADE_RETCODE_REQUOTE | Requote | MqlTradeResult |
| TRADE_RETCODE_SERVER_DISABLES_AT | Autotrading disabled by server | MqlTradeResult |
| TRADE_RETCODE_TIMEOUT | Request canceled by timeout | MqlTradeResult |
| TRADE_RETCODE_TOO_MANY_REQUESTS | Too frequent requests | MqlTradeResult |
| TRADE_RETCODE_TRADE_DISABLED | Trade is disabled | MqlTradeResult |
| TRADE_TRANSACTION_DEAL_ADD | Adding a deal to the history. The action is performed as a result of an order execution or performing operations with an account balance. | MqlTradeTransaction |
| TRADE_TRANSACTION_DEAL_DELETE | Deleting a deal from the history. There may be cases when a previously executed deal is deleted from a server. For example, a deal has been deleted in an external trading system (exchange) where it was previously transferred by a broker. | MqlTradeTransaction |
| TRADE_TRANSACTION_DEAL_UPDATE | Updating a deal in the history. There may be cases when a previously executed deal is changed on a server. For example, a deal has been changed in an external trading system (exchange) where it was previously transferred by a broker. | MqlTradeTransaction |
| TRADE_TRANSACTION_HISTORY_ADD | Adding an order to the history as a result of execution or cancellation. | MqlTradeTransaction |
| TRADE_TRANSACTION_HISTORY_DELETE | Deleting an order from the orders history. This type is provided for enhancing functionality on a trade server side. | MqlTradeTransaction |
| TRADE_TRANSACTION_HISTORY_UPDATE | Changing an order located in the orders history. This type is provided for enhancing functionality on a trade server side. | MqlTradeTransaction |
| TRADE_TRANSACTION_ORDER_ADD | Adding a new open order. | MqlTradeTransaction |
| TRADE_TRANSACTION_ORDER_DELETE | Removing an order from the list of the open ones. An order can be deleted from the open ones as a result of setting an appropriate request or execution (filling) and moving to the history. | MqlTradeTransaction |
| TRADE_TRANSACTION_ORDER_UPDATE | Updating an open order. The updates include not only evident changes from the client terminal or a trade server sides but also changes of an order state when setting it (for example, transition from  ORDER_STATE_STARTED  to  ORDER_STATE_PLACED  or from  ORDER_STATE_PLACED  to  ORDER_STATE_PARTIAL , etc.). | MqlTradeTransaction |
| TRADE_TRANSACTION_POSITION | Changing a position not related to a deal execution. This type of transaction shows that a position has been changed on a trade server side. Position volume, open price, Stop Loss and Take Profit levels can be changed. Data on changes are submitted in  MqlTradeTransaction  structure via OnTradeTransaction handler. Position change (adding, changing or closing), as a result of a deal execution, does not lead to the occurrence of TRADE_TRANSACTION_POSITION transaction. | MqlTradeTransaction |
| TRADE_TRANSACTION_REQUEST | Notification of the fact that a trade request has been processed by a server and processing result has been received. Only type field (trade transaction type) must be analyzed for such transactions in  MqlTradeTransaction  structure. The second and third parameters of  OnTradeTransaction  (request and result) must be analyzed for additional data. | MqlTradeTransaction |
| TUESDAY | Tuesday | SymbolInfoInteger ,  SymbolInfoSessionQuote ,  SymbolInfoSessionTrade |
| TYPE_BOOL | bool | MqlParam |
| TYPE_CHAR | char | MqlParam |
| TYPE_COLOR | color | MqlParam |
| TYPE_DATETIME | datetime | MqlParam |
| TYPE_DOUBLE | double | MqlParam |
| TYPE_FLOAT | float | MqlParam |
| TYPE_INT | int | MqlParam |
| TYPE_LONG | long | MqlParam |
| TYPE_SHORT | short | MqlParam |
| TYPE_STRING | string | MqlParam |
| TYPE_UCHAR | uchar | MqlParam |
| TYPE_UINT | uint | MqlParam |
| TYPE_ULONG | ulong | MqlParam |
| TYPE_USHORT | ushort | MqlParam |
| UCHAR_MAX | Maximal value, which can be represented by uchar type | Numerical Type Constants |
| UINT_MAX | Maximal value, which can be represented by uint type | Numerical Type Constants |
| ULONG_MAX | Maximal value, which can be represented by ulong type | Numerical Type Constants |
| UPPER_BAND | Upper limit | Indicators Lines |
| UPPER_HISTOGRAM | Upper histogram | Indicators Lines |
| UPPER_LINE | Upper line | Indicators Lines |
| USHORT_MAX | Maximal value, which can be represented by ushort type | Numerical Type Constants |
| VOLUME_REAL | Trade volume | Price Constants |
| VOLUME_TICK | Tick volume | Price Constants |
| WEDNESDAY | Wednesday | SymbolInfoInteger ,  SymbolInfoSessionQuote ,  SymbolInfoSessionTrade |
| WHOLE_ARRAY | Means the number of items remaining until the end of the array, i.e., the entire array will be processed | Other Constants |
| WRONG_VALUE | The constant can be implicitly  cast  to any  enumeration  type | Other Constants |
