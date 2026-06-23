# Create

Creates a graphical resource without binding to a chart object.

```
virtual bool  Create(
   const string       name,                                 // name
   const int          width,                                // width
   const int          height,                               // height
   ENUM_COLOR_FORMAT  clrfmt=COLOR_FORMAT_XRGB_NOALPHA      // format
   );

```

Parameters

name

[in]  Basis for a graphical resource name. A resource name is generated during the creation by adding a pseudorandom string.

width

[in]  Width (size along X axis) in pixels.

height

[in]  Height (size along Y axis) in pixels.

clrfmt=COLOR_FORMAT_XRGB_NOALPHA

[in]  Color processing method. See [ResourceCreate()](/en/docs/common/resourcecreate) function description to learn more about color processing methods.

Return Value

true - successful, otherwise - false
