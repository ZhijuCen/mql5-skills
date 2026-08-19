# Create

Virtual method that creates a graphical resource.

```
 virtual bool  Create(
   const string       name,    // name
   const int          width,   // width
   const int          height,  // height
   ENUM_COLOR_FORMAT  clrfmt,  // format
   )

```

Parameters

name

[in] Basis for a graphical resource name. A resource name is generated during the creation by adding a pseudorandom string.

width

[in]  Width (size along X axis) in pixels.

height

[in]  Height (size along Y axis) in pixels.

clrfmt

[in]  Color processing method. See the ResourceCreate() function description to learn more about color processing methods.

Return Value

true if successful, otherwise — false.
