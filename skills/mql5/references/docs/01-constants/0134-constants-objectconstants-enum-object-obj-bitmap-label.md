# OBJ_BITMAP_LABEL

Bitmap Label object.

![Note](pics/objbitmaplabel.png)

Note

Anchor point position relative to the label can be selected from [ENUM_ANCHOR_POINT](/en/docs/constants/objectconstants/enum_anchorpoint) enumeration. Anchor point coordinates are set in pixels.

You can also select bitmap anchoring corner from [ENUM_BASE_CORNER](/en/docs/constants/objectconstants/enum_basecorner) enumeration.

For bitmap label, you can select [visibility scope](/en/docs/constants/objectconstants/enum_object_property#visual_rectangle) of an image.

Example

The following script creates several bitmaps on the chart. Special functions have been developed to create and change graphical object's properties. You can use these functions "as is" in your own applications.

```
//--- description
#property description "Script creates \"Bitmap Label\" object."
//--- display window of the input parameters during the script's launch
#property script_show_inputs
//--- input parameters of the script
input string            InpName="BmpLabel";               // Label name
input string            InpFileOn="\\Images\\dollar.bmp"; // File name for On mode
input string            InpFileOff="\\Images\\euro.bmp";  // File name for Off mode
input bool              InpState=false;                   // Label pressed/released
input ENUM_BASE_CORNER  InpCorner=CORNER_LEFT_UPPER;      // Chart corner for anchoring
input ENUM_ANCHOR_POINT InpAnchor=ANCHOR_CENTER;          // Anchor type
input color             InpColor=clrRed;                  // Border color when highlighted
input ENUM_LINE_STYLE   InpStyle=STYLE_SOLID;             // Line style when highlighted
input int               InpPointWidth=1;                  // Point size to move
input bool              InpBack=false;                    // Background object
input bool              InpSelection=false;               // Highlight to move
input bool              InpHidden=true;                   // Hidden in the object list
input long              InpZOrder=0;                      // Priority for mouse click
//+------------------------------------------------------------------+
//| Create Bitmap Label object                                       |
//+------------------------------------------------------------------+
bool BitmapLabelCreate(const long              chart_ID=0,               // chart's ID
                       const string            name="BmpLabel",          // label name
                       const int               sub_window=0,             // subwindow index
                       const int               x=0,                      // X coordinate
                       const int               y=0,                      // Y coordinate
                       const string            file_on="",               // image in On mode
                       const string            file_off="",              // image in Off mode
                       const int               width=0,                  // visibility scope X coordinate
                       const int               height=0,                 // visibility scope Y coordinate
                       const int               x_offset=10,              // visibility scope shift by X axis
                       const int               y_offset=10,              // visibility scope shift by Y axis
                       const bool              state=false,              // pressed/released
                       const ENUM_BASE_CORNER  corner=CORNER_LEFT_UPPER, // chart corner for anchoring
                       const ENUM_ANCHOR_POINT anchor=ANCHOR_LEFT_UPPER, // anchor type 
                       const color             clr=clrRed,               // border color when highlighted
                       const ENUM_LINE_STYLE   style=STYLE_SOLID,        // line style when highlighted
                       const int               point_width=1,            // move point size
                       const bool              back=false,               // in the background
                       const bool              selection=false,          // highlight to move
                       const bool              hidden=true,              // hidden in the object list
                       const long              z_order=0)                // priority for mouse click
  {
//--- reset the error value
   ResetLastError();
//--- create a bitmap label
   if(!ObjectCreate(chart_ID,name,OBJ_BITMAP_LABEL,sub_window,0,0))
     {
      Print(__FUNCTION__,
            ": failed to create \"Bitmap Label\" object! Error code = ",GetLastError());
      return(false);
     }
//--- set the images for On and Off modes
   if(!ObjectSetString(chart_ID,name,OBJPROP_BMPFILE,0,file_on))
     {
      Print(__FUNCTION__,
            ": failed to load the image for On mode! Error code = ",GetLastError());
      return(false);
     }
   if(!ObjectSetString(chart_ID,name,OBJPROP_BMPFILE,1,file_off))
     {
      Print(__FUNCTION__,
            ": failed to load the image for Off mode! Error code = ",GetLastError());
      return(false);
     }
//--- set label coordinates
   ObjectSetInteger(chart_ID,name,OBJPROP_XDISTANCE,x);
   ObjectSetInteger(chart_ID,name,OBJPROP_YDISTANCE,y);
//--- set visibility scope for the image; if width or height values
//--- exceed the width and height (respectively) of a source image,
//--- it is not drawn; in the opposite case,
//--- only the part corresponding to these values is drawn
   ObjectSetInteger(chart_ID,name,OBJPROP_XSIZE,width);
   ObjectSetInteger(chart_ID,name,OBJPROP_YSIZE,height);
//--- set the part of an image that is to be displayed in the visibility scope
//--- the default part is the upper left area of an image; the values allow
//--- performing a shift from this area displaying another part of the image
   ObjectSetInteger(chart_ID,name,OBJPROP_XOFFSET,x_offset);
   ObjectSetInteger(chart_ID,name,OBJPROP_YOFFSET,y_offset);
//--- define the label's status (pressed or released)
   ObjectSetInteger(chart_ID,name,OBJPROP_STATE,state);
//--- set the chart's corner, relative to which point coordinates are defined
   ObjectSetInteger(chart_ID,name,OBJPROP_CORNER,corner);
//--- set anchor type
   ObjectSetInteger(chart_ID,name,OBJPROP_ANCHOR,anchor);
//--- set the border color when object highlighting mode is enabled
   ObjectSetInteger(chart_ID,name,OBJPROP_COLOR,clr);
//--- set the border line style when object highlighting mode is enabled
   ObjectSetInteger(chart_ID,name,OBJPROP_STYLE,style);
//--- set a size of the anchor point for moving an object
   ObjectSetInteger(chart_ID,name,OBJPROP_WIDTH,point_width);
//--- display in the foreground (false) or background (true)
   ObjectSetInteger(chart_ID,name,OBJPROP_BACK,back);
//--- enable (true) or disable (false) the mode of moving the label by mouse
   ObjectSetInteger(chart_ID,name,OBJPROP_SELECTABLE,selection);
   ObjectSetInteger(chart_ID,name,OBJPROP_SELECTED,selection);
//--- hide (true) or display (false) graphical object name in the object list
   ObjectSetInteger(chart_ID,name,OBJPROP_HIDDEN,hidden);
//--- set the priority for receiving the event of a mouse click in the chart
   ObjectSetInteger(chart_ID,name,OBJPROP_ZORDER,z_order);
//--- successful execution
   return(true);
  }
//+------------------------------------------------------------------+
//| Set a new image for Bitmap label object                          |
//+------------------------------------------------------------------+
bool BitmapLabelSetImage(const long   chart_ID=0,      // chart's ID
                         const string name="BmpLabel", // label name
                         const int    on_off=0,        // modifier (On or Off)
                         const string file="")         // path to the file
  {
//--- reset the error value
   ResetLastError();
//--- set the path to the image file
   if(!ObjectSetString(chart_ID,name,OBJPROP_BMPFILE,on_off,file))
     {
      Print(__FUNCTION__,
            ": failed to load the image! Error code = ",GetLastError());
      return(false);
     }
//--- successful execution
   return(true);
  }
//+------------------------------------------------------------------+
//| Move Bitmap Label object                                         |
//+------------------------------------------------------------------+
bool BitmapLabelMove(const long   chart_ID=0,      // chart's ID
                     const string name="BmpLabel", // label name
                     const int    x=0,             // X coordinate
                     const int    y=0)             // Y coordinate
  {
//--- reset the error value
   ResetLastError();
//--- move the object
   if(!ObjectSetInteger(chart_ID,name,OBJPROP_XDISTANCE,x))
     {
      Print(__FUNCTION__,
            ": failed to move X coordinate of the object! Error code = ",GetLastError());
      return(false);
     }
   if(!ObjectSetInteger(chart_ID,name,OBJPROP_YDISTANCE,y))
     {
      Print(__FUNCTION__,
            ": failed to move Y coordinate of the object! Error code = ",GetLastError());
      return(false);
     }
//--- successful execution
   return(true);
  }
//+------------------------------------------------------------------+
//| Change visibility scope (object) size                            |
//+------------------------------------------------------------------+
bool BitmapLabelChangeSize(const long   chart_ID=0,      // chart's ID
                           const string name="BmpLabel", // label name
                           const int    width=0,         // label width
                           const int    height=0)        // label height
  {
//--- reset the error value
   ResetLastError();
//--- change the object size
   if(!ObjectSetInteger(chart_ID,name,OBJPROP_XSIZE,width))
     {
      Print(__FUNCTION__,
            ": failed to change the object width! Error code = ",GetLastError());
      return(false);
     }
   if(!ObjectSetInteger(chart_ID,name,OBJPROP_YSIZE,height))
     {
      Print(__FUNCTION__,
            ": failed to change the object height! Error code = ",GetLastError());
      return(false);
     }
//--- successful execution
   return(true);
  }
//+--------------------------------------------------------------------+
//| Change coordinate of the upper left corner of the visibility scope |
//+--------------------------------------------------------------------+
bool BitmapLabelMoveVisibleArea(const long   chart_ID=0,      // chart's ID
                                const string name="BmpLabel", // label name
                                const int    x_offset=0,      // visibility scope X coordinate
                                const int    y_offset=0)      // visibility scope Y coordinate
  {
//--- reset the error value
   ResetLastError();
//--- change the object's visibility scope coordinates
   if(!ObjectSetInteger(chart_ID,name,OBJPROP_XOFFSET,x_offset))
     {
      Print(__FUNCTION__,
            ": failed to change X coordinate of the visibility scope! Error code = ",GetLastError());
      return(false);
     }
   if(!ObjectSetInteger(chart_ID,name,OBJPROP_YOFFSET,y_offset))
     {
      Print(__FUNCTION__,
            ": failed to change Y coordinate of the visibility scope! Error code = ",GetLastError());
      return(false);
     }
//--- successful execution
   return(true);
  }
//+------------------------------------------------------------------+
//| Delete "Bitmap label" object                                     |
//+------------------------------------------------------------------+
bool BitmapLabelDelete(const long   chart_ID=0,      // chart's ID
                       const string name="BmpLabel") // label name
  {
//--- reset the error value
   ResetLastError();
//--- delete the label
   if(!ObjectDelete(chart_ID,name))
     {
      Print(__FUNCTION__,
            ": failed to delete \"Bitmap label\" object! Error code = ",GetLastError());
      return(false);
     }
//--- successful execution
   return(true);
  }
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- chart window size
   long x_distance;
   long y_distance;
//--- set window size
   if(!ChartGetInteger(0,CHART_WIDTH_IN_PIXELS,0,x_distance))
     {
      Print("Failed to get the chart width! Error code = ",GetLastError());
      return;
     }
   if(!ChartGetInteger(0,CHART_HEIGHT_IN_PIXELS,0,y_distance))
     {
      Print("Failed to get the chart height! Error code = ",GetLastError());
      return;
     }
//--- define bitmap label coordinates
   int x=(int)x_distance/2;
   int y=(int)y_distance/2;
//--- set label size and visibility scope coordinates
   int width=32;
   int height=32;
   int x_offset=0;
   int y_offset=0;
//--- place bitmap label at the center of the window
   if(!BitmapLabelCreate(0,InpName,0,x,y,InpFileOn,InpFileOff,width,height,x_offset,y_offset,InpState,
      InpCorner,InpAnchor,InpColor,InpStyle,InpPointWidth,InpBack,InpSelection,InpHidden,InpZOrder))
     {
      return;
     }
//--- redraw the chart and wait one second
   ChartRedraw();
   Sleep(1000);
//--- change label's visibility scope size in the loop
   for(int i=0;i<6;i++)
     {
      //--- change visibility scope size
      width--;
      height--;
      if(!BitmapLabelChangeSize(0,InpName,width,height))
         return;
      //--- check if the script's operation has been forcefully disabled
      if(IsStopped())
         return;
      //--- redraw the chart
      ChartRedraw();
      // 0.3 seconds of delay
      Sleep(300);
     }
//--- 1 second of delay
   Sleep(1000);
//--- change label's visibility scope coordinates in the loop
   for(int i=0;i<2;i++)
     {
      //--- change visibility scope coordinates
      x_offset++;
      y_offset++;
      if(!BitmapLabelMoveVisibleArea(0,InpName,x_offset,y_offset))
         return;
      //--- check if the script's operation has been forcefully disabled
      if(IsStopped())
         return;
      //--- redraw the chart
      ChartRedraw();
      // 0.3 seconds of delay
      Sleep(300);
     }
//--- 1 second of delay
   Sleep(1000);
//--- delete the label
   BitmapLabelDelete(0,InpName);
   ChartRedraw();
//--- 1 second of delay
   Sleep(1000);
//---
  }

```
