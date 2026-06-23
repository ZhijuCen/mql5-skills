# GetData

Gets the specified element of the specified buffer of the indicator. [Refresh()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorrefresh) should be called for working with recent data before using the method.

```
double  GetData(
   const int  buffer_num,     // buffer number
   const int  index           // index
   ) const

```

Parameters

buffer_num

[in]  Indicator buffer number.

index

[in]  Indicator buffer element index.

Return Value

value - success, [EMPTY_VALUE](/en/docs/constants/namedconstants/otherconstants) - cannot receive the data.

# GetData

Gets the data from the indicator's buffer by starting position and number.

```
int  GetData(
   const int      start_pos,      // position
   const int      count,          // number
   const int      buffer_num,     // buffer number
   double&        buffer[]        // array
   ) const

```

Parameters

start_pos

[in]  Starting position of the indicator buffer.

count

[in]  Number of indicator buffer elements.

buffer_num

[in]  Number of the indicator buffer.

buffer

[in]  Reference to the array for storing data.

Return Value

Number of the indicator values received ​​from the specified indicator buffer - success, otherwise -1.

# GetData

Gets the data from the indicator buffer by start time and number.

```
int  GetData(
   const datetime  start_time,     // starting time
   const int       count,          // amount
   const int       buffer_num,     // buffer number
   double&         buffer[]        // array
   ) const

```

Parameters

start_time

[in]  Indicator buffer element starting time.

count

[in]  Number of indicator buffer elements.

buffer_num

[in]  Number of the indicator buffer.

buffer

[in]  Reference to the array for storing data.

Return Value

Number of the indicator values received ​​from the specified buffer, otherwise -1.

# GetData

Gets the data from the indicator buffer by start and end time.

```
int  GetData(
   const datetime  start_time,     // start time
   const datetime  stop_time,      // end time
   const int       buffer_num,     // number of buffer
   double&         buffer[]        // array
   ) const

```

Parameters

start_time

[in]  Indicator buffer initial element time.

stop_time

[in]  Indicator buffer end element time.

buffer_num

[in]  Number of the indicator buffer.

buffer

[in]  Reference to the array for storing data.

Return Value

Number of the indicator values received ​​from the specified buffer - success, otherwise -1.
