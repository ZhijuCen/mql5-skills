# ValidationSettings

Checks the settings.

```
virtual bool  ValidationSettings()

```

Return Value

true - successful, otherwise - false.

Note

The function checks Take Profit and Stop Loss levels. The correct values are 0 and values greater than the minimal indention in points from the current close price to place Stop orders.
