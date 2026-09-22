<!-- source: https://www.tradingview.com/pine-script-reference/v6/ | fetched 2026-09-23 | examples omitted -->

<!-- anchor: fun_color.new -->
Function color applies the specified transparency to the given color.

#### Syntax & Overloads

color.new(color, transp) → const color

color.new(color, transp) → input color

color.new(color, transp) → simple color

color.new(color, transp) → series color

#### Arguments

**color (const color) **Color to apply transparency to.

**transp (const int/float) **Possible values are from 0 (not transparent) to 100 (invisible).

#### Returns

Color with specified transparency.

#### Remarks

Using arguments that are not constants (e.g., 'simple', 'input' or 'series') will have an impact on the colors displayed in the script's "Settings/Style" tab. See the User Manual for more information.

<!-- anchor: fun_nz -->
Replaces na (undefined) values with either a type-specific default value or a specified replacement.

#### Syntax & Overloads

nz(source, replacement) → simple color

nz(source, replacement) → simple int

nz(source, replacement) → series color

nz(source, replacement) → series int

nz(source, replacement) → simple float

nz(source, replacement) → series float

#### Arguments

**source (simple color) **The source series to process.

**replacement (simple color) **Optional. The value the function uses to replace na values in the `source` series. The default depends on the `source` type: `0` for "int", `0.0` for "float", or `#00000000` for "color".

#### Returns

The value of `source` if it is not `na`. If the value of `source` is `na`, returns zero, or the `replacement` argument when one is used.

#### See also

nana()fixnan()

<!-- anchor: fun_alertcondition -->
Creates alert condition, that is available in Create Alert dialog. Please note, that alertcondition() does NOT create an alert, it just gives you more options in Create Alert dialog. Also, alertcondition() effect is invisible on chart.

#### Syntax

```
alertcondition(condition, title, message) → void
```

#### Arguments

**condition (series bool) **Series of boolean values that is used for alert. True values mean alert fire, false - no alert. Required argument.

**title (const string) **Title of the alert condition. Optional argument.

**message (const string) **Message to display when alert fires. Optional argument.

#### Remarks

Please note that an alertcondition call generates an additional plot. All such calls are taken into account when we calculate the number of the output series per script.

#### See also

alert()

<!-- anchor: fun_math.abs -->
Absolute value of `number` is `number` if `number` >= 0, or -`number` otherwise.

#### Syntax & Overloads

math.abs(number) → const int

math.abs(number) → input int

math.abs(number) → const float

math.abs(number) → simple int

math.abs(number) → input float

math.abs(number) → series int

math.abs(number) → simple float

math.abs(number) → series float

#### Arguments

**number (const int) **The number to use in the calculation.

#### Returns

The absolute value of `number`.

<!-- anchor: fun_math.max -->
Returns the greatest of multiple values.

#### Syntax & Overloads

math.max(number0, number1, ...) → const int

math.max(number0, number1, ...) → const float

math.max(number0, number1, ...) → input int

math.max(number0, number1, ...) → simple int

math.max(number0, number1, ...) → input float

math.max(number0, number1, ...) → series int

math.max(number0, number1, ...) → simple float

math.max(number0, number1, ...) → series float

#### Arguments

**number0, number1, ... (const int) **A sequence of numbers to use in the calculation.

#### Returns

The greatest of multiple given values.

#### See also

math.min()

<!-- anchor: fun_math.min -->
Returns the smallest of multiple values.

#### Syntax & Overloads

math.min(number0, number1, ...) → const int

math.min(number0, number1, ...) → const float

math.min(number0, number1, ...) → input int

math.min(number0, number1, ...) → simple int

math.min(number0, number1, ...) → input float

math.min(number0, number1, ...) → series int

math.min(number0, number1, ...) → simple float

math.min(number0, number1, ...) → series float

#### Arguments

**number0, number1, ... (const int) **A sequence of numbers to use in the calculation.

#### Returns

The smallest of multiple given values.

#### See also

math.max()

<!-- anchor: fun_math.pow -->
Mathematical power function.

#### Syntax & Overloads

math.pow(base, exponent) → const float

math.pow(base, exponent) → input float

math.pow(base, exponent) → simple float

math.pow(base, exponent) → series float

#### Arguments

**base (const int/float) **Specify the base to use.

**exponent (const int/float) **Specifies the exponent.

#### Returns

`base` raised to the power of `exponent`. If `base` is a series, it is calculated elementwise.

#### See also

math.sqrt()math.exp()

<!-- anchor: fun_math.round -->
Returns the value of `number` rounded to the nearest integer, with ties rounding up. If the `precision` parameter is used, returns a float value rounded to that amount of decimal places.

#### Syntax & Overloads

math.round(number) → const int

math.round(number) → input int

math.round(number) → simple int

math.round(number) → series int

math.round(number, precision) → const float

math.round(number, precision) → input float

math.round(number, precision) → simple float

math.round(number, precision) → series float

#### Arguments

**number (const int/float) **The value to be rounded.

#### Returns

The value of `number` rounded to the nearest integer, or according to precision.

#### Remarks

Note that for 'na' values function returns 'na'.

#### See also

math.ceil()math.floor()

<!-- anchor: fun_math.sqrt -->
Square root of any `number` >= 0 is the unique y >= 0 such that y^2 = `number`.

#### Syntax & Overloads

math.sqrt(number) → const float

math.sqrt(number) → input float

math.sqrt(number) → simple float

math.sqrt(number) → series float

#### Arguments

**number (const int/float) **The number to use in the calculation.

#### Returns

The square root of `number`.

#### See also

math.pow()

<!-- anchor: fun_math.sum -->
The sum function returns the sliding sum of last y values of x.

#### Syntax

```
math.sum(source, length) → series float
```

#### Arguments

**source (series int/float) **Series of values to process.

**length (series int) **Number of bars (length).

#### Returns

Sum of `source` for `length` bars back.

#### Remarks

`na` values in the `source` series are ignored; the function calculates on the `length` quantity of non-`na` values.

#### See also

ta.cum()for

<!-- anchor: fun_request.security -->
Requests the result of an expression from a specified context (symbol and timeframe).

#### Syntax

```
request.security(symbol, timeframe, expression, gaps, lookahead, ignore_invalid_symbol, currency, calc_bars_count) → series <type>
```

#### Arguments

**symbol (series string) **Symbol or ticker identifier of the requested data. Use an empty string or syminfo.tickerid to request data using the chart's symbol. To retrieve data with additional modifiers (extended sessions, dividend adjustments, non-standard chart types like Heikin Ashi and Renko, etc.), create a custom ticker ID for the request using the functions in the `ticker.*` namespace.

**timeframe (series string) **Timeframe of the requested data. Use an empty string or timeframe.period to request data from the chart's timeframe or the `timeframe` specified in the indicator() function. To request data from a different timeframe, supply a valid timeframe string. See here to learn about specifying timeframe strings.

**expression (variable, function, object, array, matrix, or map of series int/float/bool/string/color/enum, or a tuple of these) **The expression to calculate and return from the requested context. It can accept a built-in variable like close, a user-defined variable, an expression such as `ta.change(close) / (high - low)`, a function call that does not use Pine Script® drawings, an object, a collection, or a tuple of expressions.

**gaps (simple barmerge_gaps) **Specifies how the returned values are merged on chart bars. Possible values: barmerge.gaps_on, barmerge.gaps_off. With barmerge.gaps_on a value only appears on the current chart bar when it first becomes available from the function's context, otherwise na is returned (thus a "gap" occurs). With barmerge.gaps_off what would otherwise be gaps are filled with the latest known value returned, avoiding na values. Optional. The default is barmerge.gaps_off.

**lookahead (simple barmerge_lookahead) **On historical bars only, returns data from the timeframe before it elapses. Possible values: barmerge.lookahead_on, barmerge.lookahead_off. Has no effect on realtime values. Optional. The default is barmerge.lookahead_off starting from Pine Script® v3. The default is barmerge.lookahead_on in v1 and v2. WARNING: Using barmerge.lookahead_on at timeframes higher than the chart's without offsetting the `expression` argument like in `close[1]` will introduce future leak in scripts, as the function will then return the `close` price before it is actually known in the current context. As is explained in the User Manual's page on Repainting this will produce misleading results.

**ignore_invalid_symbol (input bool) **Determines the behavior of the function if the specified symbol is not found: if false, the script will halt and throw a runtime error; if true, the function will return na and execution will continue. Optional. The default is false.

**currency (series string) **Optional. Specifies the target currency for converting values expressed in currency units (e.g., open, high, low, close) or expressions involving such values. Literal values such as `200` are not converted. The conversion rate for monetary values depends on the previous daily value of a corresponding currency pair from the most popular exchange. A spread symbol is used if no exchange provides the rate directly. Possible values: a "string" representing a valid currency code (e.g., "USD" or "USDT") or a constant from the `currency.*` namespace (e.g., currency.USD or currency.USDT). The default is syminfo.currency.

**calc_bars_count (simple int) **Optional. Determines the maximum number of recent historical bars that the function can request. If specified, the function evaluates the `expression` argument starting from that number of bars behind the last historical bar in the requested dataset, treating those bars as the only available data. Limiting the number of historical bars in a request can help improve calculation efficiency in some cases. The default is the same as the number of chart bars available for the symbol and timeframe. The maximum number of bars that the function can attempt to retrieve depends on the intrabar limit of the user's plan. However, the request cannot retrieve more bars than are available in the dataset.

#### Returns

A result determined by `expression`.

#### Remarks

Scripts using this function might calculate differently on historical and realtime bars, leading to repainting.

A single script can contain no more than 40 unique `request.*()` function calls. A call is unique only if it does not call the same function with the same arguments.

When using two calls to a `request.*()` function to evaluate the same expression from the same context with different `calc_bars_count` values, the second call requests the same number of historical bars as the first. For example, if a script calls `request.security("AAPL", "", close, calc_bars_count = 3)` after it calls `request.security("AAPL", "", close, calc_bars_count = 5)`, the second call also uses five bars of historical data, not three.

The symbol of a `request.()` call can be inherited if it is not specified precisely, i.e., if the `symbol` argument is an empty string or syminfo.tickerid. Similarly, the timeframe of a `request.()` call can be inherited if the `timeframe` argument is an empty string or timeframe.period. These values are normally taken from the chart on which the script is running. However, if `request.*()` function A is called from within the expression of `request.*()` function B, then function A can inherit the values from function B. See here for more information.

#### See also

syminfo.tickersyminfo.tickeridtimeframe.periodticker.new()ticker.modify()request.security_lower_tf()request.dividends()request.earnings()request.splits()request.financial()

<!-- anchor: var_chart.bg_color -->
Returns the color of the chart's background from the "Chart settings/Appearance/Background" field. When a gradient is selected, the middle point of the gradient is returned.

#### Type

input color

#### See also

chart.fg_color

<!-- anchor: var_chart.fg_color -->
Returns a color providing optimal contrast with chart.bg_color.

#### Type

input color

#### See also

chart.bg_color

<!-- anchor: var_syminfo.mintick -->
Min tick value for the current symbol.

#### Type

simple float

#### See also

syminfo.pointvaluesyminfo.mincontract

<!-- anchor: var_syminfo.mincontract -->
The smallest amount of the current symbol that can be traded. This limit is set by the exchange. For cryptocurrencies, it is often less than 1 token. For most other types of asset, it is often 1.

#### Type

simple float

#### See also

syminfo.minticksyminfo.pointvalue

<!-- anchor: fun_timeframe.from_seconds -->
Converts a number of seconds into a valid timeframe string.

#### Syntax & Overloads

timeframe.from_seconds(seconds) → simple string

timeframe.from_seconds(seconds) → series string

#### Arguments

**seconds (simple int) **The number of seconds in the timeframe.

#### Returns

A timeframe string compliant with timeframe string specifications.

#### Remarks

If no valid timeframe exists for the quantity of seconds supplied, the next higher valid timeframe will be returned. Accordingly, one second or less will return "1S", 2-5 seconds will return "5S", and 604,799 seconds (one second less than 7 days) will return "7D".

If the seconds exactly represent two or more valid timeframes, the one with the larger base unit will be used. Thus 604,800 seconds (7 days) returns "1W", not "7D".

All values above 31,622,400 (366 days) return "12M".

#### See also

timeframe.in_seconds()request.securityrequest.security_lower_tf


<!-- anchor: fun_timeframe.in_seconds -->
Converts a timeframe string into seconds.

#### Syntax & Overloads

timeframe.in_seconds(timeframe) → simple int

timeframe.in_seconds(timeframe) → series int

#### Arguments

**timeframe (simple string) **Timeframe string in timeframe string specifications format. Optional. The default is timeframe.period.

#### Returns

The "int" representation of the number of seconds in the timeframe string.

#### Remarks

When the timeframe is "1M" or more, calculations use 2628003 as the number of seconds in one month, which represents 30.4167 (365/12) days.

#### See also

input.timeframe()timeframe.periodtimeframe.from_seconds()


<!-- anchor: const_math.pi -->
Is a named constant for Archimedes' constant. It is equal to 3.1415926535897932.

#### Type

const float

#### See also

math.emath.phimath.rphi

