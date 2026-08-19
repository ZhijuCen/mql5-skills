# GetData

Gets data from a timeseries buffer by starting position and number.

```
int  GetData(
   int   start_pos,     // position
   int   count,         // number
   double& buffer       // array
   ) const

```

Parameters

start_pos

[in]  Starting position of a timeseries buffer.

count

[in]  Number of timeseries buffer elements.

buffer

[in]  Reference to the data storage array.

Return Value

>=0 - successful, -1 - cannot receive data.

# GetData

Gets data from a timeseries buffer by starting time and number.

```
int  GetData(
   datetime  start_time,     // starting time
   int       count,          // number
   double&     buffer        // array
   ) const

```

Parameters

start_time

[in]  Time of a timeseries buffer initial element.

count

[in]  Number of a timeseries buffer element.

buffer

[in]  Reference to the data storage array.

Return Value

>=0 - successful, -1 - cannot receive data.

# GetData

Gets data from a timeseries buffer by starting and stop times.

```
int  GetData(
   datetime  start_time,     // starting time
   datetime  stop_time,      // stop time
   double&   buffer          // array
   ) const

```

Parameters

start_time

[in]  Time of a timeseries buffer initial element.

stop_time

[in]  Time of a timeseries buffer last element.

buffer

[in]  Reference to the data storage array.

Return Value

>=0 - successful, -1 - cannot receive data.
