# Event-related chart properties

Four types of events are capable of generating a lot of messages and therefore are disabled by default. To activate or disable them later, set the appropriate chart properties using the [ChartSetInteger](/en/book/applications/charts/charts_properties_overview) function. All properties are of Boolean type: true means enabled, and false means disabled.

| Identifier | Description |
| --- | --- |
| CHART_EVENT_MOUSE_WHEEL | Sending CHARTEVENT_MOUSE_WHEEL messages about mouse wheel events to the chart |
| CHART_EVENT_MOUSE_MOVE | Sending CHARTEVENT_MOUSE_MOVE messages about mouse movements to the chart |
| CHART_EVENT_OBJECT_CREATE | Sending CHARTEVENT_OBJECT_CREATE messages about the creation of graphical objects to the chart |
| CHART_EVENT_OBJECT_DELETE | Sending CHARTEVENT_OBJECT_DELETE messages about the deletion of graphical objects to the chart |

If any MQL program changes one of these properties, it affects all other programs running on the same chart and remains in effect even after the original program terminates.

By default, all properties have the false value.

Let's complement the EventAll.mq5 indicator from the previous section with four input variables that allow you to enable any of these types of events (in addition to the rest that cannot be disabled). In addition, we will describe four auxiliary variables in order to be able to restore the chart settings after deleting the indicator.

```
input bool ShowMouseMove = false;
input bool ShowMouseWheel = false;
input bool ShowObjectCreate = false;
input bool ShowObjectDelete = false;
   
bool mouseMove, mouseWheel, objectCreate, objectDelete;

```

At startup, remember the current values of the properties and then apply the settings selected by the user.

```
void OnInit()
{
   mouseMove = PRTF(ChartGetInteger(0, CHART_EVENT_MOUSE_MOVE));
   mouseWheel = PRTF(ChartGetInteger(0, CHART_EVENT_MOUSE_WHEEL));
   objectCreate = PRTF(ChartGetInteger(0, CHART_EVENT_OBJECT_CREATE));
   objectDelete = PRTF(ChartGetInteger(0, CHART_EVENT_OBJECT_DELETE));
   
   ChartSetInteger(0, CHART_EVENT_MOUSE_MOVE, ShowMouseMove);
   ChartSetInteger(0, CHART_EVENT_MOUSE_WHEEL, ShowMouseWheel);
   ChartSetInteger(0, CHART_EVENT_OBJECT_CREATE, ShowObjectCreate);
   ChartSetInteger(0, CHART_EVENT_OBJECT_DELETE, ShowObjectDelete);
}

```

Properties are restored in the OnDeinit handler.

```
void OnDeinit(const int)
{
   ChartSetInteger(0, CHART_EVENT_MOUSE_MOVE, mouseMove);
   ChartSetInteger(0, CHART_EVENT_MOUSE_WHEEL, mouseWheel);
   ChartSetInteger(0, CHART_EVENT_OBJECT_CREATE, objectCreate);
   ChartSetInteger(0, CHART_EVENT_OBJECT_DELETE, objectDelete);
}

```

Run the indicator with the new event types enabled. Be prepared for a lot of mouse movement messages. Here is a snippet of the log:

```
CHARTEVENT_MOUSE_WHEEL 5308557 -120.000000 ''
CHARTEVENT_CHART_CHANGE 0 0.000000 ''
CHARTEVENT_MOUSE_WHEEL 5308557 -120.000000 ''
CHARTEVENT_CHART_CHANGE 0 0.000000 ''
CHARTEVENT_MOUSE_MOVE 141 81.000000 '2'
CHARTEVENT_MOUSE_MOVE 141 81.000000 '0'
...
CHARTEVENT_OBJECT_CREATE 0 0.000000 'Daily Rectangle 37664'
CHARTEVENT_MOUSE_MOVE 323 146.000000 '0'
CHARTEVENT_MOUSE_MOVE 322 146.000000 '0'
CHARTEVENT_MOUSE_MOVE 321 146.000000 '0'
CHARTEVENT_MOUSE_MOVE 320 146.000000 '0'
CHARTEVENT_MOUSE_MOVE 318 146.000000 '0'
CHARTEVENT_MOUSE_MOVE 316 146.000000 '0'
CHARTEVENT_MOUSE_MOVE 314 146.000000 '0'
CHARTEVENT_MOUSE_MOVE 314 145.000000 '0'
...
CHARTEVENT_OBJECT_DELETE 0 0.000000 'Daily Rectangle 37664'
CHARTEVENT_KEYDOWN 46 1.000000 '339

```

We will disclose the specifics of information for each type of event in the relevant sections below.
