# CreateBitmap

Creates a graphical resource bound to a chart object.

1. Creates a graphical resource in the main window of the current chart.

```
bool  CreateBitmap(
   const string       name,                                 // name
   const datetime     time,                                 // time
   const double       price,                                // price
   const int          width,                                // width
   const int          height,                               // height
   ENUM_COLOR_FORMAT  clrfmt=COLOR_FORMAT_XRGB_NOALPHA      // format
   );

```

2. Creates a graphical resource using a chart ID and a subwindow number.

```
bool  CreateBitmap(
   const long         chart_id,                             // chart ID
   const int          subwin,                               // subwindow number
   const string       name,                                 // name
   const datetime     time,                                 // time
   const double       price,                                // price
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

time

[in]  Chart object anchor point time coordinate.

price

[in]  Chart object anchor point price coordinate.

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
