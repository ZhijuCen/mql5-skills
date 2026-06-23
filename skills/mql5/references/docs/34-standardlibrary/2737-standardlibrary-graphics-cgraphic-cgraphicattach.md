# Attach

The version for getting a graphical resource from the OBJ_BITMAP_LABEL object and binding it to the CGraphic class instance:

```
bool  Attach(
   const long    chart_id,     // chart ID
   const string  objname       // graphical object name 
   )

```

The version for creating a graphical resource for the OBJ_BITMAP_LABEL object and binding it to the CGraphic class instance:

```
bool  Attach(
   const long    chart_id,     // chart ID
   const string  objname,      // graphical object name
   const int     width,        // image width 
   const int     height        // image height
   )

```

Parameters

chart_id

[in]  Chart ID.

objname

[in]  Name of the graphical object.

width

[in]  Image width in the resource.

height

[in]  Image height in the resource.

Return Value

true — successful, false — failed to bind the object.
