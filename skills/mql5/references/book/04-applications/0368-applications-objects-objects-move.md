# Moving objects

To move objects in time/price coordinates, you can use not only the ObjectSet functions of property change but also the special function ObjectMove, which changes the coordinates of the specified anchor point of the object.

bool ObjectMove(long chartId, const string name, int index, datetime time, double price)

The chartId parameter sets the chart ID (0 is for the current chart). The name of the object is passed in the name parameter. The anchor point index and coordinates are specified in the index, time, and price parameters, respectively.

The function uses an asynchronous call, that is, it sends a command to the chart's event queue and does not wait for the movement itself.

The function returns an indication of whether the command was successfully queued (in this case, the result is true). The actual position of the object should be learned using calls to the ObjectGet functions.

In the indicator [ObjectHighLowFibo.mq5](/en/book/applications/objects/objects_levels), we modify the DrawFibo function in such a way as to enable ObjectMove. Instead of two calls to ObjectSet functions in the loop through the anchor points, we now have one ObjectMove call:

```
bool DrawFibo(const string name, const datetime &t[], const double &p[],
   const color clr)
{
   ...
   for(int i = 0; i < ArraySize(t); ++i)
   {
      // was:
      // ObjectSetInteger(0, name, OBJPROP_TIME, i, t[i]);
      // ObjectSetDouble(0, name, OBJPROP_PRICE, i, p[i]);
      // became:
      ObjectMove(0, name, i, t[i], p[i]);
   }
   ...
}

```

It makes sense to apply the ObjectMove function where both coordinates of the anchor point change. In some cases, only one coordinate has an effect (for example, in the channels of standard deviation and linear regression at the anchor points, only the start and end dates/times are important, and the channels calculate the price value at these points automatically). In such cases, a single call of the ObjectSet function is more appropriate than ObjectMove.
