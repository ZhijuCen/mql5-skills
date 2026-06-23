# X_Offset (Get Method)

Gets the value of "X_Offset" property (the upper left corner) of the [CChartObjectBitmap](/en/docs/standardlibrary/chart_object_classes/obj_controls/cchartobjectbitmap) graphical object.

```
int  X_Offset() const

```

Return Value

Value of "X_Offset" property of the object assigned to the class instance. If there is no object assigned, it returns 0.

# X_Offset (Set Method)

Sets new value for "X_Offset" property (the upper left corner) of the [CChartObjectBitmap](/en/docs/standardlibrary/chart_object_classes/obj_controls/cchartobjectbitmap) graphical object. The value is set in pixels relative to the upper left corner of the original image.

```
bool  X_Offset(
   int  X      // property value
   )

```

Parameters

X

[in]  New value for "X_Offset" property.

Return Value

true - successful, false - cannot change the property.
