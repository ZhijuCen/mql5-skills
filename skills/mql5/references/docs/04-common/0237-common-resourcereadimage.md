# ResourceReadImage

The function reads data from the graphical resource [created by ResourceCreate() function](/en/docs/common/resourcecreate#dynamic_resourcecreate) or [saved in EX5 file during compilation](/en/docs/runtime/resources#resource_include).

```
bool  ResourceReadImage(
   const string      resource_name,       // graphical resource name for reading
   uint&             data[],              // array for receiving data from the resource
   uint&             width,               // for receiving the image width in the resource
   uint&             height,              // for receiving the image height in the resource
   );

```

Parameters

resource_name

[in]  Name of the graphical resource containing an image. To gain access to its own resources, the name is used in brief form "::resourcename". If we download a resource from a compiled EX5 file, the full name should be used with the path relative to MQL5 directory, file and resource names – "path\\filename.ex5::resourcename".

data[][]

[in]  One- or two-dimensional array for receiving data from the graphical resource.

img_width

[out]  Graphical resource image width in pixels.

img_height

[out]  Graphical resource image height in pixels.

Return Value

true if successful, otherwise false. To get information about the error, call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

If data[] array is then to be used for [creating a graphical resource](/en/docs/common/resourcecreate#enum_color_format), [ COLOR_FORMAT_ARGB_NORMALIZE or COLOR_FORMAT_XRGB_NOALPHA](/en/docs/common/resourcecreate#enum_color_format) color formats should be used.

If data[] array is two-dimensional and its second dimension is less than X(width) graphical resource size, ResourceReadImage() function returns false and reading is not performed. But if the resource exists, actual image size is returned to width and height parameters.  This will allow making another attempt to receive data from the resource.

Example:

```
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
//--- In this case, in order to indicate the name of the graphical resource used, we need to add "::" before its name
   ObjectSetString(0,obj_name,OBJPROP_BMPFILE,"::"+rc_name);
   
//--- set the DodgerBlue color with the transparency of 200
   uint clr=ColorToARGB(clrDodgerBlue,200);
//--- fill the entire array of pixels of the graphical resource with the set color
   ArrayInitialize(rc_data,clr);
//--- update the graphical resource data
   Update(rc_name,rc_data,rc_width,rc_height,true);
   
//--- wait 3 seconds before reading the graphical resource data 
   Print("Wait 3 seconds before ResourceReadImage()");
   Sleep(3000);
//--- read the image from the resource into a new array of pixels
   uint rc_data_copy[];
   uint w=0,h=0;
   ResetLastError();
   if(!ResourceReadImage("::"+rc_name,rc_data_copy,w,h))
     {
      Print("ResourceReadImage() failed. Error code: ",GetLastError());
      return;
     }
 
//--- set the OrangeRed color with the transparency of 200
   clr=ColorToARGB(clrOrangeRed,200);
//--- fill the entire array of pixels of the graphical resource with the set color and create a new graphical resource based on it
   ArrayInitialize(rc_data_copy,clr);
   if(!ResourceCreate(rc_name+"Copy",rc_data_copy,rc_width,rc_height,0,0,0,COLOR_FORMAT_ARGB_NORMALIZE))
     {
      Print("New ResourceCreate() failed. Error code: ",GetLastError());
      return;
     }
   Print("Size of created new recource array: ",rc_data_copy.Size());
   
//--- create the "Graphical label" object using the coordinates of the last tick price and time
   string obj_name2="BitmapLabel";
   if(!ObjectCreate(0,obj_name2,OBJ_BITMAP_LABEL,0,0,0))
     {
      Print("ObjectCreate() failed. Error code: ",GetLastError());
      return;
     }
//--- get screen coordinates using the previously received price and time
   int x=0,y=0;
   if(!ChartTimePriceToXY(0,0,tick.time,tick.bid,x,y))
     {
      Print("New ChartTimePriceToXY() failed. Error code: ",GetLastError());
      return;
     }
//--- set the width and height of the created graphical label object equal to the width and height of the graphical resource.
//--- set the object anchor point to its center.
   ObjectSetInteger(0,obj_name2,OBJPROP_XSIZE,rc_width);
   ObjectSetInteger(0,obj_name2,OBJPROP_YSIZE,rc_height);
   ObjectSetInteger(0,obj_name2,OBJPROP_ANCHOR,ANCHOR_LEFT_UPPER);
   ObjectSetInteger(0,obj_name2,OBJPROP_XDISTANCE,x);
   ObjectSetInteger(0,obj_name2,OBJPROP_YDISTANCE,y);
//--- set the copied graphical resource as an image file for the graphical label object
//--- in this case, in order to indicate the name of the graphical resource used, we need to add "::" before its name
   ObjectSetString(0,obj_name2,OBJPROP_BMPFILE,"::"+rc_name+"Copy");
   
//--- change the color of the new graphical label object
   Print("Wait 3 seconds before changing color to GreenYellow");
   Sleep(3000);
//--- set the GreenYellow color with the transparency of 200
   clr=ColorToARGB(clrGreenYellow,200);
//--- fill the entire array of pixels of the new graphical resource with the set color
   ArrayInitialize(rc_data_copy,clr);
//--- update the graphical resource data 
   Update(rc_name+"Copy",rc_data_copy,rc_width,rc_height,true);
   
//--- wait three seconds and delete resources and both objects
   Print("Wait 3 seconds before deleting both objects");
   Sleep(3000);
   Print("Deleting Resource and all Bitmap objects");
   ResourceFree("::"+rc_name);
   ResourceFree("::"+rc_name+"Copy");
   ObjectDelete(0,obj_name);
   ObjectDelete(0,obj_name2);
  }
//+------------------------------------------------------------------+
//| Update graphical resource data                                   |
//+------------------------------------------------------------------+
void Update(const string res_name,const uint &pixel_data[],const uint width,const uint height,const bool redraw)
  {
//--- leave if zero dimensions are passed
   if(width==0 || height==0)
      return;
//--- update resource data and redraw the chart
   if(ResourceCreate(res_name,pixel_data,width,height,0,0,0,COLOR_FORMAT_ARGB_NORMALIZE) && redraw)
      ChartRedraw();
  }

```

See also

[Resource](/en/docs/runtime/resources), [ObjectCreate()](/en/docs/objects/objectcreate), [ObjectSetString()](/en/docs/objects/objectsetstring), [OBJPROP_BMPFILE](/en/docs/constants/objectconstants/enum_object_property#enum_object_property_string)
