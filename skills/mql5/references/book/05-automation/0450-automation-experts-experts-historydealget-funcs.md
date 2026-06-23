# Functions for reading deal properties from history

To read deal properties, there are groups of functions organized by [property type](/en/book/automation/experts/experts_deal_properties): integer, real and string. Before calling functions, you need to select the desired [period of history](/en/book/automation/experts/experts_history_select) and thus ensure the availability of deals with tickets that are passed in the first parameter (ticket) of all functions.

There are two forms for each type of property: returning a value directly and writing to a variable by reference. The second form returns true to indicate success. The first form will simply return 0 on error. The error code is in the _LastError variable.

Integer and compatible property types (datetime, enumerations) can be obtained using the HistoryDealGetInteger function.

long HistoryDealGetInteger(ulong ticket, ENUM_DEAL_PROPERTY_INTEGER property)

bool HistoryDealGetInteger(ulong ticket, ENUM_DEAL_PROPERTY_INTEGER property,  

   long &value)

Real properties are read by the HistoryDealGetDouble function.

double HistoryDealGetDouble(ulong ticket, ENUM_DEAL_PROPERTY_DOUBLE property)

bool HistoryDealGetDouble(ulong ticket, ENUM_DEAL_PROPERTY_DOUBLE property,  

   double &value)

For string properties there is the HistoryDealGetString function.

string HistoryDealGetString(ulong ticket, ENUM_DEAL_PROPERTY_STRING property)

bool HistoryDealGetString(ulong ticket, ENUM_DEAL_PROPERTY_STRING property,  

   string &value)

A unified reading of deal properties will be provided by the DealMonitor class (DealMonitor.mqh), organized in exactly the same way as OrderMonitor and PositionMonitor. The base class is DealMonitorInterface, inherited from the template MonitorInterface (we described it in the section [Functions for reading the properties of active orders](/en/book/automation/experts/experts_orderget_funcs)). It is at this level that the specific types of ENUM_DEAL_PROPERTY enumerations are specified as template parameters and the specific implementation of the stringify method.

```
#include <MQL5Book/TradeBaseMonitor.mqh>
   
class DealMonitorInterface:
   public MonitorInterface<ENUM_DEAL_PROPERTY_INTEGER,
   ENUM_DEAL_PROPERTY_DOUBLE,ENUM_DEAL_PROPERTY_STRING>
{
public:
   // property descriptions taking into account integer subtypes
   virtual string stringify(const long v,
      const ENUM_DEAL_PROPERTY_INTEGER property) const override
   {
      switch(property)
      {
         case DEAL_TYPE:
            return enumstr<ENUM_DEAL_TYPE>(v);
         case DEAL_ENTRY:
            return enumstr<ENUM_DEAL_ENTRY>(v);
         case DEAL_REASON:
            return enumstr<ENUM_DEAL_REASON>(v);
         
         case DEAL_TIME:
            return TimeToString(v, TIME_DATE | TIME_SECONDS);
         
         case DEAL_TIME_MSC:
            return STR_TIME_MSC(v);
      }
      
      return (string)v;
   }
};

```

The DealMonitor class below is somewhat similar to a class recently modified to work with history OrderMonitor. In addition to the application of HistoryDeal functions instead of HistoryOrder functions, it should be noted that for deals there is no need to check the ticket in the online environment because deals exist only in history.

```
class DealMonitor: public DealMonitorInterface
{
   bool historyDealSelectWeak(const ulong t) const
   {
      return ((HistoryDealGetInteger(t, DEAL_TICKET) == t) ||
         (HistorySelect(0, LONG_MAX) && (HistoryDealGetInteger(t, DEAL_TICKET) == t)));
   }
public:
   const ulong ticket;
   DealMonitor(const long t): ticket(t)
   {
      if(!historyDealSelectWeak(ticket))
      {
         PrintFormat("Error: HistoryDealSelect(%lld) failed", ticket);
      }
      else
      {
         ready = true;
      }
   }
   
   virtual long get(const ENUM_DEAL_PROPERTY_INTEGER property) const override
   {
      return HistoryDealGetInteger(ticket, property);
   }
   
   virtual double get(const ENUM_DEAL_PROPERTY_DOUBLE property) const override
   {
      return HistoryDealGetDouble(ticket, property);
   }
   
   virtual string get(const ENUM_DEAL_PROPERTY_STRING property) const override
   {
      return HistoryDealGetString(ticket, property);
   }
   ...
};

```

Based on DealMonitor and TradeFilter it is easy to create a deal filter (DealFilter.mqh). Recall that TradeFilter, as the base class for many entities, was described in the section [Selecting orders by properties](/en/book/automation/experts/experts_order_filter).

```
#include <MQL5Book/DealMonitor.mqh>
#include <MQL5Book/TradeFilter.mqh>
   
class DealFilter: public TradeFilter<DealMonitor,
   ENUM_DEAL_PROPERTY_INTEGER,
   ENUM_DEAL_PROPERTY_DOUBLE,
   ENUM_DEAL_PROPERTY_STRING>
{
protected:
   virtual int total() const override
   {
      return HistoryDealsTotal();
   }
   virtual ulong get(const int i) const override
   {
      return HistoryDealGetTicket(i);
   }
};

```

As a generalized example of working with histories, consider the position history recovery script TradeHistoryPrint.mq5.

TradeHistoryPrint

The script will build a history for the current chart symbol.

We first need filters for deals and orders.

```
#include <MQL5Book/OrderFilter.mqh>
#include <MQL5Book/DealFilter.mqh>

```

From the deals, we will extract the position IDs and, based on them, we will request details about the orders.

The history can be viewed in its entirety or for a specific position, for which we will provide a mode selection and an input field for the identifier in the input variables.

```
enum SELECTOR_TYPE
{
   TOTAL,    // Whole history
   POSITION, // Position ID
};
   
input SELECTOR_TYPE Type = TOTAL;
input ulong PositionID = 0; // Position ID

```

It should be remembered that sampling a long account history can be an overhead, so it is desirable to provide for caching of the obtained results of history processing in working Expert Advisors, along with the last processing timestamp. With each subsequent analysis of history, you can start the process not from the very beginning, but from a remembered moment.

To display information about history records with column alignment in a visually attractive way, it makes sense to represent it as an array of structures. However, our filters already support querying data stored in special structures - tuples. Therefore, we will apply a trick: we will describe our application structures, observing the rules of tuples:

- The first field must have the name _1; it is optionally used in the sorting algorithm.
- The size function returning the number of fields must be described in the structure.
- The structure should have a template method assign to populate fields from the properties of the passed monitor object derived from MonitorInterface.

In standard tuples, the method assign is described like this:

```
   template<typename M> 
   void assign(const int &properties[], M &m);

```

As the first parameter, it receives an array with the property IDs corresponding to the fields we are interested in. In fact, this is the array that is passed by the calling code to the select method of the filter (TradeFilter::select), and then by reference it gets to assign. But since we will now create not some standard tuples but our own structures that "know" about the applied nature of their fields, we can leave the array with property identifiers inside the structure itself and not "drive" it into the filter and back to the assign method of the same structure.

In particular, to request deals, we describe the DealTuple structure with 8 fields. Their identifiers will be specified in the fields static array.

```
struct DealTuple
{
   datetime _1;   // deal time
   ulong deal;    // deal ticket
   ulong order;   // order ticket
   string type;   // ENUM_DEAL_TYPE as string 
   string in_out; // ENUM_DEAL_ENTRY as string 
   double volume;
   double price;
   double profit;
   
   static int size() { return 8; }; // number of properties 
   static const int fields[]; // identifiers of the requested deal properties
   ...
};
   
static const int DealTuple::fields[] =
{
   DEAL_TIME, DEAL_TICKET, DEAL_ORDER, DEAL_TYPE,
   DEAL_ENTRY, DEAL_VOLUME, DEAL_PRICE, DEAL_PROFIT
};

```

This approach brings together identifiers and fields to store the corresponding values in a single place, which makes it easier to understand and maintain the source code.

Filling fields with property values will require a slightly modified (simplified) version of the assign method which takes the IDs from the fields array and not from the input parameter.

```
struct DealTuple
{
   ...
   template<typename M> // M is derived from MonitorInterface<>
   void assign(M &m)
   {
      static const int DEAL_TYPE_ = StringLen("DEAL_TYPE_");
      static const int DEAL_ENTRY_ = StringLen("DEAL_ENTRY_");
      static const ulong L = 0; // default type declaration (dummy)
      
      _1 = (datetime)m.get(fields[0], L);
      deal = m.get(fields[1], deal);
      order = m.get(fields[2], order);
      const ENUM_DEAL_TYPE t = (ENUM_DEAL_TYPE)m.get(fields[3], L);
      type = StringSubstr(EnumToString(t), DEAL_TYPE_);
      const ENUM_DEAL_ENTRY e = (ENUM_DEAL_ENTRY)m.get(fields[4], L);
      in_out = StringSubstr(EnumToString(e), DEAL_ENTRY_);
      volume = m.get(fields[5], volume);
      price = m.get(fields[6], price);
      profit = m.get(fields[7], profit);
   }
};

```

At the same time, we convert the numeric elements of the ENUM_DEAL_TYPE and ENUM_DEAL_ENTRY enumerations into user-friendly strings. Of course, this is only needed for logging. For programmatic analysis, the types should be left as they are.

Since we have invented a new version of the assign method in their tuples, you need to add a new version of the select method for it in the TradeFilter class. The innovation will certainly be useful for other programs, and therefore we will introduce it directly into TradeFilter, not into some new derived class.

```
template<typename T,typename I,typename D,typename S>
class TradeFilter
{
   ...
   template<typename U> // U must have first field _1 and method assign(T)
   bool select(U &data[], const bool sort = false) const
   {
      const int n = total();
      // loop through the elements
      for(int i = 0; i < n; ++i)
      {
         const ulong t = get(i);
         // read properties through the monitor object
         T m(t);
         // check all filtering conditions
         if(match(m, longs)
         && match(m, doubles)
         && match(m, strings))
         {
            // for a suitable object, add its properties to an array
            const int k = EXPAND(data);
            data[k].assign(m);
         }
      }
      
      if(sort)
      {
         static const U u;
         sortTuple(data, u._1);
      }
      
      return true;
   }

```

Recall that all template methods are not implemented by the compiler until they are called in code with a specific type. Therefore, the presence of such patterns in TradeFilter does not oblige you to include any tuple header files or describe similar structures if you don't use them.

So, if earlier, to select transactions using a standard tuple, we would have to write like this:

```
#include <MQL5Book/Tuples.mqh>
...
DealFilter filter;
int properties[] =
{
   DEAL_TIME, DEAL_TICKET, DEAL_ORDER, DEAL_TYPE,
   DEAL_ENTRY, DEAL_VOLUME, DEAL_PRICE, DEAL_PROFIT
};
Tuple8<ulong,ulong,ulong,ulong,ulong,double,double,double> tuples[];
filter.let(DEAL_SYMBOL, _Symbol).select(properties, tuples);

```

Then with a customized structure, everything is much simpler:

```
DealFilter filter;
DealTuple tuples[];
filter.let(DEAL_SYMBOL, _Symbol).select(tuples);

```

Similar to the DealTuple structure, let's describe the 10-field structure for orders OrderTuple.

```
struct OrderTuple
{
   ulong _1;       // ticket (also used as 'ulong' prototype)
   datetime setup;
   datetime done;
   string type;
   double volume;
   double open;
   double current;
   double sl;
   double tp;
   string comment;
   
   static int size() { return 10; }; // number of properties
   static const int fields[]; // identifiers of requested order properties
   
   template<typename M> // M is derived from MonitorInterface<>
   void assign(M &m)
   {
      static const int ORDER_TYPE_ = StringLen("ORDER_TYPE_");
      
      _1 = m.get(fields[0], _1);
      setup = (datetime)m.get(fields[1], _1);
      done = (datetime)m.get(fields[2], _1);
      const ENUM_ORDER_TYPE t = (ENUM_ORDER_TYPE)m.get(fields[3], _1);
      type = StringSubstr(EnumToString(t), ORDER_TYPE_);
      volume = m.get(fields[4], volume);
      open = m.get(fields[5], open);
      current = m.get(fields[6], current);
      sl = m.get(fields[7], sl);
      tp = m.get(fields[8], tp);
      comment = m.get(fields[9], comment);
   }
};
   
static const int OrderTuple::fields[] =
{
   ORDER_TICKET, ORDER_TIME_SETUP, ORDER_TIME_DONE, ORDER_TYPE, ORDER_VOLUME_INITIAL,
   ORDER_PRICE_OPEN, ORDER_PRICE_CURRENT, ORDER_SL, ORDER_TP, ORDER_COMMENT
};

```

Now everything is ready to implement the main function of the script — OnStart. At the very beginning, we will describe the objects of filters for deals and orders.

```
void OnStart()
{
   DealFilter filter;
   HistoryOrderFilter subfilter;
   ...

```

Depending on the input variables, we choose either the entire history or a specific position.

```
   if(PositionID == 0 || Type == TOTAL)
   {
      HistorySelect(0, LONG_MAX);
   }
   else if(Type == POSITION)
   {
      HistorySelectByPosition(PositionID);
   }
   ...

```

Next, we will collect all position identifiers in an array, or leave one specified by the user.

```
   ulong positions[];
   if(PositionID == 0)
   {
      ulong tickets[];
      filter.let(DEAL_SYMBOL, _Symbol)
         .select(DEAL_POSITION_ID, tickets, positions, true); // true - sorting
      ArrayUnique(positions);
   }
   else
   {
      PUSH(positions, PositionID);
   }
   
   const int n = ArraySize(positions);
   Print("Positions total: ", n);
   if(n == 0) return;
   ...

```

The helper function ArrayUnique leaves non-repeating elements in the array. It requires the source array to be sorted for it to work.

Further, in a loop through positions, we request deals and orders related to each of them. Deals are sorted by the first field of the DealTuple structure, i.e., by time. Perhaps the most interesting is the calculation of profit/loss on a position. To do this, we sum the values of the profit field of all deals.

```
   for(int i = 0; i < n; ++i)
   {
      DealTuple deals[];
      filter.let(DEAL_POSITION_ID, positions[i]).select(deals, true);
      const int m = ArraySize(deals);
      if(m == 0)
      {
         Print("Wrong position ID: ", positions[i]);
         break; // invalid id set by user
      }
      double profit = 0; // TODO: need to take into account commissions, swaps and fees
      for(int j = 0; j < m; ++j) profit += deals[j].profit;
      PrintFormat("Position: % 8d %16lld Profit:%f", i + 1, positions[i], (profit));
      ArrayPrint(deals);
      
      Print("Order details:");
      OrderTuple orders[];
      subfilter.let(ORDER_POSITION_ID, positions[i], IS::OR_EQUAL)
         .let(ORDER_POSITION_BY_ID, positions[i], IS::OR_EQUAL)
         .select(orders);
      ArrayPrint(orders);
   }
}

```

This code does not analyze commissions (DEAL_COMMISSION), swaps (DEAL_SWAP), and fees (DEAL_FEE) in deal properties. In real Expert Advisors, this should probably be done (depending on the requirements of the strategy). We will look at another example of trading history analysis in the section on [testing multicurrency Expert Advisors](/en/book/automation/tester/tester_multicurrency_sync), and there we will take into account this moment.

You can compare the results of the script with the table on the History tab in the terminal: its Profit column shows the net profit for each position (swaps, commissions, and fees are in adjacent columns, but they need to be included).

It is important to note that an order of the ORDER_TYPE_CLOSE_BY type will be displayed in both positions only if the entire history is selected in the settings. If a specific position was selected, the system will include such an order only in one of them (the one that was specified in the trade request first, in the position field) but not the second one (which was specified in position_by).

Below is an example of the result of the script for a symbol with a small history.

```
Positions total: 3
Position:        1       1253500309 Profit:238.150000
                   [_1]     [deal]    [order] [type] [in_out] [volume]  [price]  [profit]
[0] 2022.02.04 17:34:57 1236049891 1253500309 "BUY"  "IN"      1.00000 76.23900   0.00000
[1] 2022.02.14 16:28:41 1242295527 1259788704 "SELL" "OUT"     1.00000 76.42100 238.15000
Order details:
          [_1]             [setup]              [done] [type] [volume]   [open] [current] »
   » [sl] [tp] [comment]
[0] 1253500309 2022.02.04 17:34:57 2022.02.04 17:34:57 "BUY"   1.00000 76.23900  76.23900 »
   » 0.00 0.00 ""       
[1] 1259788704 2022.02.14 16:28:41 2022.02.14 16:28:41 "SELL"  1.00000 76.42100  76.42100 »
   » 0.00 0.00 ""       
Position:        2       1253526613 Profit:878.030000
                   [_1]     [deal]    [order] [type] [in_out] [volume]  [price]  [profit]
[0] 2022.02.07 10:00:00 1236611994 1253526613 "BUY"  "IN"      1.00000 75.75000   0.00000
[1] 2022.02.14 16:28:40 1242295517 1259788693 "SELL" "OUT"     1.00000 76.42100 878.03000
Order details:
          [_1]             [setup]              [done]      [type] [volume]   [open] [current] »
   » [sl] [tp] [comment]
[0] 1253526613 2022.02.04 17:55:18 2022.02.07 10:00:00 "BUY_LIMIT"  1.00000 75.75000  75.67000 »
   » 0.00 0.00 ""       
[1] 1259788693 2022.02.14 16:28:40 2022.02.14 16:28:40 "SELL"       1.00000 76.42100  76.42100 »
   » 0.00 0.00 ""       
Position:        3       1256280710 Profit:4449.040000
                   [_1]     [deal]    [order] [type] [in_out] [volume]  [price]   [profit]
[0] 2022.02.09 13:17:52 1238797056 1256280710 "BUY"  "IN"      2.00000 74.72100    0.00000
[1] 2022.02.14 16:28:39 1242295509 1259788685 "SELL" "OUT"     2.00000 76.42100 4449.04000
Order details:
          [_1]             [setup]              [done] [type] [volume]   [open] [current] »
   » [sl] [tp] [comment]
[0] 1256280710 2022.02.09 13:17:52 2022.02.09 13:17:52 "BUY"   2.00000 74.72100  74.72100 »
   » 0.00 0.00 ""       
[1] 1259788685 2022.02.14 16:28:39 2022.02.14 16:28:39 "SELL"  2.00000 76.42100  76.42100 »
   » 0.00 0.00 ""       

```

The case of increasing a position (two "IN" deals) and its reversal (an "INOUT" deal of a larger volume) on a netting account is shown in the following fragment.

```
Position:        5        219087383 Profit:0.170000
                   [_1]    [deal]   [order] [type] [in_out] [volume] [price] [profit]
[0] 2022.03.29 08:03:33 215612450 219087383 "BUY"  "IN"      0.01000 1.10011  0.00000
[1] 2022.03.29 08:04:05 215612451 219087393 "BUY"  "IN"      0.01000 1.10009  0.00000
[2] 2022.03.29 08:04:29 215612457 219087400 "SELL" "INOUT"   0.03000 1.10018  0.16000
[3] 2022.03.29 08:04:34 215612460 219087403 "BUY"  "OUT"     0.01000 1.10017  0.01000
Order details:
         [_1]             [setup]              [done] [type] [volume] [open] [current] »
   » [sl] [tp] [comment]
[0] 219087383 2022.03.29 08:03:33 2022.03.29 08:03:33 "BUY"   0.01000 0.0000   1.10011 »
   » 0.00 0.00 ""       
[1] 219087393 2022.03.29 08:04:05 2022.03.29 08:04:05 "BUY"   0.01000 0.0000   1.10009 »
   » 0.00 0.00 ""       
[2] 219087400 2022.03.29 08:04:29 2022.03.29 08:04:29 "SELL"  0.03000 0.0000   1.10018 »
   » 0.00 0.00 ""       
[3] 219087403 2022.03.29 08:04:34 2022.03.29 08:04:34 "BUY"   0.01000 0.0000   1.10017 »
   » 0.00 0.00 ""       

```

We will consider a partial history using the example of specific positions for the case of an opposite closure on a hedging account. First, you can view the first position separately: PositionID=1276109280. It will be shown in full regardless of the input parameter Type.

```
Positions total: 1
Position:        1       1276109280 Profit:-0.040000
                   [_1]     [deal]    [order] [type] [in_out] [volume] [price] [profit]
[0] 2022.03.07 12:20:53 1258725455 1276109280 "BUY"  "IN"      0.01000 1.08344  0.00000
[1] 2022.03.07 12:20:58 1258725503 1276109328 "SELL" "OUT_BY"  0.01000 1.08340 -0.04000
Order details:
          [_1]             [setup]              [done]     [type] [volume]  [open] [current] »
   » [sl] [tp]                    [comment]
[0] 1276109280 2022.03.07 12:20:53 2022.03.07 12:20:53 "BUY"       0.01000 1.08344   1.08344 »
   » 0.00 0.00 ""                          
[1] 1276109328 2022.03.07 12:20:58 2022.03.07 12:20:58 "CLOSE_BY"  0.01000 1.08340   1.08340 »
   » 0.00 0.00 "#1276109280 by #1276109283"

```

You can also see the second one: PositionID=1276109283. However, if Type equals "position", to select a fragment of history, the function HistorySelectByPosition is used, and as a result there will be only one exit order (despite the fact that there are two deals).

```
Positions total: 1
Position:        1       1276109283 Profit:0.000000
                   [_1]     [deal]    [order] [type] [in_out] [volume] [price] [profit]
[0] 2022.03.07 12:20:53 1258725458 1276109283 "SELL" "IN"      0.01000 1.08340  0.00000
[1] 2022.03.07 12:20:58 1258725504 1276109328 "BUY"  "OUT_BY"  0.01000 1.08344  0.00000
Order details:
          [_1]             [setup]              [done] [type] [volume]  [open] [current] »
   » [sl] [tp] [comment]
[0] 1276109283 2022.03.07 12:20:53 2022.03.07 12:20:53 "SELL"  0.01000 1.08340   1.08340 »
   » 0.00 0.00 ""       

```

If we set Type to the "whole history", a "CLOSE_BY" order will appear.

```
Positions total: 1
Position:        1       1276109283 Profit:0.000000
                   [_1]     [deal]    [order] [type] [in_out] [volume] [price] [profit]
[0] 2022.03.07 12:20:53 1258725458 1276109283 "SELL" "IN"      0.01000 1.08340  0.00000
[1] 2022.03.07 12:20:58 1258725504 1276109328 "BUY"  "OUT_BY"  0.01000 1.08344  0.00000
Order details:
          [_1]             [setup]              [done]     [type] [volume]  [open] [current] »
   » [sl] [tp]                    [comment]
[0] 1276109283 2022.03.07 12:20:53 2022.03.07 12:20:53 "SELL"      0.01000 1.08340   1.08340 »
   » 0.00 0.00 ""                          
[1] 1276109328 2022.03.07 12:20:58 2022.03.07 12:20:58 "CLOSE_BY"  0.01000 1.08340   1.08340 »
   » 0.00 0.00 "#1276109280 by #1276109283"

```

With such settings, the history is selected completely, but the filter leaves only those orders, in which the identifier of the specified position is found in the ORDER_POSITION_ID or ORDER_POSITION_BY_ID properties. For composing conditions with a logical OR, the IS::OR_EQUAL element has been added to the TradeFilter class. You can additionally study it.
