# DXContextGetColors

Gets an image of a specified size and offset from a graphic context.

```
bool  DXContextGetColors(
   int    context,                       // graphic context handle   
   uint&  image[],                       // image pixels array 
   int    image_width=WHOLE_ARRAY,       // image width in pixels
   int    image_height=WHOLE_ARRAY,      // image height in pixels
   int    image_offset_x=0,              // X offset
   int    image_offset_y=0               // Y offset
   );

```

Parameters

context

[in]  Handle for a graphic context created in [DXContextCreate()](/en/docs/directx/dxcontextcreate).

image

[out]  The array of image_width*image_height pixels in [ARGB](/en/docs/convert/colortoargb) format.

image_width=WHOLE_ARRAY

[in]  Image width in pixels.

image_height=WHOLE_ARRAY

[in]  Image height in pixels.

image_offset_x=0

[in]  X offset.

image_offset_y=0

[in]  Y offset.

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.
