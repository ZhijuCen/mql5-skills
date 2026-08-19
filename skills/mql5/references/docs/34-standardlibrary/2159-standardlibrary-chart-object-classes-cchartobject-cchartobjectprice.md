# Price (Get Method)

Gets the price coordinate of the specified anchor point of a graphical object.

```
double  Price(
   int  point      // point number
   ) const

```

Parameters

point

[in]  Number of a graphical object anchor point.

Return Value

Price coordinate of the specified anchor point of the graphical object attached to an instance of the class. If there is no attached object or the object does not have this point, it returns [EMPTY_VALUE](/en/docs/constants/namedconstants/otherconstants).

# Price (Set Method)

Sets the price coordinate of the specified anchor point of a graphical object.

```
bool  Price(
   int     point,         // point number
   double  new_price      // price
   )

```

Parameters

point

[in]  Number of a graphical object anchor point.

new_price

[in]  New value for the price coordinate of the specified graphical object anchor point.

Return Value

true - success, false - cannot change the price coordinate.

Example:

```
//--- example for CChartObject::Price  
#include <ChartObjects\ChartObject.mqh>  
//---  
void OnStart()  
  {  
   CChartObject object;  
   double       price;  
   //---  
   for(int i=0;i<object.NumPoints();i++)  
     {  
      //--- get price of the chart object point
      double point_price=object.Price(i);  
      if(point_price!=price)  
        {  
         //--- set price for the chart object point
         object.Price(i,price);  
        }  
     }  
  }  

```
