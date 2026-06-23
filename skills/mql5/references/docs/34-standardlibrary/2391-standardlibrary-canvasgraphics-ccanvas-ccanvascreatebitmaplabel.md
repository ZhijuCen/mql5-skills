# CreateBitmapLabel

Creates a graphical resource bound to a chart object.

1. Creates a graphical resource in the main window of the current chart.

```
bool  CreateBitmapLabel(
   const string       name,                                 // name
   const int          x,                                    // X coordinate
   const int          y,                                    // Y coordinate
   const int          width,                                // width
   const int          height,                               // height
   ENUM_COLOR_FORMAT  clrfmt=COLOR_FORMAT_XRGB_NOALPHA      // format
   );

```

2. Creates a graphical resource using a chart ID and a subwindow number.

```
bool  CreateBitmapLabel(
   const long         chart_id,                             // chart ID
   const int          subwin,                               // subwindow number
   const string       name,                                 // name
   const int          x,                                    // X coordinate
   const int          y,                                    // Y coordinate
   const int          width,                                // width
   const int          height,                               // height
   ENUM_COLOR_FORMAT  clrfmt=COLOR_FORMAT_XRGB_NOALPHA      // format
   );

```

Parameters

chart_id

[in]  Chart ID for creating an object.

subwin

[in]  Chart subwindow number for creating an object.

name

[in]  Chart object name and a basis for a graphical resource name.

x

[in]  Chart object anchor point X coordinate.

y

[in]  Chart object anchor point Y coordinate.

width

[in]  Graphical resource width (size along X axis) in pixels.

height

[in]  Graphical resource height (size along Y axis) in pixels.

clrfmt=COLOR_FORMAT_XRGB_NOALPHA

[in]  Color processing method. See [ResourceCreate()](/en/docs/common/resourcecreate) function description to learn more about color processing methods.

Return Value

true - successful, otherwise - false

Note

If the first function version is used, the object is created in the main window of the current chart.

Object size coincides with the size of a graphical resource.
