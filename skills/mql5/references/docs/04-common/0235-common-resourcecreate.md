# ResourceCreate

Creates an image resource based on a data set. There are two variants of the function:  

Creating a resource based on a file

```
bool  ResourceCreate(
   const string      resource_name,       // Resource name
   const string      path                 // A relative path to the file
   );

```

Creating a resource based on the array of pixels

```
bool  ResourceCreate(
   const string      resource_name,       // Resource name
   const uint&       data[],              // Data set as an array
   uint              img_width,           // The width of the image resource
   uint              img_height,          // The height of the image resource
   uint              data_xoffset,        // The horizontal rightward offset of the upper left corner of the image
   uint              data_yoffset,        // The vertical downward offset of the upper left corner of the image
   uint              data_width,          // The total width of the image based on the data set
   ENUM_COLOR_FORMAT color_format         // Color processing method
   );

```

Parameters

resource_name

[in]  Resource name.

data[][]

[in]  A one-dimensional or two-dimensional array for creating a complete image.

img_width

[in]  The width of the rectangular image area in pixels to be placed in the resource in the form of an image. It cannot be greater than the data_width value.

img_height

[in]  The height of the rectangular image area in pixels to be placed in the resource in the form of an image.

data_xoffset

[in]  The horizontal rightward offset of the rectangular area of the image.

data_yoffset

[in]  The vertical downward offset of the rectangular area of the image.

data_width

[in]  Required only for one-dimensional arrays. It denotes the full width of the image from the data set. If data_width=0, it is assumed to be equal to img_width. For two-dimensional arrays the parameter is ignored and is assumed to be equal to the second dimension of the data[] array.

color_format

[in]  Color processing method, from a value from the [ENUM_COLOR_FORMAT](/en/docs/common/resourcecreate#enum_color_format) enumeration.

Return Value

Returns true if successful, otherwise false. To get information about the error call the [GetLastError()](/en/docs/check/getlasterror) function. The following errors may occur:

- 4015 – ERR_RESOURCE_NAME_DUPLICATED (identical names of the dynamic and the [static](/en/docs/runtime/resources) resource)
- 4016 – ERR_RESOURCE_NOT_FOUND (the resource is not found)
- 4017 – ERR_RESOURCE_UNSUPPORTED_TYPE (this type of resource is not supported)
- 4018 – ERR_RESOURCE_NAME_IS_TOO_LONG (the name of the resource is too long)

Note

If the second version of the function is called for creating the same resource with different width, height and shift parameters, it does not create a new resource, but simply updates the existing one.

The first version of the function is used for uploading images and sounds from files, and the second version is used only for the dynamic creation of images.

Images must be in the BMP format with a color depth of 24 or 32 bits. Sounds can only be in the WAV format. The size of the resource should not exceed 16 Mb.

ENUM_COLOR_FORMAT

| Identifier | Description |
| --- | --- |
| COLOR_FORMAT_XRGB_NOALPHA | The component of the alpha channel is ignored |
| COLOR_FORMAT_ARGB_RAW | Color components are not handled by the terminal (must be correctly set by the user in premultiplied ARGB format). Use the  ColorToPRGB  function to convert color to premultiplied ARGB |
| COLOR_FORMAT_ARGB_NORMALIZE | Color components are handled by the terminal |

Example:

```
//+------------------------------------------------------------------+
//| Update graphical resource data                                   |
//+------------------------------------------------------------------+
void Update(const string res_name,const uint &pixel_data[],const uint width,const uint height,const bool redraw)
  {
//--- leave if zero dimensions are passed
   if(width==0 || height==0)
      return;
//--- Update resource data and redraw the chart
   if(ResourceCreate(res_name,pixel_data,width,height,0,0,0,COLOR_FORMAT_ARGB_NORMALIZE) && redraw)
      ChartRedraw();
  }
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare the parameters of the graphical resource
   string rc_name="Resource";
   uint   rc_width=100;
   uint   rc_height=100;
   uint   rc_data[];
   uint   rc_size=rc_width*rc_height;
 
   ResetLastError();
//--- set the size of the pixel array
   if(ArrayResize(rc_data,rc_size)!=rc_size)
     {
      Print("ArrayResize() failed. Error code: ",GetLastError());
      return;
     }
//--- fill the pixel array with a transparent color and create a graphical resource based on it
   ArrayInitialize(rc_data,0x00FFFFFF);
   if(!ResourceCreate(rc_name,rc_data,rc_width,rc_height,0,0,0,COLOR_FORMAT_ARGB_NORMALIZE))
     {
      Print("ResourceCreate() failed. Error code: ",GetLastError());
      return;
     }
   Print("Size of created recource array: ",rc_data.Size());
 
//--- check the created graphical resource.
//--- get the time and price data of the current bar
   MqlTick tick={};
   if(!SymbolInfoTick(Symbol(),tick))
     {
      Print("SymbolInfoTick() failed. Error code: ",GetLastError());
      return;
     }
//--- create the Bitmap object using the coordinates of the last tick price and time
   string obj_name="Bitmap";
   if(!ObjectCreate(0,obj_name,OBJ_BITMAP,0,tick.time,tick.bid))
     {
      Print("ObjectCreate() failed. Error code: ",GetLastError());
      return;
     }
//--- set the width and height of the created bitmap object equal to the width and height of the graphical resource.
//--- set the object anchor point to its center.
   ObjectSetInteger(0,obj_name,OBJPROP_XSIZE,rc_width);
   ObjectSetInteger(0,obj_name,OBJPROP_YSIZE,rc_height);
   ObjectSetInteger(0,obj_name,OBJPROP_ANCHOR,ANCHOR_CENTER);
//--- specify the previously created graphical resource for the bitmap object as an image file
//--- in this case, in order to indicate the name of the graphical resource used, we need to add "::" before its name
   ObjectSetString(0,obj_name,OBJPROP_BMPFILE,"::"+rc_name);
   
//--- set the DodgerBlue color with the transparency of 200
   uint clr=ColorToARGB(clrDodgerBlue,200);
//--- fill the entire array of pixels of the graphical resource with the set color
   ArrayInitialize(rc_data,clr);
//--- update the graphical resource data
   Update(rc_name,rc_data,rc_width,rc_height,true);
  }

```

See also

[Resources](/en/docs/runtime/resources), [ObjectCreate()](/en/docs/objects/objectcreate), [ObjectSetString()](/en/docs/objects/objectsetstring), [OBJPROP_BMPFILE](/en/docs/constants/objectconstants/enum_object_property#enum_object_property_string)
