# Getting event descriptions by ID

Real MQL programs, as a rule, request current or upcoming calendar events, filtering by time range, countries, currencies, or other criteria. The API functions intended for this, which we have yet to consider, return [MqlCalendarValue](/en/book/advanced/calendar/calendar_overview) structures, which store only the event identifier instead of its description. Therefore, the CalendarEventById function can be useful if you need to extract complete information.

bool CalendarEventById(ulong id, MqlCalendarEvent &event)

The CalendarEventById function gets the description of the event by its ID. The function returns a success or error indication.

An example of how to use this function will be given in the next section.
