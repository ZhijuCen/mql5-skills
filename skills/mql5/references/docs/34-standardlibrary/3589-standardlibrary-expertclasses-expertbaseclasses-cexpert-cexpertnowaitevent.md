# NoWaitEvent

Resets the event waiting flag.

```
void  NoWaitEvent(
   ENUM_TRADE_EVENTS    event         // flag
   )

```

Parameters

event

[in]  Flag with events (from ENUM_TRADE_EVENTS enumeration) to reset.

Return Value

None.

Event flags

```
//--- flags of expected events
enum ENUM_TRADE_EVENTS
  {
   TRADE_EVENT_NO_EVENT              =0,         // no expected events
   TRADE_EVENT_POSITION_OPEN         =0x1,       // flag of expecting the "opening of position" event
   TRADE_EVENT_POSITION_VOLUME_CHANGE=0x2,       // flag of expecting of the "modification of position volume" event
   TRADE_EVENT_POSITION_MODIFY       =0x4,       // flag of expecting of the "modification of stop order of position" event
   TRADE_EVENT_POSITION_CLOSE        =0x8,       // flag of expecting of the "closing of position" event
   TRADE_EVENT_POSITION_STOP_TAKE    =0x10,      // flag of expecting of the "triggering of stop order of position"
   TRADE_EVENT_ORDER_PLACE           =0x20,      // flag of expecting of the "placing of pending order" event
   TRADE_EVENT_ORDER_MODIFY          =0x40,      // flag of expecting of the "modification of pending order" event
   TRADE_EVENT_ORDER_DELETE          =0x80,      // flag of expecting of the "deletion of pending order" event
   TRADE_EVENT_ORDER_TRIGGER         =0x100      // flag of expecting of the "triggering of pending order" event
  };

```
