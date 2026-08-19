# LogLevel

Sets logging level for messages.

```
void  LogLevel(
   ENUM_LOG_LEVELS  log_level      // level
   )

```

Parameters

log_level

[in]  New logging level.

Return Value

None.

Note

LOG_LEVEL_NO and less disables displaying any messages (set up automatically in the optimization mode). LOG_LEVEL_ERRORS enables displaying only error messages (value by default). LOG_LEVEL_ALL and greater enables displaying any messages (set up automatically in the test mode).

ENUM_LOG_LEVELS

| Identifier | Description | Value |
| --- | --- | --- |
| LOG_LEVEL_NO | Displaying messages disabled | 0 |
| LOG_LEVEL_ERRORS | Only error messages are displayed | 1 |
| LOG_LEVEL_ALL | All messages are displayed | 2 |
