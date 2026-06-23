# OnSetZOrder

The virtual handler of "SetZOrder" (change of the [OBJPROP_ZORDER](/en/docs/constants/objectconstants/enum_object_property#enum_object_property_integer) property) event.

```
virtual bool  OnSetZOrder()

```

Return Value

true - event processed, otherwise - false.

Note

The base class method does nothing and always returns true.
