# TextGetSize

The function returns the line width and height at the current [font settings](/en/docs/objects/textsetfont).

```
bool  TextGetSize(
   const string       text,          // text string
   uint&               width,        // buffer width in pixels
   uint&               height        // buffer height in pixels
   );

```

Parameters

text

[in]  String, for which length and width should be obtained.

width

[out]  Input parameter for receiving width.

height

[out]  Input parameter for receiving height.

Return Value

Returns true if successful, otherwise false. Possible code errors:

- ERR_INTERNAL_ERROR(4001) - operating system error.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   COORD_X    200
#define   COORD_Y    100
#define   OBJ_NAME   "TestTextGetSizeBitmapLabel"
#define   RES_NAME   "TestTextGetSizeResource"
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- prepare three lines of text for output to the chart
   string text1="This is the first line of text";
   string text2="The second line also contains text";
   string text3="Each word in each line has its own size";
   
   string text_array1[];   // array to get the set of words from string 1
   string text_array2[];   // array to get the set of words from string 2
   string text_array3[];   // array to get the set of words from string 3
   
//--- fill three arrays of words
   if(!SplitTextIntoWords(text1, text_array1) || !SplitTextIntoWords(text2, text_array2) || !SplitTextIntoWords(text3, text_array3))
      return;
      
//--- current chart ID
   long   chart_id= ChartID();
   
//--- declare the parameters of the graphical resource
   uint   rc_width =(int)ChartGetInteger(chart_id, CHART_WIDTH_IN_PIXELS); 
   uint   rc_height=(int)ChartGetInteger(chart_id, CHART_HEIGHT_IN_PIXELS); 
   uint   rc_data[]; 
   uint   rc_size=rc_width*rc_height;
  
//--- create a graphical resource for text output
   if(!CreateResource(chart_id, rc_data, rc_width, rc_height))
      return;
   
//--- get the size of the space character by width and height
   int space_w=0, space_h=0;
   if(!TextGetSize(" ", space_w, space_h))
     {
      PrintFormat("%s: TextGetSize() failed. Error code %d",__FUNCTION__, GetLastError()); 
      return; 
     }
   
//--- increase the vertical indentation between strings by 2 and plot the texts from three arrays on the chart
   space_h+=2;
   TextArrayToChart(1, text_array1, COORD_X, COORD_Y+space_h*0, space_w, rc_data, rc_width, rc_height);
   TextArrayToChart(2, text_array2, COORD_X, COORD_Y+space_h*1, space_w, rc_data, rc_width, rc_height);
   TextArrayToChart(3, text_array3, COORD_X, COORD_Y+space_h*2, space_w, rc_data, rc_width, rc_height);
   
//--- after all the texts have been displayed, update the resource data
   Update(RES_NAME, rc_data, rc_width, rc_height, true);
   
//--- wait five seconds, then free the resource and delete the graphical object
   Sleep(5000);
   ResourceFree(RES_NAME);
   ObjectDelete(chart_id, OBJ_NAME);
   /*
   three strings of text are displayed on the chart as a result of the script execution
   each individual word in each string is displayed at a distance from the previous word,
   equal to the width of the text of the previous word obtained using the TextGetSize(); function
   the journal will contain all the words of each string with their sizes:
   Text array 1:
   [0] word: "This", width=29, height=18
   [1] word: "is", width=12, height=18
   [2] word: "the", width=21, height=18
   [3] word: "first", width=25, height=18
   [4] word: "line", width=24, height=18
   [5] word: "of", width=13, height=18
   [6] word: "text", width=24, height=18
   Text array 2:
   [0] word: "The", width=26, height=18
   [1] word: "second", width=51, height=18
   [2] word: "line", width=24, height=18
   [3] word: "also", width=29, height=18
   [4] word: "contains", width=58, height=18
   [5] word: "text", width=24, height=18
   Text array 3:
   [0] word: "Each", width=36, height=18
   [1] word: "word", width=34, height=18
   [2] word: "in", width=12, height=18
   [3] word: "each", width=34, height=18
   [4] word: "line", width=24, height=18
   [5] word: "has", width=25, height=18
   [6] word: "its", width=16, height=18
   [7] word: "own", width=28, height=18
   [8] word: "size", width=28, height=18
   */ 
  }
//+----------------------------------------------------------------------------+
//| Split a string into an array of words using the space separator (" ")      |
//+----------------------------------------------------------------------------+
bool SplitTextIntoWords(const string text, string &array[])
  {
   ResetLastError();
   if(StringSplit(text, StringGetCharacter(" ", 0), array)<0)
     {
      PrintFormat("%s: StringSplit() failed. Error code %d",__FUNCTION__, GetLastError()); 
      return(false); 
     }
   return(true);
  }
//+------------------------------------------------------------------+
//| Display text from an array on a chart                            |
//+------------------------------------------------------------------+
void TextArrayToChart(int array_num, string &array[], const int text_x, const int text_y, int space_w, uint &pixel_data[], const uint res_width, const uint res_height)
  {
   int width=0, height=0;  // text width and height
   int x=text_x;           // X coordinate of the output text
   
//--- print a header with the name of the processed array of words
   Print("Text array ", array_num,":");
   
//--- in a loop by the array of words
   int total=(int)array.Size();
   for(int i=0; i<total; i++)
     {
      //--- get the next word and send it to the chart (we draw it in the resource pixel array) 
      string word=array[i];
      TextOut(word, x, text_y, ANCHOR_LEFT_UPPER, pixel_data, res_width, res_height, ColorToARGB(clrDodgerBlue), COLOR_FORMAT_ARGB_NORMALIZE);
      
      //--- get the text size of the current word
      ResetLastError();
      if(!TextGetSize(word, width, height))
        {
         PrintFormat("%s: TextGetSize(\"%s\") failed. Error code %d",__FUNCTION__, word, GetLastError()); 
         continue; 
        }
      //--- print the text data in the journal - the word, its width and height,
      //--- then increase the X coordinate of the next word by (word width) + (space width)
      PrintFormat("[%d] word: \"%s\", width=%d, height=%d",i, word, width, height);
      x+=width+space_w;
     }
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
   ArrayInitialize(pixel_data, 0x00FFFFFF); 
   if(!ResourceCreate(RES_NAME, pixel_data, width, height, 0, 0, 0, COLOR_FORMAT_ARGB_NORMALIZE)) 
     { 
      PrintFormat("%s: ResourceCreate() failed. Error code %d",__FUNCTION__, GetLastError()); 
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

[Resources](/en/docs/runtime/resources), [ResourceCreate()](/en/docs/common/resourcecreate), [ResourceSave()](/en/docs/common/resourcesave), [TextSetFont()](/en/docs/objects/textsetfont), [TextOut()](/en/docs/objects/textout)
