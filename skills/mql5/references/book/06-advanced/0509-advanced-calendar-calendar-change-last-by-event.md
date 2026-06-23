# Tracking event changes by type

The MQL5 API allows you to request recent changes not only in general for the entire calendar or by country or currency, but also in a narrower range, or rather, for a specific type of event.

In theory, we can say that the built-in functions provide filtering of events according to several basic conditions: time, country, currency, or type of event. For other attributes, such as importance or economic sector, you need to implement your own filtering, and we will deal with this later. For now, let's introduce the CalendarValueLastByEvent function.

int CalendarValueLastByEvent(ulong id, ulong &change_id, MqlCalendarValue &values[])

The function fills the values array passed by reference with event records of a specific type with the id identifier that have occurred since change_id. This change_id parameter is both input and output: the calling code passes in it the label of the past state of the calendar, after which changes are requested, and when control returns, the function writes the current label of the calendar database state to change_id. It should be used the next time the function is called.

If you pass null in change_id, then the function does not fill the array but simply sends the current state of the database through the parameter change_id.

The array can be dynamic (then it will be automatically adjusted to the amount of data) or fixed size (if its size is insufficient, only data that fit will be copied).

The output value of the function is equal to the number of elements copied into the values array. If there are no changes or change_id = 0 is specified, the function will return 0.

To check for an error, analyze the built-in _LastError variable. Some of the possible error codes are:

- 4004 - ERR_NOT_ENOUGH_MEMORY (not enough memory to complete the request),
- 5401 - ERR_CALENDAR_TIMEOUT (request timed out),
- 5400 - ERR_CALENDAR_MORE_DATA (the size of the fixed array is not enough to get all the values).

We will not give a separate example for CalendarValueLastByEvent. Instead, let's turn to a more complex, but in-demand task of querying and filtering calendar entries with arbitrary conditions on news attributes, where all the "calendar" API functions will be involved. This will be the subject of the next section.
