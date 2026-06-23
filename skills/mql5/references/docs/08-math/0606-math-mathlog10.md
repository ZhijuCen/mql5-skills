# MathLog

Returns the logarithm of a number by base 10.

```
double  MathLog10(
   double  val      // number to take logarithm
   );

```

Parameters

val

[in]  Numeric value the common logarithm of which is to be calculated.

Return Value

The common logarithm in case of success. If val is negative, the function returns NaN (undetermined value). If val is equal to 0, the function returns INF (infinity).

Note

Instead of MathLog10() you can use log10().

Example:

```
#define GRAPH_WIDTH  750
#define GRAPH_HEIGHT 350
 
#include <Graphics\Graphic.mqh>
 
CGraphic ExtGraph;
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get 9 values from 0 to 8 with step 1
   vector X(9,VectorArange);
   Print("vector X = \n",X);
//--- calculate the decimal logarithm for each value of the X vector
   X=MathLog10(X);
   Print("MathLog10(X) = \n",X);
   
//--- transfer the calculated values from the vector to the array
   double y_array[];
   X.Swap(y_array);
 
//--- draw a graph of the calculated vector values
   CurvePlot(y_array,clrDodgerBlue);
 
//--- wait for pressing the Escape or PgDn keys to delete the graph (take a screenshot) and exit
   while(!IsStopped())
     {
      if(StopKeyPressed())
         break;
      Sleep(16);
     }
 
//--- clean up
   ExtGraph.Destroy();
   /*
   result:
   vector X = 
   [0,1,2,3,4,5,6,7,8]
   MathLog10(X) = 
   [-inf,0,0.3010299956639812,0.4771212547196624,0.6020599913279624,0.6989700043360189,0.7781512503836436,0.8450980400142568,0.9030899869919435]
   */
  }
//+------------------------------------------------------------------+
//| Fill a vector with 'value' in 'step' increments                  |
//+------------------------------------------------------------------+
template<typename T> 
void VectorArange(vector<T> &vec,T value=0.0,T step=1.0) 
  { 
   for(ulong i=0; i<vec.Size(); i++,value+=step) 
      vec[i]=value; 
  }
//+------------------------------------------------------------------+
//| When pressing ESC, return 'true'                                 |
//| When pressing PgDn, take a graph screenshot and return 'true'    |
//| Otherwise, return 'false'                                        |
//+------------------------------------------------------------------+
bool StopKeyPressed()
  {
//--- if ESC is pressed, return 'true'
   if(TerminalInfoInteger(TERMINAL_KEYSTATE_ESCAPE)!=0)
      return(true);
//--- if PgDn is pressed and a graph screenshot is successfully taken, return 'true'
   if(TerminalInfoInteger(TERMINAL_KEYSTATE_PAGEDOWN)!=0 && MakeAndSaveScreenshot(MQLInfoString(MQL_PROGRAM_NAME)+"_Screenshot"))
      return(true);
//--- return 'false' 
   return(false);
  }
//+------------------------------------------------------------------+
//| Create a graph object and draw a curve                           |
//+------------------------------------------------------------------+
void CurvePlot(double &x_array[], double &y_array[], const color colour)
  {
   ExtGraph.Create(ChartID(), "Graphic", 0, 0, 0, GRAPH_WIDTH, GRAPH_HEIGHT);
   ExtGraph.CurveAdd(x_array, y_array, ColorToARGB(colour), CURVE_LINES);
   ExtGraph.IndentUp(30);
   ExtGraph.CurvePlotAll();
   string text1="Press ESC to delete the graph and stop the script, or";
   string text2="Press PgDn to create a screen, delete the graph and stop the script";
   ExtGraph.TextAdd(54, 9, text1, ColorToARGB(clrBlack));
   ExtGraph.TextAdd(54,21, text2, ColorToARGB(clrBlack));
   ExtGraph.Update();
  }
//+------------------------------------------------------------------+
//| Take a screenshot and save the image to a file                   |
//+------------------------------------------------------------------+
bool MakeAndSaveScreenshot(const string file_name)
  {
   string file_names[];
   ResetLastError();
   int selected=FileSelectDialog("Save Picture", NULL, "All files (*.*)|*.*", FSD_WRITE_FILE, file_names, file_name+".png");
   if(selected<1)
     {
      if(selected<0)
         PrintFormat("%s: FileSelectDialog() function returned error %d", __FUNCTION__, GetLastError());
      return false;
     }
   
   bool res=false;
   if(ChartSetInteger(0,CHART_SHOW,false))
      res=ChartScreenShot(0, file_names[0], GRAPH_WIDTH, GRAPH_HEIGHT);
   ChartSetInteger(0,CHART_SHOW,true);
   return(res);
  }

```

Result:

![See also](pics/mathlog10_screenshot.png)

See also

[Real types (double, float)](/en/docs/basis/types/double), [Statistics](/en/docs/standardlibrary/mathematics/stat), [Scientific Charts](/en/docs/standardlibrary/graphics), [Client Terminal Properties](/en/docs/constants/environment_state/terminalstatus)
