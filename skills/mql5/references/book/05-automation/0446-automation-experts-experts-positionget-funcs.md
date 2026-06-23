# Functions for reading position properties

An MQL program can get position properties using several PositionGet functions depending on the type of properties. In all functions, the specific property being requested is defined in the first parameter, which takes the ID of one of the ENUM_POSITION_PROPERTY enumerations discussed in the previous section.

For each type of property, there is a short and long form of the function: the first returns the value of the property directly, and the second writes it into the second parameter, passed by reference.

Integer properties and properties of compatible types (datetime, enumerations) can be obtained by the PositionGetInteger function.

long PositionGetInteger(ENUM_POSITION_PROPERTY_INTEGER property)

bool PositionGetInteger(ENUM_POSITION_PROPERTY_INTEGER property, long &value)

If it fails, the function returns 0 or false.

The PositionGetDouble function is used to obtain real properties.

double PositionGetDouble(ENUM_POSITION_PROPERTY_DOUBLE property)

bool PositionGetDouble(ENUM_POSITION_PROPERTY_DOUBLE property, double &value)

Finally, the string properties are returned by the PositionGetString function.

string PositionGetString(ENUM_POSITION_PROPERTY_STRING property)

bool PositionGetString(ENUM_POSITION_PROPERTY_STRING property, string &value)

In case of failure, the first form of the function returns an empty string.

To read position properties, we already have a ready abstract interface MonitorInterface (TradeBaseMonitor.mqh) which we used to write an order monitor. Now it will be easy to implement a similar monitor for positions. The result is attached in the file PositionMonitor.mqh.

The PositionMonitorInterface class is inherited from MonitorInterface with assignment to the template types I, D, and S of the considered ENUM_POSITION_PROPERTY enumerations, and overrides a couple of stringify methods taking into account the specifics of position properties.

```
class PositionMonitorInterface:
   public MonitorInterface<ENUM_POSITION_PROPERTY_INTEGER,
   ENUM_POSITION_PROPERTY_DOUBLE,ENUM_POSITION_PROPERTY_STRING>
{
public:
   virtual string stringify(const long v,
      const ENUM_POSITION_PROPERTY_INTEGER property) const override
   {
      switch(property)
      {
         case POSITION_TYPE:
            return enumstr<ENUM_POSITION_TYPE>(v);
         case POSITION_REASON:
            return enumstr<ENUM_POSITION_REASON>(v);
         
         case POSITION_TIME:
         case POSITION_TIME_UPDATE:
            return TimeToString(v, TIME_DATE | TIME_SECONDS);
         
         case POSITION_TIME_MSC:
         case POSITION_TIME_UPDATE_MSC:
            return STR_TIME_MSC(v);
      }
      
      return (string)v;
   }
   
   virtual string stringify(const ENUM_POSITION_PROPERTY_DOUBLE property,
      const string format = NULL) const override
   {
      if(format == NULL &&
         (property == POSITION_PRICE_OPEN || property == POSITION_PRICE_CURRENT
         || property == POSITION_SL || property == POSITION_TP))
      {
         const int digits = (int)SymbolInfoInteger(PositionGetString(POSITION_SYMBOL),
            SYMBOL_DIGITS);
         return DoubleToString(PositionGetDouble(property), digits);
      }
      return MonitorInterface<ENUM_POSITION_PROPERTY_INTEGER,
         ENUM_POSITION_PROPERTY_DOUBLE,ENUM_POSITION_PROPERTY_STRING>
         ::stringify(property, format);
   }

```

The specific monitor class, ready to view positions, is next in the inheritance chain and is based on PositionGet functions. Selecting a position by ticket is done in the constructor.

```
class PositionMonitor: public PositionMonitorInterface
{
public:
   const ulong ticket;
   PositionMonitor(const ulong t): ticket(t)
   {
      if(!PositionSelectByTicket(ticket))
      {
         PrintFormat("Error: PositionSelectByTicket(%lld) failed: %s",
            ticket, E2S(_LastError));
      }
      else
      {
         ready = true;
      }
   }
   
   virtual long get(const ENUM_POSITION_PROPERTY_INTEGER property) const override
   {
      return PositionGetInteger(property);
   }
   
   virtual double get(const ENUM_POSITION_PROPERTY_DOUBLE property) const override
   {
      return PositionGetDouble(property);
   }
   
   virtual string get(const ENUM_POSITION_PROPERTY_STRING property) const override
   {
      return PositionGetString(property);
   }
   ...
};

```

A simple script will allow you to log all the characteristics of the first position (if at least one is available).

```
void OnStart()
{
   PositionMonitor pm(PositionGetTicket(0));
   pm.print();
}

```

In the log, we should get something like this.

```
MonitorInterface<ENUM_POSITION_PROPERTY_INTEGER, »
   » ENUM_POSITION_PROPERTY_DOUBLE,ENUM_POSITION_PROPERTY_STRING>
ENUM_POSITION_PROPERTY_INTEGER Count=9
  0 POSITION_TIME=2022.03.24 23:09:45
  1 POSITION_TYPE=POSITION_TYPE_BUY
  2 POSITION_MAGIC=0
  3 POSITION_IDENTIFIER=1291755067
  4 POSITION_TIME_MSC=2022.03.24 23:09:45'261
  5 POSITION_TIME_UPDATE=2022.03.24 23:09:45
  6 POSITION_TIME_UPDATE_MSC=2022.03.24 23:09:45'261
  7 POSITION_TICKET=1291755067
  8 POSITION_REASON=POSITION_REASON_EXPERT
ENUM_POSITION_PROPERTY_DOUBLE Count=8
  0 POSITION_VOLUME=0.01
  1 POSITION_PRICE_OPEN=1.09977
  2 POSITION_PRICE_CURRENT=1.09965
  3 POSITION_SL=0.00000
  4 POSITION_TP=1.10500
  5 POSITION_COMMISSION=0.0
  6 POSITION_SWAP=0.0
  7 POSITION_PROFIT=-0.12
ENUM_POSITION_PROPERTY_STRING Count=3
  0 POSITION_SYMBOL=EURUSD
  1 POSITION_COMMENT=
  2 POSITION_EXTERNAL_ID=

```

If there are no open positions at the moment, we will see an error message.

```
Error: PositionSelectByTicket(0) failed: TRADE_POSITION_NOT_FOUND

```

However, the monitor is useful not only and not so much by outputting properties to the log. Based on PositionMonitor, we create a class for selecting positions by conditions, similar to what we did for orders ([OrderFilter](/en/book/automation/experts/experts_order_filter)). The ultimate goal is to improve our grid Expert Advisor.

Thanks to OOP, creating a new filter class is almost effortless. Below is the complete source code (file PositionFilter.mqh).

```
class PositionFilter: public TradeFilter<PositionMonitor,
   ENUM_POSITION_PROPERTY_INTEGER,
   ENUM_POSITION_PROPERTY_DOUBLE,
   ENUM_POSITION_PROPERTY_STRING>
{
protected:
   virtual int total() const override
   {
      return PositionsTotal();
   }
   virtual ulong get(const int i) const override
   {
      return PositionGetTicket(i);
   }
};

```

Now we can write such a script for receiving specific profit on positions with the given magic number, for example.

```
input ulong Magic;
   
void OnStart()
{
   PositionFilter filter;
   
   ENUM_POSITION_PROPERTY_DOUBLE properties[] =
      {POSITION_PROFIT, POSITION_VOLUME};
   
   double profits[][2];
   ulong tickets[];
   string symbols[];
   
   filter.let(POSITION_MAGIC, Magic).select(properties, tickets, profits);
   filter.select(POSITION_SYMBOL, tickets, symbols);
   
   for(int i = 0; i < ArraySize(symbols); ++i)
   {
      PrintFormat("%s[%lld]=%f",
         symbols[i], tickets[i], profits[i][0] / profits[i][1]);
   }
}

```

In this case, we had to call the select method twice, because the types of properties we are interested in are different: real profit and lot, but the string name of the instrument. In one of the sections at the beginning of the chapter, when we were developing the filter class for symbols, we described the concept of [tuples](/en/book/automation/symbols/symbols_point_tick). In MQL5, we can implement it as structure templates with fields of arbitrary types. Such tuples would come in very handy for finalizing the hierarchy of filter classes since then it would be possible to describe the select method that fills an array of tuples with fields of any type.

The tuples are described in the file Tuples.mqh. All structures in it have a name TupleN<T1,...>, where N is a number from 2 to 8, and it corresponds to the number of template parameters (Ti types). For example, Tuple2:

```
template<typename T1,typename T2>
struct Tuple2
{
   T1 _1;
   T2 _2;
   
   static int size() { return 2; };
   
   // M — order, position, deal monitor class, any MonitorInterface<>
   template<typename M>
   void assign(const int &properties[], M &m)
   {
      if(ArraySize(properties) != size()) return;
      _1 = m.get(properties[0], _1);
      _2 = m.get(properties[1], _2);
   }
};

```

In the class TradeFilter (TradeFilter.mqh) let's add a version of the function select with tuples.

```
template<typename T,typename I,typename D,typename S>
class TradeFilter
{
   ...
 template<typename U> // type U must be Tuple<>, e.g. Tuple3<T1,T2,T3>
   bool select(const int &property[], U &data[], const bool sort = false) const
   {
      const int q = ArraySize(property);
      static const U u;                 // PRB: U::size() does not compile
      if(q != u.size()) return false;   // required condition
      
      const int n = total();
      // cycle through orders/positions/deals
      for(int i = 0; i < n; ++i)
      {
         const ulong t = get(i);
         // access to properties via monitor T
         T m(t);
         // check all filter conditions for different types of properties
         if(match(m, longs)
         && match(m, doubles)
         && match(m, strings))
         {
            // for a suitable object, store the properties in an array of tuples
            const int k = EXPAND(data);
            data[k].assign(property, m);
         }
      }
      
      if(sort)
      {
         sortTuple(data, u._1);
      }
      
      return true;
   }

```

An array of tuples can optionally be sorted by the first field _1, so you can additionally study the sortTuple helper method.

With tuples, you can query a filter object for properties of three different types in one select call.

Below there are positions with some Magic number displayed, sorted by profit; for each a symbol and a ticket are additionally obtained.

```
 input ulong Magic;
   
   void OnStart()
   {
      int props[] = {POSITION_PROFIT, POSITION_SYMBOL, POSITION_TICKET};
      Tuple3<double,string,ulong> tuples[];
      PositionFilter filter;
      filter.let(POSITION_MAGIC, Magic).select(props, tuples, true);
      ArrayPrint(tuples);
   }

```

Of course, the parameter types in the description of the array of tuples (in this case, Tuple3<double,string,ulong>) must match the requested property enumeration types (POSITION_PROFIT, POSITION_SYMBOL, POSITION_TICKET).

Now we can slightly simplify the grid Expert Advisor (meaning not just a shorter, but also a more understandable code). The new version is called PendingOrderGrid2.mq5. The changes will affect all functions related to position management.

The GetMyPositions function populates the types4tickets array of tuples passed by reference. In each Tuple2 tuple, it is supposed to store the type and ticket of the position. In this particular case, we could manage just with a two-dimensional array ulong instead of tuples because both properties are of the same base type. However, we use tuples to demonstrate how to work with them in the calling code.

```
#include <MQL5Book/Tuples.mqh>
#include <MQL5Book/PositionFilter.mqh>
   
int GetMyPositions(const string s, const ulong m,
   Tuple2<ulong,ulong> &types4tickets[])
{
   int props[] = {POSITION_TYPE, POSITION_TICKET};
   PositionFilter filter;
   filter.let(POSITION_SYMBOL, s).let(POSITION_MAGIC, m)
      .select(props, types4tickets, true);
   return ArraySize(types4tickets);
}

```

Note that the last, third parameter of the select method equals true, which instructs to sort the array by the first field, i.e., the type of positions. Thus, we will have purchases at the beginning, and sales at the end. This will be required for the counter closure.

The reincarnation of the CompactPositions method is as follows.

```
uint CompactPositions(const bool cleanup = false)
{
   uint retcode = 0;
   Tuple2<ulong,ulong> types4tickets[];
   int i = 0, j = 0;
   int n = GetMyPositions(_Symbol, Magic, types4tickets);
   if(n > 0)
   {
      Print("CompactPositions: ", n);
      for(i = 0, j = n - 1; i < j; ++i, --j)
      {
         if(types4tickets[i]._1 != types4tickets[j]._1) // as long as the types are different
         {
            retcode = CloseByPosition(types4tickets[i]._2, types4tickets[j]._2);
            if(retcode) return retcode; // error
         }
         else
         {
            break;
         }
      }
   }
   
   if(cleanup && j < n)
   {
      retcode = CloseAllPositions(types4tickets, i, j + 1);
   }
   
   return retcode;
}

```

The CloseAllPositions function is almost the same:

```
uint CloseAllPositions(const Tuple2<ulong,ulong> &types4tickets[],
   const int start = 0, const int end = 0)
{
   const int n = end == 0 ? ArraySize(types4tickets) : end;
   Print("CloseAllPositions ", n - start);
   for(int i = start; i < n; ++i)
   {
      MqlTradeRequestSyncLog request;
      request.comment = "close down " + (string)(i + 1 - start)
         + " of " + (string)(n - start);
      const ulong ticket = types4tickets[i]._2;
      if(!(request.close(ticket) && request.completed()))
      {
         Print("Error: position is not closed ", ticket);
         return request.result.retcode; // error
      }
   }
   return 0; // success 
}

```

You can compare the work of Expert Advisors PendingOrderGrid1.mq5 and PendingOrderGrid2.mq5 in the tester.

The reports will be slightly different, because if there are several positions, they are closed in opposite combinations, due to which the closing of other, unpaired positions takes place with respect to their individual spreads.
