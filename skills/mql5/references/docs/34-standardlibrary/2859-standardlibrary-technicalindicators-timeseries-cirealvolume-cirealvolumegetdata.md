# GetData

Gets the specified series buffer element.

```
datetime  GetData(
   int  index      // index
   ) const

```

Parameters

index

[in]  Buffer element index.

Return Value

Series buffer element, or 0.

# GetData

Gets the data from timeseries buffer by starting position and number.

```
int  GetData(
   int   start_pos,     // position
   int   count,         // number
   long& buffer         // array
   ) const

```

Parameters

start_pos

[in]  Starting position of timeseries buffer.

count

[in]  Number of timeseries buffer elements.

buffer

[in]  Reference to the data storage array.

Return Value

>=0 - successful, -1 - cannot receive data.

# GetData

Gets the data from timeseries buffer by starting time and number.

```
int  GetData(
   datetime  start_time,     // starting time
   int       count,          // number
   long&     buffer          // array
   ) const

```

Parameters

start_time

[in]  Time of the timeseries buffer initial element.

count

[in]  Number of timeseries buffer elements.

buffer

[in]  Reference to the data storage array.

Return Value

>=0 - successful, -1 - cannot receive data.

# GetData

Gets the element of timeseries by starting and stop times.

```
int  GetData(
   datetime  start_time,     // starting time
   datetime  stop_time,      // stop time
   long&     buffer          // target array
   ) const

```

Parameters

start_time

[in]  Starting time.

stop_time

[in]  Stop time.

buffer

[in]  Reference to the target array for data

Return Value

>=0 if successful, -1 in the case of error.
