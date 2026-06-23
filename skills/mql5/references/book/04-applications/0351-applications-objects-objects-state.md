# Managing the object state

Among the general properties of objects, there are several ones that control the state of objects. All such properties have a Boolean type, meaning they can be turned on (true) or off (false), and therefore require the use of the functions ObjectGetInteger and ObjectSetInteger.

| Identifier | Description |
| --- | --- |
| OBJPROP_HIDDEN | Disable displaying the name of a graphical object in the list of objects in the relevant dialog (called from the context menu of the chart or by pressing Ctrl+B). |
| OBJPROP_SELECTED | Object selection |
| OBJPROP_SELECTABLE | Availability of an object for selection |

A value of true for OBJPROP_HIDDEN allows you to hide an unnecessary object from the user's list. By default, true is set for objects that display calendar events, the trading history, as well as for objects created from MQL programs. To see such graphical objects and access their properties, press the All button in the Object List dialog.

An object hidden in the list remains visible on the chart. To hide an object on the chart without deleting it, you can use the [Visibility of objects in the context of timeframes](/en/book/applications/objects/objects_timeframes) setting.

The user cannot select and change the properties of objects for which OBJPROP_SELECTABLE is equal to false. Objects created programmatically are not allowed to be selected by default. As we saw in the ObjectCornerLabel.mq5 and ObjectAnchorLabel.mq5 scripts in the previous sections, it was necessary to explicitly set OBJPROP_SELECTABLE to true to unlock the ability to include OBJPROP_SELECTED as well. This is how we highlighted the anchor points on the object.

Usually, MQL programs allow the selection of their objects only if these objects serve as controls. For example, a trend line with a predefined name, which the user moves at will, can mean a condition for sending a trade order when the price crosses it.
