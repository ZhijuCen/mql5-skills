# Attach

Gets the graphical resource from an [OBJ_BITMAP_LABEL](/en/docs/constants/objectconstants/enum_object/obj_bitmap_label) object and attaches it to an instance of the CCanvas class.

```
bool  Attach(
   const long         chart_id,                              // chart identifier
   const string       objname,                               // object name
   ENUM_COLOR_FORMAT  clrfmt=COLOR_FORMAT_XRGB_NOALPHA       // color processing method
  

```

Creates a graphical [resource](/en/docs/runtime/resources) for an [OBJ_BITMAP_LABEL](/en/docs/constants/objectconstants/enum_object/obj_bitmap_label) object and attaches it to an instance of the CCanvas class.

```
bool  Attach(
   const long         chart_id,                              // chart identifier
   const string       objname,                               // object name
   const int          width,                                 // image width in pixels
   const int          height,                                // image height in pixels
   ENUM_COLOR_FORMAT  clrfmt=COLOR_FORMAT_XRGB_NOALPHA       // color processing method
  

```

Parameters

chart_id

[out]  Chart identifier.

objname

[in]  Name of the graphical object.

width

[in]  Image width in the resource.

height

[in]  Image height in the resource.

clrfmt=COLOR_FORMAT_XRGB_NOALPHA

[in]  Alpha channel processing method. The alpha channel is ignored by default.

Return Value

true – if successful, false - if failed to attach the object.
