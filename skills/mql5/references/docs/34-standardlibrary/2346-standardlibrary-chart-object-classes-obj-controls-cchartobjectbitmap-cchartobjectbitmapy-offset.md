# Y_Offset (Get Method)

Gets the value of "Y_Offset" property (the upper left corner) of the [CChartObjectBitmap](/en/docs/standardlibrary/chart_object_classes/obj_controls/cchartobjectbitmap) graphical object.

```
int  Y_Offset() const

```

Return Value

Value of "Y_Offset" property of the object assigned to the class instance. If there is no object assigned, it returns 0.

# Y_Offset (Set Method)

Sets new value for "Y_Offset" property (the upper left corner) of the [CChartObjectBitmap](/en/docs/standardlibrary/chart_object_classes/obj_controls/cchartobjectbitmap) graphical object. The value is set in pixels relative to the upper left corner of the original image.

```
bool  Y_Offset(
   int  Y      // property value
   )

```

Parameters

Y

[in]  New value for "Y_Offset" property.

Return Value

true - successful, false - cannot change the property.
