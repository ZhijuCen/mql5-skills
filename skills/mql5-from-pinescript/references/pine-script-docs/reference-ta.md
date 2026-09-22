<!-- source: https://www.tradingview.com/pine-script-reference/v6/ | fetched 2026-09-23 | examples omitted -->

<!-- anchor: fun_ta.atr -->
Function atr (average true range) returns the RMA of true range. True range is max(high - low, abs(high - close[1]), abs(low - close[1])).

#### Syntax

```
ta.atr(length) → series float
```

#### Arguments

**length (simple int) **Length (number of bars back).

#### Returns

Average true range.

#### Remarks

`na` values in the `source` series are ignored; the function calculates on the `length` quantity of non-`na` values.

#### See also

ta.tr()ta.rma()


<!-- anchor: fun_ta.rma -->
Moving average used in RSI. It is the exponentially weighted moving average with alpha = 1 / length.

#### Syntax

```
ta.rma(source, length) → series float
```

#### Arguments

**source (series int/float) **Series of values to process.

**length (simple int) **Number of bars (length).

#### Returns

Exponential moving average of `source` with alpha = 1 / `length`.

#### Remarks

`na` values in the `source` series are ignored; the function calculates on the `length` quantity of non-`na` values.

#### See also

ta.sma()ta.ema()ta.wma()ta.vwma()ta.swma()ta.alma()ta.rsi()


<!-- anchor: fun_ta.ema -->
The ema function returns the exponentially weighted moving average. In ema weighting factors decrease exponentially. It calculates by using a formula: `EMA = alpha * source + (1 - alpha) * EMA[1]`, where `alpha = 2 / (length + 1)`.

#### Syntax

```
ta.ema(source, length) → series float
```

#### Arguments

**source (series int/float) **Series of values to process.

**length (simple int) **Number of bars (length).

#### Returns

Exponential moving average of `source` with alpha = 2 / (length + 1).

#### Remarks

Please note that using this variable/function can cause indicator repainting.

`na` values in the `source` series are ignored; the function calculates on the `length` quantity of non-`na` values.

#### See also

ta.sma()ta.rma()ta.wma()ta.vwma()ta.swma()ta.alma()


<!-- anchor: fun_ta.sma -->
The sma function returns the moving average, that is the sum of last y values of x, divided by y.

#### Syntax

```
ta.sma(source, length) → series float
```

#### Arguments

**source (series int/float) **Series of values to process.

**length (series int) **Number of bars (length).

#### Returns

Simple moving average of `source` for `length` bars back.

#### Remarks

`na` values in the `source` series are ignored.

#### See also

ta.ema()ta.rma()ta.wma()ta.vwma()ta.swma()ta.alma()


<!-- anchor: fun_ta.crossover -->
The `source1`-series is defined as having crossed over `source2`-series if, on the current bar, the value of `source1` is greater than the value of `source2`, and on the previous bar, the value of `source1` was less than or equal to the value of `source2`.

#### Syntax

```
ta.crossover(source1, source2) → series bool
```

#### Arguments

**source1 (series int/float) **First data series.

**source2 (series int/float) **Second data series.

#### Returns

true if `source1` crossed over `source2` otherwise false.


<!-- anchor: fun_ta.crossunder -->
The `source1`-series is defined as having crossed under `source2`-series if, on the current bar, the value of `source1` is less than the value of `source2`, and on the previous bar, the value of `source1` was greater than or equal to the value of `source2`.

#### Syntax

```
ta.crossunder(source1, source2) → series bool
```

#### Arguments

**source1 (series int/float) **First data series.

**source2 (series int/float) **Second data series.

#### Returns

true if `source1` crossed under `source2` otherwise false.


<!-- anchor: fun_ta.dmi -->
The dmi function returns the directional movement index.

#### Syntax

```
ta.dmi(diLength, adxSmoothing) → [series float, series float, series float]
```

#### Arguments

**diLength (simple int) **DI Period.

**adxSmoothing (simple int) **ADX Smoothing Period.

#### Returns

Tuple of three DMI series: Positive Directional Movement (+DI), Negative Directional Movement (-DI) and Average Directional Movement Index (ADX).

#### See also

ta.rsi()ta.tsi()ta.mfi()


<!-- anchor: fun_ta.percentile_nearest_rank -->
Calculates percentile using method of Nearest Rank.

#### Syntax

```
ta.percentile_nearest_rank(source, length, percentage) → series float
```

#### Arguments

**source (series int/float) **Series of values to process (source).

**length (series int) **Number of bars back (length).

**percentage (simple int/float) **Percentage, a number from range 0..100.

#### Returns

P-th percentile of `source` series for `length` bars back.

#### Remarks

Using the Nearest Rank method on lengths less than 100 bars back can result in the same number being used for more than one percentile.

A percentile calculated using the Nearest Rank method will always be a member of the input data set.

The 100th percentile is defined to be the largest value in the input data set.

`na` values in the `source` series are ignored.

#### See also

ta.percentile_linear_interpolation()


<!-- anchor: fun_ta.rising -->
Test if the `source` series is now rising for `length` bars long.

#### Syntax

```
ta.rising(source, length) → series bool
```

#### Arguments

**source (series int/float) **Series of values to process.

**length (series int) **Number of bars (length).

#### Returns

true if current `source` is greater than any previous `source` for `length` bars back, false otherwise.

#### Remarks

`na` values in the `source` series are ignored.

#### See also

ta.falling()


<!-- anchor: fun_ta.falling -->
Test if the `source` series is now falling for `length` bars long.

#### Syntax

```
ta.falling(source, length) → series bool
```

#### Arguments

**source (series int/float) **Series of values to process.

**length (series int) **Number of bars (length).

#### Returns

true if current `source` value is less than any previous `source` value for `length` bars back, false otherwise.

#### Remarks

`na` values in the `source` series are ignored; the function calculates on the `length` quantity of non-`na` values.

#### See also

ta.rising()


<!-- anchor: fun_ta.highest -->
Highest value for a given number of bars back.

#### Syntax

```
ta.highest(source, length) → series float
```

#### Arguments

**source (series int/float) **Series of values to process.

**length (series int) **Number of bars (length).

#### Returns

Highest value in the series.

#### Remarks

Two args version: `source` is a series and `length` is the number of bars back.

One arg version: `length` is the number of bars back. Algorithm uses high as a `source` series.

`na` values in the `source` series are ignored.

#### See also

ta.lowest()ta.lowestbars()ta.highestbars()ta.valuewhen()ta.barssince()


<!-- anchor: fun_ta.lowest -->
Lowest value for a given number of bars back.

#### Syntax

```
ta.lowest(source, length) → series float
```

#### Arguments

**source (series int/float) **Series of values to process.

**length (series int) **Number of bars (length).

#### Returns

Lowest value in the series.

#### Remarks

Two args version: `source` is a series and `length` is the number of bars back.

One arg version: `length` is the number of bars back. Algorithm uses low as a `source` series.

`na` values in the `source` series are ignored.

#### See also

ta.highest()ta.lowestbars()ta.highestbars()ta.valuewhen()ta.barssince()

