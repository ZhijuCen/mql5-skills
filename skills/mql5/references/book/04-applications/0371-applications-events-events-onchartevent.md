# Event handling function OnChartEvent

An indicator or Expert Advisor can receive interactive events from the terminal if the code contains the OnChartEvent function with the following prototype.

void OnChartEvent(const int event, const long &lparam, const double &dparam, const string &sparam)

This function will be called by the terminal in response to user actions or in case of generating a "user event" using [EventChartCustom](/en/book/applications/events/events_custom).

In the event parameter, the event identifier (its type) is passed as one of the values of the ENUM_CHART_EVENT enumeration (see the table).

| Identifier | Description |
| --- | --- |
| CHARTEVENT_KEYDOWN | Keyboard action |
| CHARTEVENT_MOUSE_MOVE | Moving the mouse and clicking mouse buttons (if the CHART_EVENT_MOUSE_MOVE property is set for the chart) |
| CHARTEVENT_MOUSE_WHEEL | Clicking or scrolling the mouse wheel (if the CHART_EVENT_MOUSE_WHEEL property is set for the chart) |
| CHARTEVENT_CLICK | Mouse-click on the chart |
| CHARTEVENT_OBJECT_CREATE | Creating a graphical object (if the CHART_EVENT_OBJECT_CREATE property is set for the chart) |
| CHARTEVENT_OBJECT_CHANGE | Modifying a graphical object through the properties dialog |
| CHARTEVENT_OBJECT_DELETE | Deleting a graphical object (if the CHART_EVENT_OBJECT_DELETE property is set for the chart) |
| CHARTEVENT_OBJECT_CLICK | Mouse-click on a graphical object |
| CHARTEVENT_OBJECT_DRAG | Dragging a graphical object |
| CHARTEVENT_OBJECT_ENDEDIT | Finishing text editing in the "input field" graphical object |
| CHARTEVENT_CHART_CHANGE | Changing the chart dimensions or properties (via the properties dialog, toolbar, or context menu) |
| CHARTEVENT_CUSTOM | The starting number of the event from the custom event range |
| CHARTEVENT_CUSTOM_LAST | The end number of the event from the custom event range |

The lparam, dparam, and sparam parameters are used differently depending on the event type. In general, we can say that they contain additional data necessary to process a particular event. The following sections provide details for each type.

Attention! The OnChartEvent function is called only for indicators and Expert Advisors that are directly plotted on the chart. If any indicator is created programmatically using [iCustom](/en/book/applications/indicators_use/indicators_icustom) or [IndicatorCreate](/en/book/applications/indicators_use/indicators_indicatorcreate), the OnChartEvent events will not be translated to it.  

   

In addition, the OnChartEvent handler is not called in the [tester](/en/book/automation/tester), even in visual mode.

For the first demonstration of the OnChartEvent handler, let's consider a bufferless indicator EventAll.mq5 which intercepts and logs all events.

```
void OnChartEvent(const int id,
   const long &lparam, const double &dparam, const string &sparam)
{
   ENUM_CHART_EVENT evt = (ENUM_CHART_EVENT)id;
   PrintFormat("%s %lld %f '%s'", EnumToString(evt), lparam, dparam, sparam);
}

```

By default, all types of events can be generated on the chart, except for four mass events, which, as indicated in the table above, are enabled by the special properties of the chart. In the next section, we will supplement the indicator with settings to include certain types according to preferences.

Run the indicator on a chart with existing objects or create objects while the indicator is running.

Change the size or settings of the chart, make mouse clicks, and edit the properties of objects. The following entries will appear in the log.

```
CHARTEVENT_CHART_CHANGE 0 0.000000 ''
CHARTEVENT_CLICK 149 144.000000 ''
CHARTEVENT_OBJECT_CLICK 112 105.000000 'Daily Rectangle 53404'
CHARTEVENT_CLICK 112 105.000000 ''
CHARTEVENT_KEYDOWN 46 1.000000 '339'
CHARTEVENT_CLICK 13 252.000000 ''
CHARTEVENT_OBJECT_DRAG 0 0.000000 'Daily Button 61349'
CHARTEVENT_OBJECT_CLICK 145 104.000000 'Daily Button 61349'
CHARTEVENT_CLICK 145 104.000000 ''
CHARTEVENT_CHART_CHANGE 0 0.000000 ''
CHARTEVENT_OBJECT_DRAG 0 0.000000 'Daily Vertical Line 22641'
CHARTEVENT_OBJECT_DRAG 0 0.000000 'Daily Vertical Line 22641'
CHARTEVENT_OBJECT_CLICK 177 206.000000 'Daily Vertical Line 22641'
CHARTEVENT_CLICK 177 206.000000 ''
CHARTEVENT_OBJECT_CHANGE 0 0.000000 'Daily Rectangle 37930'
CHARTEVENT_CHART_CHANGE 0 0.000000 ''
CHARTEVENT_CLICK 152 118.000000 ''

```

Here we see events of various types, the meanings of their parameters will become clear after reading the following sections.
