# CopyIndicatorBuffer

Get the data of the specified [indicator](/en/docs/indicators) buffer in the specified quantity to a [vector](/en/docs/basis/types/matrix_vector).

The data will be copied into the vector locating the oldest element at the beginning of the physical memory allocated for the vector. There are three function options.

Access by the initial position and the number of required elements

```
bool  vector::CopyIndicatorBuffer(
   long      indicator_handle,     // indicator handle
   ulong     buffer_index,         // indicator buffer number
   ulong     start_pos,            // starting position to copy
   ulong     count                 // number of elements to copy
   );

```

Access by the start date and the number of required elements

```
bool  vector::CopyIndicatorBuffer(
   long      indicator_handle,     // indicator handle
   ulong     buffer_index,         // indicator buffer number
   datetime  start_time,           // from which date to copy
   ulong     count                 // number of elements to copy
   );

```

Access by the initial and final dates of the required time interval

```
bool  vector::CopyIndicatorBuffer(
   long      indicator_handle,     // indicator handle
   ulong     buffer_index,         // indicator buffer number
   datetime  start_time,           // from which date to copy
   datetime  stop_time             // up to which date to copy
   );

```

Parameters

indicator_handle

[in] The indicator handle obtained by the relevant indicator function.

buffer_index

[in]  The number of the indicator buffer.

start_pos

[in]  The number of the first copied element index.

count

[in]  The number of copied elements.

start_time

[in]  Bar time corresponding to the first element.

stop_time

[in]  Bar time corresponding to the last element.

Return Value

The function returns 'true' on success or 'false' if an [error](/en/docs/constants/errorswarnings/errorcodes) occurs.

Note

The elements of the copied data (the indicator buffer with index buffer_index) are counted down from the present to the past, and thus the starting position equal to 0 means the current bar (the indicator value for the current bar).

When copying an unknown amount of data, you should declare a vector without specifying a size (without allocating memory for the data), since the CopyBuffer() function tries to distribute the size of the receiving vector to the size of the copied data.

When partial copying of the indicator values is needed, you should use an intermediate vector into which the required quantity is copied. From this intermediate vector, you can copy the required number of values member by member, to the required places of the receiving vector.

If you are copying a predetermined amount of data, it is recommended to [pre-declare a vector and specify its size](/en/docs/matrix/matrix_initialization) to avoid unnecessary memory reallocation.

When requesting data from an indicator, the function immediately returns false if requested timeseries have not yet been constructed or they need to be downloaded from the server, while it initiates loading/constructing.

When requesting data from an EA or a script, [download from the server](/en/docs/series/timeseries_access#synchronized) is initiated if the terminal does not have the appropriate data locally, or construction of the necessary timeseries starts if the data can be constructed from the local history but the required timeframes are not ready yet. The function returns the amount that will be ready by the time the timeout expires.

See also

[CopyBuffer](/en/docs/series/copybuffer)
