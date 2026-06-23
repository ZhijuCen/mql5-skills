# Attach

Gets the graphical resource from an [OBJ_BITMAP_LABEL](/en/docs/constants/objectconstants/enum_object/obj_bitmap_label) object and attaches it to an instance of the CCanvas class.

```
bool  Attach(
   const long         chart_id,                              // chart ID
   const string       objname,                               // object name
   ENUM_COLOR_FORMAT  clrfmt=COLOR_FORMAT_XRGB_NOALPHA       // color handling method 
   )

```

Creates a graphical [resource](/en/docs/runtime/resources) for an [OBJ_BITMAP_LABEL](/en/docs/constants/objectconstants/enum_object/obj_bitmap_label) object and attaches it to an instance of the CCanvas class.

```
bool  Attach(
   const long         chart_id,                              // chart ID
   const string       objname,                               // object name
   const int          width,                                 // image width in pixels
   const int          height,                                // image height in pixels
   ENUM_COLOR_FORMAT  clrfmt=COLOR_FORMAT_XRGB_NOALPHA       // color handling method 
   )

```

Parameters

chart_id

[in]  Chart ID.

objname

[in]  Name of the graphical object.

width

[in]  Frame width in a resource.

height

[in]  Frame height.

clrfmt=COLOR_FORMAT_XRGB_NOALPHA

[in]  Color handling method. See [ResourceCreate()](/en/docs/common/resourcecreate) function description to learn more about color handling methods.

Note

true – if successful, false - if failed to add a graphic object.
