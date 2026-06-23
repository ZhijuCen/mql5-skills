# BarsCalculated

Returns the number of calculated data for the specified indicator.

```
int  BarsCalculated(
   int       indicator_handle,     // indicator handle
   );

```

Parameters

indicator_handle

[in]  The indicator handle, returned by the corresponding indicator function.

Return Value

Returns the amount of calculated data in the indicator buffer or -1 in the case of error (data not calculated yet)

Note

The function is useful when it's necessary to get the indicator data immediately after its creation (indicator handle is available).

Example:

```
void OnStart()
  {
   double Ups[];
//--- set timeseries ordering for the arrays
   ArraySetAsSeries(Ups,true);
//--- create handle for the Fractal Indicator
   int FractalsHandle=iFractals(NULL,0);
//--- reset the error code
   ResetLastError();
//--- try to copy the indicator values
   int i,copied=CopyBuffer(FractalsHandle,0,0,1000,Ups);
   if(copied<=0)
     {
      Sleep(50);
      for(i=0;i<100;i++)
        {
         if(BarsCalculated(FractalsHandle)>0)
            break;
         Sleep(50);
        }
      copied=CopyBuffer(FractalsHandle,0,0,1000,Ups);
      if(copied<=0)
        {
         Print("Failed to copy upper fractals. Error = ",GetLastError(),
         "i = ",i,"    copied = ",copied);
         return;
        }
       else
         Print("Upper fractals copied",
         "i = ",i,"    copied = ",copied);
     }
   else Print("Upper fractals copied. ArraySize = ",ArraySize(Ups));
  }

```
