# Levels of Elliott Wave

Elliott Waves are represented by two graphical objects of types OBJ_ELLIOTWAVE5 and OBJ_ELLIOTWAVE3. To set the wave size (method of wave labeling), the OBJPROP_DEGREE property is used, to which one of values of the ENUM_ELLIOT_WAVE_DEGREE enumeration can be assigned.

ENUM_ELLIOT_WAVE_DEGREE

| ID | Description |
| --- | --- |
| ELLIOTT_GRAND_SUPERCYCLE | Grand Supercycle |
| ELLIOTT_SUPERCYCLE | Supercycle |
| ELLIOTT_CYCLE | Cycle |
| ELLIOTT_PRIMARY | Primary |
| ELLIOTT_INTERMEDIATE | Intermediate |
| ELLIOTT_MINOR | Minor |
| ELLIOTT_MINUTE | Minute |
| ELLIOTT_MINUETTE | Minuette |
| ELLIOTT_SUBMINUETTE | Subminuette |

Example:

```
   for(int i=0;i<ObjectsTotal(0);i++)
     {
      string currobj=ObjectName(0,i);
      if((ObjectGetInteger(0,currobj,OBJPROP_TYPE)==OBJ_ELLIOTWAVE3) || 
         ((ObjectGetInteger(0,currobj,OBJPROP_TYPE)==OBJ_ELLIOTWAVE5)))
        {
         //--- set the marking level in INTERMEDIATE
         ObjectSetInteger(0,currobj,OBJPROP_DEGREE,ELLIOTT_INTERMEDIATE);
         //--- show lines between tops of waves
         ObjectSetInteger(0,currobj,OBJPROP_DRAWLINES,true);
         //--- set line color
         ObjectSetInteger(0,currobj,OBJPROP_COLOR,clrBlue);
         //--- set line width
         ObjectSetInteger(0,currobj,OBJPROP_WIDTH,5);
         //--- set description
         ObjectSetString(0,currobj,OBJPROP_TEXT,"test script");
        }
     }

```
