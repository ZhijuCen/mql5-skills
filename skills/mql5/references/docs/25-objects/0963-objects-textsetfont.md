# TextSetFont

The function sets the font for displaying the text using drawing methods and returns the result of that operation. Arial font with the size -120 (12 pt) is used by default.

```
bool  TextSetFont(
   const string  name,            // font name or path to font file on the disk
   int           size,            // font size
   uint          flags,           // combination of flags
   int           orientation=0    // text slope angle
   );

```

Parameters

name

[in]  Font name in the system or the name of the resource containing the font or the path to font file on the disk.

size

[in]  The font size that can be set using positive and negative values. In case of positive values, the size of a displayed text does not depend on the operating system's font size settings. In case of negative values, the value is set in tenths of a point and the text size depends on the operating system settings ("standard scale" or "large scale"). See the Note below for more information about the differences between the modes.

flags

[in]  Combination of [flags](/en/docs/objects/textsetfont#font_type_flags) describing font style.

orientation

[in]  Text's horizontal inclination to X axis, the unit of measurement is 0.1 degrees. It means that orientation=450 stands for inclination equal to 45 degrees.

Return Value

Returns true if the current font is successfully installed, otherwise false. Possible code errors:

- ERR_INVALID_PARAMETER(4003) - name presents NULL or "" (empty string),
- ERR_INTERNAL_ERROR(4001) - operating system error (for example, an attempt to create a non-existent font).

Note

If "::" is used in font name, the font is downloaded from [EX5 resource](/en/docs/runtime/resources). If name font name is specified with an extension, the font is downloaded from the file, if the path starts from "\" or "/", the file is searched relative to MQL5 directory. Otherwise, it is searched relative to the path of EX5 file which called TextSetFont() function.

The font size is set using positive or negative values. This fact defines the dependence of the text size from the operating system settings (size scale).

- If the size is specified using a positive number, this size is transformed into physical measurement units of a device (pixels) when changing a logical font into a physical one, and this size corresponds to the height of the symbol glyphs picked from the available fonts. This case is not recommended when the texts displayed by [TextOut()](/en/docs/objects/textout) function and the ones displayed by [OBJ_LABEL](/en/docs/constants/objectconstants/enum_object) ("Label") graphical object are to be used together on the chart.
- If the size is specified using a negative number, this number is supposed to be set in tenths of a logical point and is divided by 10 (for example, -350 is equal to 35 logical points). An obtained value is then transformed into physical measurement units of a device (pixels) and corresponds to the absolute value of the height of a symbol picked from the available fonts. Multiply the font size specified in the object properties by -10 to make the size of a text on the screen similar to the one in [OBJ_LABEL](/en/docs/constants/objectconstants/enum_object) object.

The flags can be used as the combination of style flags with one of the flags specifying the font width. Flag names are shown below.

Flags for specifying font style

| Flag | Description |
| --- | --- |
| FONT_ITALIC | Italic |
| FONT_UNDERLINE | Underline |
| FONT_STRIKEOUT | Strikeout |

Flags for specifying font width

| Flag |
| --- |
| FW_DONTCARE |
| FW_THIN |
| FW_EXTRALIGHT |
| FW_ULTRALIGHT |
| FW_LIGHT |
| FW_NORMAL |
| FW_REGULAR |
| FW_MEDIUM |
| FW_SEMIBOLD |
| FW_DEMIBOLD |
| FW_BOLD |
| FW_EXTRABOLD |
| FW_ULTRABOLD |
| FW_HEAVY |
| FW_BLACK |

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   COORD_X    200
#define   COORD_Y    100
#define   OBJ_NAME   "TestTextGetSizeBitmapLabel"
#define   RES_NAME   "TestTextGetSizeResource"
#define   COLOR_NULL 0x00FFFFFF
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- current chart ID
   long   chart_id= ChartID();
   
   string font_names[] ={"Arial", "Tahoma", "Calibri"};
   uint   flags_array[]={0, FONT_ITALIC, FONT_UNDERLINE, FONT_STRIKEOUT};
   uint   fw_array[]={FW_DONTCARE, FW_THIN, FW_EXTRALIGHT, FW_ULTRALIGHT, FW_LIGHT,
                      FW_NORMAL, FW_REGULAR, FW_MEDIUM, FW_SEMIBOLD, FW_DEMIBOLD,
                      FW_BOLD, FW_EXTRABOLD, FW_ULTRABOLD, FW_HEAVY, FW_BLACK};
   
//--- disable drawing any attributes of the price chart
   ChartSetInteger(chart_id, CHART_SHOW, false);
   
//--- declare the parameters of the graphical resource
   uint rc_width =(int)ChartGetInteger(chart_id, CHART_WIDTH_IN_PIXELS); 
   uint rc_height=(int)ChartGetInteger(chart_id, CHART_HEIGHT_IN_PIXELS); 
   uint rc_data[]; 
   uint rc_size=rc_width*rc_height;
  
//--- create a graphical resource for text output
   if(!CreateResource(chart_id, rc_data, rc_width, rc_height))
      return;
   
//--- loop through font names
   for(int i=0; i<(int)font_names.Size(); i++)
     {
      //--- loop through font flags
      for(int j=0; j<(int)flags_array.Size(); j++)
        {
         //--- draw text with the font and style flag obtained from the array
         DrawText(font_names[i], flags_array[j], rc_data, rc_width, rc_height);
         Sleep(800);
         ArrayInitialize(rc_data, COLOR_NULL);
        }
      Sleep(800);
      ArrayInitialize(rc_data, COLOR_NULL);
     }
   
//--- after outputting all texts with different font sizes and styles,
//--- show text with different font width flags
   for(int i=0; i<(int)fw_array.Size(); i++)
     {
      //--- set the font size and name for displaying text with width flags
      string font_name="Tahoma";
      int    size=-140;
      TextSetFont(font_name, size, fw_array[i]);
      
      //--- create a drawn text string, output it to the resource pixel array, and update the resource
      string text=StringFormat("Text%d: Font name: \"%s%s\", size: %d (%d)", i+1, font_name, FlagWidthDescription(fw_array[i]), size, size/-10);
      TextOut(text, COORD_X, COORD_Y, ANCHOR_LEFT_UPPER, rc_data, rc_width, rc_height, ColorToARGB(clrDodgerBlue), COLOR_FORMAT_ARGB_NORMALIZE);
      Update(RES_NAME, rc_data, rc_width, rc_height, true);
      //--- wait a second
      Sleep(1000);
      ArrayInitialize(rc_data, COLOR_NULL);
     }
   
//--- wait five seconds, then free the resource and delete the graphical object
   Sleep(5000);
   ResourceFree(RES_NAME);
   ObjectDelete(chart_id, OBJ_NAME);
   
//--- allow drawing any attributes of the price chart
   ChartSetInteger(chart_id, CHART_SHOW, true);
   ChartRedraw(chart_id);
   /*
   Text messages are displayed on the chart as a result of the script execution.
   The texts have different fonts, as well as style and width flags
   */ 
  }
//+------------------------------------------------------------------+
//| Display five text strings of different                           |
//| sizes with the specified font and flags                          |
//+------------------------------------------------------------------+
void DrawText(const string font_name, uint flags, uint &pixels_array[], uint res_width, uint res_height)
  {
//--- output five strings of text with different font sizes
   for(int i=0; i<5; i++)
     {
      //--- calculate the font size and set the font for text output using drawing methods
      int size=-140+10*i;
      TextSetFont(font_name, size, flags);
      
      //--- create a drawn text string, output it to the resource pixel array, and update the resource
      string text=StringFormat("Text%d: Font name: \"%s%s\", size: %d (%d)", i+1, font_name, FlagDescription(flags), size, size/-10);
      TextOut(text, COORD_X, COORD_Y+22*i, ANCHOR_LEFT_UPPER, pixels_array, res_width, res_height, ColorToARGB(clrDodgerBlue), COLOR_FORMAT_ARGB_NORMALIZE);
      Update(RES_NAME, pixels_array, res_width, res_height, true);
      //--- wait a bit
      Sleep(800);
     }
  }
//+------------------------------------------------------------------+
//| Return a description of the font style flags                     |
//+------------------------------------------------------------------+
string FlagDescription(const uint flag)
  {
   switch(flag)
     {
      case FONT_ITALIC     :  return(" Italic");
      case FONT_UNDERLINE  :  return(" Underline");
      case FONT_STRIKEOUT  :  return(" Strikeout");
     }
   return("");
  }
//+------------------------------------------------------------------+
//| Return the description of the font width flags                   |
//+------------------------------------------------------------------+
string FlagWidthDescription(const uint flag)
  {
   switch(flag)
     {
      case FW_DONTCARE  :  return(" Dontcare");
      case FW_THIN      :  return(" Thin");
      case FW_EXTRALIGHT:  return(" Extralight");
      case FW_ULTRALIGHT:  return(" Ultralight");
      case FW_LIGHT     :  return(" Light");
      case FW_NORMAL    :  return(" Normal");
      case FW_REGULAR   :  return(" Regular");
      case FW_MEDIUM    :  return(" Medium");
      case FW_SEMIBOLD  :  return(" Semibold");
      case FW_DEMIBOLD  :  return(" Demibold");
      case FW_BOLD      :  return(" Bold");
      case FW_EXTRABOLD :  return(" Extrabold");
      case FW_ULTRABOLD :  return(" Ultrabold");
      case FW_HEAVY     :  return(" Heavy");
      case FW_BLACK     :  return(" Black");
     }
   return("");
  }
//+------------------------------------------------------------------+
//| Create a graphical resource for the entire chart                 |
//+------------------------------------------------------------------+
bool CreateResource(const long chart_id, uint &pixel_data[], const uint width, const uint height)
  {
//--- set the size of the pixel array
   ResetLastError(); 
   uint size=width*height;
   if(ArrayResize(pixel_data, size)!=size) 
     { 
      PrintFormat("%s: ArrayResize() failed. Error code %d",__FUNCTION__, GetLastError()); 
      return(false); 
     } 
//--- fill the pixel array with a transparent color and create a graphical resource based on it
   ArrayInitialize(pixel_data, COLOR_NULL); 
   if(!ResourceCreate(RES_NAME, pixel_data, width, height, 0, 0, 0, COLOR_FORMAT_ARGB_NORMALIZE)) 
     { 
      PrintFormat("%s: ResourceCreate() failed. Error code ",__FUNCTION__, GetLastError()); 
      return(false); 
     } 
  
//--- create the Graphic Label object at the coordinates of the upper left corner of the chart
   if(!ObjectCreate(0, OBJ_NAME, OBJ_BITMAP_LABEL, 0, 0, 0)) 
     { 
      PrintFormat("%s: ObjectCreate() failed. Error code %d",__FUNCTION__, GetLastError()); 
      return(false); 
     } 
//--- set the width and height of the created bitmap object equal to the width and height of the graphical resource.
//--- set the object anchor point to its center.
   if(!ObjectSetInteger(chart_id, OBJ_NAME, OBJPROP_XSIZE, width))
     {
      PrintFormat("%s: ObjectSetInteger() failed. Error code %d",__FUNCTION__, GetLastError()); 
      return(false); 
     }
   if(!ObjectSetInteger(chart_id, OBJ_NAME, OBJPROP_YSIZE, height))
     {
      PrintFormat("%s: ObjectSetInteger() failed. Error code %d",__FUNCTION__, GetLastError()); 
      return(false); 
     }
//--- specify the previously created graphical resource for the bitmap object as an image file
//--- in this case, in order to indicate the name of the graphical resource used, we need to add "::" before its name
   if(!ObjectSetString(chart_id, OBJ_NAME, OBJPROP_BMPFILE, "::"+RES_NAME))
     {
      PrintFormat("%s: ObjectSetString() failed. Error code %d",__FUNCTION__, GetLastError()); 
      return(false); 
     }
    
//--- all is fine
   return(true);
  }
//+------------------------------------------------------------------+ 
//| Update graphical resource data                                   |
//+------------------------------------------------------------------+ 
void Update(const string res_name, const uint &pixel_data[], const uint width, const uint height, const bool redraw) 
  { 
//--- leave if zero dimensions are passed
   if(width==0 || height==0) 
      return; 
//--- update resource data and redraw the chart
   if(ResourceCreate(res_name, pixel_data, width, height, 0, 0, 0, COLOR_FORMAT_ARGB_NORMALIZE) && redraw) 
      ChartRedraw(); 
  } 

```

See also

[Resources](/en/docs/runtime/resources), [ResourceCreate()](/en/docs/common/resourcecreate), [ResourceSave()](/en/docs/common/resourcesave), [TextOut()](/en/docs/objects/textout)
