# ResourceSave

Saves a resource into the specified file.

```
bool  ResourceSave(
   const string  resource_name      // Resource name
   const string  file_name          // File name
   );

```

Parameters

resource_name

[in]  The name of the resource, must start with "::".

file_name

[in]  The name of the file relative to MQL5\Files.

Return Value

true – in case of success, otherwise false. For the error information call [GetLastError()](/en/docs/check/getlasterror).

Note

The function always overwrites a file and creates all the required intermediate directories in the file name if necessary.

Example:

```
//--- graphical resource parameters
string ExtResName="Resource";
int    ExtResWidth=100;
int    ExtResHeight=100;
uint   ExtResData[];
int    ExtResSize=ExtResWidth*ExtResHeight;
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   ResetLastError();
//--- set the size of the pixel array
   if(ArrayResize(ExtResData,ExtResSize)!=ExtResSize)
     {
      Print("ArrayResize() failed. Error code: ",GetLastError());
      return;
     }
//--- fill the pixel array with a transparent color and create a graphical resource based on it
   ArrayInitialize(ExtResData,0x00FFFFFF);
   if(!ResourceCreate(ExtResName,ExtResData,ExtResWidth,ExtResHeight,0,0,0,COLOR_FORMAT_ARGB_NORMALIZE))
     {
      Print("ResourceCreate() failed. Error code: ",GetLastError());
      return;
     }
   Print("Size of created recource array: ",ExtResData.Size());
 
//--- check the created graphical resource.
//--- get the time and price data of the current bar
   MqlTick tick={};
   if(!SymbolInfoTick(Symbol(),tick))
     {
      Print("SymbolInfoTick() failed. Error code: ",GetLastError());
      return;
     }
//--- Create the Bitmap object using the coordinates of the last tick price and time
   string obj_name="Bitmap";
   if(!ObjectCreate(0,obj_name,OBJ_BITMAP,0,tick.time,tick.bid))
     {
      Print("ObjectCreate() failed. Error code: ",GetLastError());
      return;
     }
//--- set the width and height of the created bitmap object equal to the width and height of the graphical resource.
//--- set the object anchor point to its center.
   ObjectSetInteger(0,obj_name,OBJPROP_XSIZE,ExtResWidth);
   ObjectSetInteger(0,obj_name,OBJPROP_YSIZE,ExtResHeight);
   ObjectSetInteger(0,obj_name,OBJPROP_ANCHOR,ANCHOR_CENTER);
//--- specify the previously created graphical resource for the bitmap object as an image file
//--- in this case, in order to indicate the name of the graphical resource used, we need to add "::" before its name
   ObjectSetString(0,obj_name,OBJPROP_BMPFILE,"::"+ExtResName);
   
//--- set the GreenYellow color with the transparency of 200
   uint clr=ColorToARGB(clrGreenYellow,200);
//--- fill the entire array of pixels of the graphical resource with the set color
   ArrayInitialize(ExtResData,clr);
//--- draw the grid using DodgerBlue color
   for(int x=0;x<ExtResWidth;x+=9)
      LineVertical(x,0,ExtResHeight,ColorToARGB(clrDodgerBlue,200));
   for(int y=0;y<ExtResHeight;y+=9)
      LineHorizontal(0,ExtResWidth,y,ColorToARGB(clrDodgerBlue,200));
//--- update the graphical resource data
   Update(ExtResName,ExtResData,ExtResWidth,ExtResHeight,true);
   
//--- wait 3 seconds before deleting the resource and graphical object
   Print("Wait 3 seconds before deleting the resource and graphic object");
   Sleep(3000);
 
//--- save the resource to the file
   ResetLastError();
   if(!ResourceSave("::"+ExtResName,"ResourceSave\\"+ExtResName+".bmp"))
     {
      Print("ResourceSave() failed. Error code: ",GetLastError());
      return;
     }
//--- delete the resource and graphic object image
   if(!ResourceFree("::"+ExtResName))
     {
      Print("ResourceFree() failed. Error code: ",GetLastError());
      return;
     }
   if(!ObjectDelete(0,obj_name))
     {
      Print("ObjectDelete() failed. Error code: ",GetLastError());
      return;
     }
 
//--- now create the "Graphical label" object using the coordinates of the price and time of the last tick shifted to the left by the image width
//--- get screen coordinates using the previously received last tick price and time
   int x=0,y=0;
   if(!ChartTimePriceToXY(0,0,tick.time,tick.bid,x,y))
     {
      Print("ChartTimePriceToXY() failed. Error code: ",GetLastError());
      return;
     }
   obj_name="BitmapLabel";
   if(!ObjectCreate(0,obj_name,OBJ_BITMAP_LABEL,0,0,0))
     {
      Print("ObjectCreate() failed. Error code: ",GetLastError());
      return;
     }
//--- set the object anchor point to its center.
   ObjectSetInteger(0,obj_name,OBJPROP_ANCHOR,ANCHOR_CENTER);
//--- set the coordinates of the price and time of the last tick, shifted to the left by the image width, to the graphical label object
   ObjectSetInteger(0,obj_name,OBJPROP_XDISTANCE,x-ExtResWidth);
   ObjectSetInteger(0,obj_name,OBJPROP_YDISTANCE,y);
//--- specify the resource, previously saved as a bmp image, for the graphical label object as an image file
   ObjectSetString(0,obj_name,OBJPROP_BMPFILE,"\\Files\\ResourceSave\\"+ExtResName+".bmp");
//--- update the chart
   ChartRedraw();
   
//--- wait 3 seconds before deleting the graphical label object
   Print("Wait 3 seconds before deleting the new graphic object");
   Sleep(3000);
   if(!ObjectDelete(0,obj_name))
      Print("ObjectDelete() failed. Error code: ",GetLastError());
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
//+------------------------------------------------------------------+
//| Draw a vertical line                                             |
//+------------------------------------------------------------------+
void LineVertical(int x,int y1,int y2,const uint clr)
  {
   int tmp;
//--- sort by Y
   if(y1>y2)
     {
      tmp=y1;
      y1 =y2;
      y2 =tmp;
     }
//--- line outside the image boundaries
   if(y2<0 || y1>=ExtResHeight || x<0 || x>=ExtResWidth)
      return;
//--- stay within the image boundaries
   if(y1<0)
      y1=0;
   if(y2>=ExtResHeight)
      y2=ExtResHeight-1;
//--- draw the line
   int index=y1*ExtResWidth+x;
   for(int i=y1; i<=y2; i++,index+=ExtResWidth)
      ExtResData[index]=clr;
  }
//+------------------------------------------------------------------+
//| Draw a horizontal line                                           |
//+------------------------------------------------------------------+
void LineHorizontal(int x1,int x2,int y,const uint clr)
  {
   int tmp;
//--- sort by X
   if(x1>x2)
     {
      tmp=x1;
      x1 =x2;
      x2 =tmp;
     }
//--- line outside the image boundaries
   if(x2<0 || x1>=ExtResWidth || y<0 || y>=ExtResHeight)
      return;
//--- stay within the image boundaries
   if(x1<0)
      x1=0;
   if(x2>=ExtResWidth)
      x2=ExtResWidth-1;
//--- draw the line
   ArrayFill(ExtResData,y*ExtResWidth+x1,(x2-x1)+1,clr);
  }

```

See also

[Resources](/en/docs/runtime/resources), [ObjectCreate()](/en/docs/objects/objectcreate), [PlaySound()](/en/docs/common/playsound), [ObjectSetString()](/en/docs/objects/objectsetstring), [OBJPROP_BMPFILE](/en/docs/constants/objectconstants/enum_object_property#enum_object_property_string)
