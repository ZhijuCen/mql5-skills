# ResourceFree

The function deletes [dynamically created resource](/en/docs/common/resourcecreate#dynamic_resourcecreate) (freeing the memory allocated for it).

```
bool  ResourceFree(
   const string  resource_name      // resource name
   );

```

Parameters

resource_name

[in]  [Resource](/en/docs/runtime/resources) name should start with "::".

Return Value

True if successful, otherwise false. To get information about the error, call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

ResourceFree() allows mql5 application developers to manage memory consumption when actively working with resources. [Graphical objects](/en/docs/objects) bound to the resource being deleted from the memory will be displayed correctly after its deletion. However, newly created graphical objects ([OBJ_BITMAP](/en/docs/constants/objectconstants/enum_object/obj_bitmap) and [OBJ_BITMAP_LABEL](/en/docs/constants/objectconstants/enum_object/obj_bitmap_label)) will not be able to use the deleted resource.

The function deletes only dynamic resources created by the program.

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
//--- in this case, in order to indicate the name of the graphical resource used, we need to add "::" before its name
   ObjectSetString(0,obj_name,OBJPROP_BMPFILE,"::"+rc_name);
   
//--- set the DodgerBlue color with the transparency of 200
   uint clr=ColorToARGB(clrDodgerBlue,200);
//--- fill the entire array of pixels of the graphical resource with the set color
   ArrayInitialize(rc_data,clr);
//--- update the graphical resource data
   Update(rc_name,rc_data,rc_width,rc_height,true);
   
//--- wait three seconds and change the image color
   Print("Wait 3 seconds before changing color");
   Sleep(3000);
//--- set the OrangeRed color with the transparency of 200
   Print("Change color");
   clr=ColorToARGB(clrOrangeRed,200);
//--- fill the entire array of pixels of the graphical resource with the set color
   ArrayInitialize(rc_data,clr);
//--- update the graphical resource data
   Update(rc_name,rc_data,rc_width,rc_height,true);
   
//--- wait three seconds and release the graphical resource
   Print("Wait 3 seconds before ResourceFree()");
   Sleep(3000);
   bool res=ResourceFree("::"+rc_name);
   Print("ResourceFree: ",res);
 
//--- try changing the color after releasing the resource
   Print("Trying to change color to GreenYellow after ResourceFree()");
//--- set the GreenYellow color with the transparency of 200
   clr=ColorToARGB(clrGreenYellow,200);
//--- fill the entire array of pixels of the graphical resource with the set color
   ArrayInitialize(rc_data,clr);
//--- update the graphical resource data (the image remains, but the color cannot be changed)
   Update(rc_name,rc_data,rc_width,rc_height,true);
   Print("The color has not changed because the resource has been released");
   
//--- wait three seconds and delete the bitmap object
   Print("Wait 3 seconds before deleting the Bitmap object");
   Sleep(3000);
   Print("Delete Bitmap object");
   ObjectDelete(0,obj_name);
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

[Resources](/en/docs/runtime/resources), [ObjectCreate()](/en/docs/objects/objectcreate), [PlaySound()](/en/docs/common/playsound), [ObjectSetString()](/en/docs/objects/objectsetstring), [OBJPROP_BMPFILE](/en/docs/constants/objectconstants/enum_object_property#enum_object_property_string)
