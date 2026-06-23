# Functions for reading properties of active orders

The sets of functions that can be used to get the values of all order properties differ for active and historical orders. This section describes the functions for reading the properties of active orders. For the functions for accessing the properties of orders in the history, see the [relevant section](/en/book/automation/experts/experts_historyorderget_funcs).

Integer properties can be read using the OrderGetInteger function, which has two forms: the first one returns directly the value of the property, the second one returns a logical sign of success (true) or error (false), and the second parameter passed by reference is filled with the value of the property.

long OrderGetInteger(ENUM_ORDER_PROPERTY_INTEGER property)

bool OrderGetInteger(ENUM_ORDER_PROPERTY_INTEGER property, long &value)

Both functions allow you to get the requested order property of an integer-compatible type (datetime, long/ulong or listing). Although the prototype mentions long, from a technical point of view, the value is stored as an 8-byte cell, which can be cast to compatible types without any conversion of the internal representation, in particular, to ulong, which is used for all tickets.

A similar pair of functions is intended for properties of real type double.

double OrderGetDouble(ENUM_ORDER_PROPERTY_DOUBLE property)

bool OrderGetDouble(ENUM_ORDER_PROPERTY_DOUBLE property, double &value)

Finally, string properties are available through a pair of OrderGetString functions.

string OrderGetString(ENUM_ORDER_PROPERTY_STRING property)

bool OrderGetString(ENUM_ORDER_PROPERTY_STRING property, string &value)

As their first parameter, all functions take the identifier of the property we are interested in. This must be an element of one of the enumerations — ENUM_ORDER_PROPERTY_INTEGER, ENUM_ORDER_PROPERTY_DOUBLE, or ENUM_ORDER_PROPERTY_STRING — discussed in the [previous section](/en/book/automation/experts/experts_order_properties).

Please note before calling any of the previous functions, you should first select an order using OrderSelect or OrderGetTicket.

To read all the properties of a specific order, we will develop the OrderMonitor class (OrderMonitor.mqh) which operates on the same principle as the previously considered symbol (SymbolMonitor.mqh) and trading account (AccountMonitor.mqh) monitors.

These and other monitor classes discussed in the book offer a unified way to analyze properties through overloaded versions of virtual get methods.

Looking a little ahead, let's say that deals and positions have the same grouping of properties according to the three main types of values, and we also need to implement monitors for them. In this regard, it makes sense to separate the general algorithm into a base abstract class MonitorInterface (TradeBaseMonitor.mqh). This is a template class with three parameters intended to specify the types of specific enumerations, for integer (I), real (D), and string (S) property groups.

```
#include <MQL5Book/EnumToArray.mqh>
   
template<typename I,typename D,typename S>
class MonitorInterface
{
protected:
   bool ready;
public:
   MonitorInterface(): ready(false) { }
   
   bool isReady() const
   {
      return ready;
   }
   ...

```

Due to the fact that finding an order (deal or position) in the trading environment may fail for various reasons, the class has a reserved variable ready in which derived classes will have to write a sign of successful initialization, that is, the choice of an object to read its properties.

Several purely virtual methods declare access to properties of the corresponding types.

```
   virtual long get(const I property) const = 0;
   virtual double get(const D property) const = 0;
   virtual string get(const S property) const = 0;
   virtual long get(const int property, const long) const = 0;
   virtual double get(const int property, const double) const = 0;
   virtual string get(const int property, const string) const = 0;
   ...

```

In the first three methods, the property type is specified by one of the template parameters. In further three methods, the type is specified by the second parameter of the method itself: this is required because the last methods take not the constants of a particular enumeration but simply an integer as the first parameter. On the one hand, this is convenient for the continuous numbering of identifiers (the enumeration constants of the three types do not intersect). On the other hand, we need another source for determining the type of value since the type returned by the function/method does not participate in the process of choosing the appropriate [overload](/en/book/basis/functions/functions_overloading).

This approach allows you to get properties based on various inputs available in the calling code. Next, we will create classes based on OrderMonitor (as well as future DealMonitor and PositionMonitor) to select objects according to a set of arbitrary conditions, and there all these methods will be in demand.

Quite often, programs need to get a string representation of any properties, for example, for logging. In the new monitors, this is implemented by the stringify methods. Obviously, they get the values of the requested properties through get method calls mentioned above.

```
   virtual string stringify(const long v, const I property) const = 0;
   
   virtual string stringify(const I property) const
   {
      return stringify(get(property), property);
   }
   
   virtual string stringify(const D property, const string format = NULL) const
   {
      if(format == NULL) return (string)get(property);
      return StringFormat(format, get(property));
   }
   
   virtual string stringify(const S property) const
   {
      return get(property);
   }
   ...

```

The only method that has not received implementation is the first version of stringify for type long. This is due to the fact that the group of integer properties, as we saw in the previous section, actually contain different application types, including date and time, enumerations, and integers. Therefore, only derived classes can provide their conversion to understandable strings. This situation is common for all trading entities, not only orders but also deals and positions the properties of which we will consider later.

When an integer property contains an enumeration element (for example, ENUM_ORDER_TYPE, ORDER_TYPE_FILLING, etc.), you should use the EnumToString function to convert it to a string. This task is fulfilled by a helper method enumstr. Soon we will see its widespread use in specific monitor classes, starting with OrderMonitor after a couple of paragraphs.

```
   template<typename E>
   static string enumstr(const long v)
   {
      return EnumToString((E)v);
   }

```

To log all properties of a particular type, we have created the list2log method which uses stringify in a loop.

```
   template<typename E>
   void list2log() const
   {
      E e = (E)0; // suppress warning 'possible use of uninitialized variable'
      int array[];
      const int n = EnumToArray(e, array, 0, USHORT_MAX);
      Print(typename(E), " Count=", n);
      for(int i = 0; i < n; ++i)
      {
         e = (E)array[i];
         PrintFormat("% 3d %s=%s", i, EnumToString(e), stringify(e));
      }
   }

```

Finally, to make it easier to log the properties of all three groups, there is a method print which calls list2log three times for each group of properties.

```
   virtual void print() const
   {
      if(!ready) return;
      
      Print(typename(this));
      list2log<I>();
      list2log<D>();
      list2log<S>();
   }

```

Having at our disposal a base template class MonitorInterface, we describe OrderMonitorInterface, where we specify certain enumeration types for orders from the previous section and provide an implementation of stringify for integer properties of orders.

```
class OrderMonitorInterface:
   public MonitorInterface<ENUM_ORDER_PROPERTY_INTEGER,
   ENUM_ORDER_PROPERTY_DOUBLE,ENUM_ORDER_PROPERTY_STRING>
{
public:
   // description of properties according to subtypes
   virtual string stringify(const long v,
      const ENUM_ORDER_PROPERTY_INTEGER property) const override
   {
      switch(property)
      {
         case ORDER_TYPE:
            return enumstr<ENUM_ORDER_TYPE>(v);
         case ORDER_STATE:
            return enumstr<ENUM_ORDER_STATE>(v);
         case ORDER_TYPE_FILLING:
            return enumstr<ENUM_ORDER_TYPE_FILLING>(v);
         case ORDER_TYPE_TIME:
            return enumstr<ENUM_ORDER_TYPE_TIME>(v);
         case ORDER_REASON:
            return enumstr<ENUM_ORDER_REASON>(v);
         
         case ORDER_TIME_SETUP:
         case ORDER_TIME_EXPIRATION:
         case ORDER_TIME_DONE:
            return TimeToString(v, TIME_DATE | TIME_SECONDS);
         
         case ORDER_TIME_SETUP_MSC:
         case ORDER_TIME_DONE_MSC:
            return STR_TIME_MSC(v);
      }
      
      return (string)v;
   }
};

```

The STR_TIME_MSC macro for displaying time in milliseconds is defined as follows:

```
#define STR_TIME_MSC(T) (TimeToString((T) / 1000, TIME_DATE | TIME_SECONDS) \
    + StringFormat("'%03d", (T) % 1000))

```

Now we are ready to describe the final class for reading the properties of any order: OrderMonitor derived from OrderMonitorInterface. The order ticket is passed to the constructor, and it is selected in the trading environment using OrderSelect.

```
class OrderMonitor: public OrderMonitorInterface
{
public:
   const ulong ticket;
   OrderMonitor(const long t): ticket(t)
   {
      if(!OrderSelect(ticket))
      {
         PrintFormat("Error: OrderSelect(%lld) failed: %s",
            ticket, E2S(_LastError));
      }
      else
      {
         ready = true;
      }
   }
   ...

```

The main working part of the monitor consists of redefinitions of virtual functions for reading properties. Here we see the OrderGetInteger, OrderGetDouble, and OrderGetString function calls.

```
   virtual long get(const ENUM_ORDER_PROPERTY_INTEGER property) const override
   {
      return OrderGetInteger(property);
   }
   
   virtual double get(const ENUM_ORDER_PROPERTY_DOUBLE property) const override
   {
      return OrderGetDouble(property);
   }
   
   virtual string get(const ENUM_ORDER_PROPERTY_STRING property) const override
   {
      return OrderGetString(property);
   }
   
   virtual long get(const int property, const long) const override
   {
      return OrderGetInteger((ENUM_ORDER_PROPERTY_INTEGER)property);
   }
   
   virtual double get(const int property, const double) const override
   {
      return OrderGetDouble((ENUM_ORDER_PROPERTY_DOUBLE)property);
   }
   
   virtual string get(const int property, const string)  const override
   {
      return OrderGetString((ENUM_ORDER_PROPERTY_STRING)property);
   }
};

```

This code fragment is presented in a short form: operators for working with orders in the history have been removed from it. we will see the full code of OrderMonitor later when we explore this aspect in the following sections.

It is important to note that the monitor object does not store copies of its properties. Therefore, access to get methods must be carried out immediately after the creation of the object and, accordingly, the call OrderSelect. To read the properties at a later period, you will need to allocate the order again in the internal cache of the MQL program, for example, by calling the method refresh.

```
   void refresh()
   {
      ready = OrderSelect(ticket);
   }

```

Let's test the work of OrderMonitor by adding it to the Expert Advisor MarketOrderSend.mq5. A new version named MarketOrderSendMonitor.mq5 connects the file OrderMonitor.mqh by the directive #include, and in the body of the function OnTimer (in the block of successful confirmation of opening a position on an order) creates a monitor object and calls its print method.

```
#include <MQL5Book/OrderMonitor.mqh>
...
void OnTimer()
{
   ...
   const ulong order = (wantToBuy ?
      request.buy(volume, Price) :
      request.sell(volume, Price));
   if(order != 0)
   {
      Print("OK Order: #=", order);
      if(request.completed())
      {
         Print("OK Position: P=", request.result.position);
         
         OrderMonitor m(order);
         m.print();
         ...
      }
   }
}

```

In the log, we should see new lines containing all the properties of the order.

```
OK Order: #=1287846602
Waiting for position for deal D=1270417032
OK Position: P=1287846602
MonitorInterface<ENUM_ORDER_PROPERTY_INTEGER, »
   » ENUM_ORDER_PROPERTY_DOUBLE,ENUM_ORDER_PROPERTY_STRING>
ENUM_ORDER_PROPERTY_INTEGER Count=14
  0 ORDER_TIME_SETUP=2022.03.21 13:28:59
  1 ORDER_TIME_EXPIRATION=1970.01.01 00:00:00
  2 ORDER_TIME_DONE=2022.03.21 13:28:59
  3 ORDER_TYPE=ORDER_TYPE_BUY
  4 ORDER_TYPE_FILLING=ORDER_FILLING_FOK
  5 ORDER_TYPE_TIME=ORDER_TIME_GTC
  6 ORDER_STATE=ORDER_STATE_FILLED
  7 ORDER_MAGIC=1234567890
  8 ORDER_POSITION_ID=1287846602
  9 ORDER_TIME_SETUP_MSC=2022.03.21 13:28:59'572
 10 ORDER_TIME_DONE_MSC=2022.03.21 13:28:59'572
 11 ORDER_POSITION_BY_ID=0
 12 ORDER_TICKET=1287846602
 13 ORDER_REASON=ORDER_REASON_EXPERT
ENUM_ORDER_PROPERTY_DOUBLE Count=7
  0 ORDER_VOLUME_INITIAL=0.01
  1 ORDER_VOLUME_CURRENT=0.0
  2 ORDER_PRICE_OPEN=1.10275
  3 ORDER_PRICE_CURRENT=1.10275
  4 ORDER_PRICE_STOPLIMIT=0.0
  5 ORDER_SL=0.0
  6 ORDER_TP=0.0
ENUM_ORDER_PROPERTY_STRING Count=3
  0 ORDER_SYMBOL=EURUSD
  1 ORDER_COMMENT=
  2 ORDER_EXTERNAL_ID=
TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, »
   » @ 1.10275, P=1287846602, M=1234567890
DONE, D=1270417032, #=1287846602, V=0.01, @ 1.10275, Bid=1.10275, Ask=1.10275, »
   » Request executed, Req=3

```

The fourth line starts the output from the print method which includes the full name of the monitor object MonitorInterface together with parameter types (in this case, the triple ENUM_ORDER_PROPERTY) and then all the properties of a particular order.

However, property printing is not the most interesting action a monitor can provide. The task of selecting orders by conditions (values of arbitrary properties) is much more in demand among Experts Advisors. Using the monitor as an auxiliary tool, we will create a mechanism for filtering orders similar to what we have done for symbols: [SymbolFilter.mqh](/en/book/automation/symbols/symbols_currencies).
