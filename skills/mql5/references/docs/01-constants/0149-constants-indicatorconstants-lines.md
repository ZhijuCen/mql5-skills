# Indicators Lines

Some [technical indicators](/en/docs/indicators) have several buffers drawn in the chart. Numbering of indicator buffers starts with 0. When copying indicator values using the [CopyBuffer()](/en/docs/series/copybuffer) function into an array of the double type, for some indicators one may indicate the identifier of a copied buffer instead of its number.

Identifiers of indicator lines permissible when copying values of [iMACD()](/en/docs/indicators/imacd), [iRVI()](/en/docs/indicators/irvi) and [iStochastic()](/en/docs/indicators/istochastic).

| Constant | Value | Description |
| --- | --- | --- |
| MAIN_LINE | 0 | Main line |
| SIGNAL_LINE | 1 | Signal line |

Identifiers of indicator lines permissible when copying values of [ADX()](/en/docs/indicators/iadx) and [ADXW()](/en/docs/indicators/iadxwilder).

| Constant | Value | Description |
| --- | --- | --- |
| MAIN_LINE | 0 | Main line |
| PLUSDI_LINE | 1 | Line +DI |
| MINUSDI_LINE | 2 | Line –DI |

Identifiers of indicator lines permissible when copying values of [iBands()](/en/docs/indicators/ibands).

| Constant | Value | Description |
| --- | --- | --- |
| BASE_LINE | 0 | Main line |
| UPPER_BAND | 1 | Upper limit |
| LOWER_BAND | 2 | Lower limit |

Identifiers of indicator lines permissible when copying values of [iEnvelopes()](/en/docs/indicators/ienvelopes) and [iFractals()](/en/docs/indicators/ifractals).

| Constant | Value | Description |
| --- | --- | --- |
| UPPER_LINE | 0 | Upper line |
| LOWER_LINE | 1 | Bottom line |

Identifiers of indicator lines permissible when copying values of [iGator()](/en/docs/indicators/igator)

| Constant | Value | Description |
| --- | --- | --- |
| UPPER_HISTOGRAM | 0 | Upper histogram |
| LOWER_HISTOGRAM | 2 | Bottom histogram |

Identifiers of indicator lines permissible when copying values of [iAlligator()](/en/docs/indicators/ialligator).

| Constant | Value | Description |
| --- | --- | --- |
| GATORJAW_LINE | 0 | Jaw line |
| GATORTEETH_LINE | 1 | Teeth line |
| GATORLIPS_LINE | 2 | Lips line |

Identifiers of indicator lines permissible when copying values of [iIchimoku()](/en/docs/indicators/iichimoku).

| Constant | Value | Description |
| --- | --- | --- |
| TENKANSEN_LINE | 0 | Tenkan-sen line |
| KIJUNSEN_LINE | 1 | Kijun-sen line |
| SENKOUSPANA_LINE | 2 | Senkou Span A line |
| SENKOUSPANB_LINE | 3 | Senkou Span B line |
| CHIKOUSPAN_LINE | 4 | Chikou Span line |
