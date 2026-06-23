# ObjectSetDouble

The function sets the value of the corresponding object property. The object property must be of the [double](/en/docs/basis/types/double) type. There are 2 variants of the function.

Setting property value, without modifier

```
bool  ObjectSetDouble(
   long                            chart_id,          // chart identifier
   string                          name,              // object name
   ENUM_OBJECT_PROPERTY_DOUBLE     prop_id,           // property
   double                          prop_value         // value
   );

```

Setting a property value indicating the modifier

```
bool  ObjectSetDouble(
   long                            chart_id,          // chart identifier
   string                          name,              // object name
   ENUM_OBJECT_PROPERTY_DOUBLE     prop_id,           // property
   int                             prop_modifier,     // modifier
   double                          prop_value         // value
   );

```

Parameters

chart_id

[in]  Chart identifier. 0 means the current chart.

name

[in]  Name of the object.

prop_id

[in]  ID of the object property. The value can be one of the values of the [ENUM_OBJECT_PROPERTY_DOUBLE](/en/docs/constants/objectconstants/enum_object_property#enum_object_property_double) enumeration.

prop_modifier

[in]  Modifier of the specified property. It denotes the number of the level in [Fibonacci tools](/en/docs/constants/objectconstants/enum_object) and in the graphical object Andrew's pitchfork. The numeration of levels starts from zero.

prop_value

[in]  The value of the property.

Return Value

The function returns true only if the command to change properties of a graphical object has been sent to a chart successfully. Otherwise it returns false. To read more about the [error](/en/docs/constants/errorswarnings/errorcodes) call [GetLastError()](/en/docs/check/getlasterror).

Note

The function uses an asynchronous call, which means that the function does not wait for the execution of the command that has been added to the queue of the specified chart. Instead, it immediately returns control.

To check the command execution result, you can use a function that requests the specified object property. However, you should keep in mind that such functions are added to the end of the queue of that chart, and they wait for the execution result, and can therefore be time consuming. This feature should be taken into account when working with a large number of objects on a chart.

Example of creating a Fibonacci object and adding a new level in it

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- auxiliary arrays
   double high[],low[],price1,price2;
   datetime time[],time1,time2;
//--- Copy the open prices - 100 latest bars are enough
   int copied=CopyHigh(Symbol(),0,0,100,high);
   if(copied<=0)
     {
      Print("Failed to copy the values of the High price series");
      return;
     }
//--- Copy the close price - 100 latest bars are enough
   copied=CopyLow(Symbol(),0,0,100,low);
   if(copied<=0)
     {
      Print("Failed to copy the values of the Low price series");
      return;
     }
//--- Copy the open time for the last 100 bars
   copied=CopyTime(Symbol(),0,0,100,time);
   if(copied<=0)
     {
      Print("Failed to copy the values of the price series of Time");
      return;
     }
//--- Organize access to the copied data as to timeseries - backwards
   ArraySetAsSeries(high,true);
   ArraySetAsSeries(low,true);
   ArraySetAsSeries(time,true);
 
//--- Coordinates of the first anchor point of the Fibo object
   price1=high[70];
   time1=time[70];
//--- Coordinates of the second anchor point of the Fibo object
   price2=low[50];
   time2=time[50];
 
//--- Time to create the Fibo object
   bool created=ObjectCreate(0,"Fibo",OBJ_FIBO,0,time1,price1,time2,price2);
   if(created) // If the object is created successfully
     {
      //--- set the color of Fibo levels
      ObjectSetInteger(0,"Fibo",OBJPROP_LEVELCOLOR,Blue);
      //--- by the way, how much Fibo levels do we have?
      int levels=ObjectGetInteger(0,"Fibo",OBJPROP_LEVELS);
      Print("Fibo levels before = ",levels);
      //---output to the Journal => number of level:value level_desription
      for(int i=0;i<levels;i++)
        {
         Print(i,": ",ObjectGetDouble(0,"Fibo",OBJPROP_LEVELVALUE,i),
               "  ",ObjectGetString(0,"Fibo",OBJPROP_LEVELTEXT,i));
        }
      //--- Try to increase the number of levels per unit
      bool modified=ObjectSetInteger(0,"Fibo",OBJPROP_LEVELS,levels+1);
      if(!modified) // failed to change the number of levels
        {
         Print("Failed to change the number of levels of Fibo, error ",GetLastError());
        }
      //--- just inform
      Print("Fibo levels after = ",ObjectGetInteger(0,"Fibo",OBJPROP_LEVELS));
      //--- set a value for a newly created level
      bool added=ObjectSetDouble(0,"Fibo",OBJPROP_LEVELVALUE,levels,133);
      if(added) // managed to set a value for the level
        {
         Print("Successfully set one more Fibo level");
         //--- Also do not forget to set the level description
         ObjectSetString(0,"Fibo",OBJPROP_LEVELTEXT,levels,"my level");
         ChartRedraw(0);
         //--- Get the actual value of the number of levels in the Fibo object
         levels=ObjectGetInteger(0,"Fibo",OBJPROP_LEVELS);
         Print("Fibo levels after adding = ",levels);
         //--- once again output all levels - just to make sure
         for(int i=0;i<levels;i++)
           {
            Print(i,":",ObjectGetDouble(0,"Fibo",OBJPROP_LEVELVALUE,i),
                  "  ",ObjectGetString(0,"Fibo",OBJPROP_LEVELTEXT,i));
           }
        }
      else // Fails if you try to increase the number of levels in the Fibo object
        {
         Print("Failed to set one more Fibo level. Error ",GetLastError());
        }
     }
  }

```

See also

[Object Types](/en/docs/constants/objectconstants/enum_object), [Object Properties](/en/docs/constants/objectconstants/enum_object_property)
