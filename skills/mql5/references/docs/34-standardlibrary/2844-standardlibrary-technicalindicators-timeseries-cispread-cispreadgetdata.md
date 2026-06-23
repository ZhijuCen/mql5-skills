# GetData

Gets the specified element of timeseries buffer.

```
int  GetData(
   int  index      // index
   ) const

```

Parameters

index

[in]  Index of the buffer element.

Return Value

The timeseries buffer element, or 0.

# GetData

Gets the element of timeseries by starting position and number of elements.

```
int  GetData(
   int   start_pos,     // position
   int   count,         // number
   int&  buffer         // array
   ) const

```

Parameters

start_pos

[in]  Starting position of a timeseries buffer.

count

[in]  Number of timeseries buffer elements.

buffer

[in]  Reference to the array for storing the data.

Return Value

>=0 - successful, -1 - cannot receive the data.

# GetData

Gets data from a timeseries buffer by initial time and number.

```
int  GetData(
   datetime  start_time,     // starting time
   int       count,          // number
   int&      buffer          // array
   ) const

```

Parameters

start_time

[in]  Time of the timeseries buffer's initial element.

count

[in]  Number of timeseries buffer elements.

buffer

[in]  Reference to the array for storing data.

Return Value

>=0 - successful, -1 - cannot receive data.

# GetData

Gets the data from a timeseries buffer by start and stop times.

```
int  GetData(
   datetime  start_time,     // starting time
   datetime  stop_time,      // stop time
   int&      buffer          // array
   ) const

```

Parameters

start_time

[in]  Starting time of a timeseries buffer element.

stop_time

[in]  Stop time of a timeseries buffer element.

buffer

[in]  Reference to the array for storing data.

Return Value

>=0 - successful, -1 - cannot receive the data.
