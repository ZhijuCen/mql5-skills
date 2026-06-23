# Functions for reading order properties from history

The functions for reading properties of historical orders are divided into 3 groups according to the basic type of property values, in accordance with the division of identifiers of available properties into three enumerations: ENUM_ORDER_PROPERTY_INTEGER, ENUM_ORDER_PROPERTY_DOUBLE and ENUM_ORDER_PROPERTY_STRING discussed earlier in a [separate section](/en/book/automation/experts/experts_order_properties) when exploring active orders.

Before calling these functions, you need to somehow [select the appropriate set of tickets in the history](/en/book/automation/experts/experts_history_select).

If you try to read the properties of an order or a deal having tickets outside the selected history context, the environment may generate a WRONG_INTERNAL_PARAMETER (4002) error, which can be analyzed via _LastError.

For each base property type, there are two function forms: one directly returns the value of the requested property, the second one writes it into a parameter passed by reference and returns a success indicator (true) or errors (false).

For integer and compatible types (datetime, enums) of properties there is a dedicated function HistoryOrderGetInteger.

long HistoryOrderGetInteger(ulong ticket, ENUM_ORDER_PROPERTY_INTEGER property)

bool HistoryOrderGetInteger(ulong ticket, ENUM_ORDER_PROPERTY_INTEGER property,  

   long &value)

The function allows you to find out the order property from the selected history by its ticket number.

For real properties, the HistoryOrderGetDouble function is assigned.

double HistoryOrderGetDouble(ulong ticket, ENUM_ORDER_PROPERTY_DOUBLE property)

bool HistoryOrderGetDouble(ulong ticket, ENUM_ORDER_PROPERTY_DOUBLE property,  

   double &value)

Finally, string properties can be read with HistoryOrderGetString.

string HistoryOrderGetString(ulong ticket, ENUM_ORDER_PROPERTY_STRING property)

bool HistoryOrderGetString(ulong ticket, ENUM_ORDER_PROPERTY_STRING property,  

   string &value)

Now we can supplement the OrderMonitor class (OrderMonitor.mqh) for working with historical orders. First, let's add a boolean variable to the history class, which we will fill in the constructor based on the segment in which the order with the passed ticket was selected: among the active ones (OrderSelect) or in history (HistoryOrderSelect).

```
class OrderMonitor: public OrderMonitorInterface
{
   bool history;
   
public:
   const ulong ticket;
   OrderMonitor(const long t): ticket(t), history(!OrderSelect(t))
   {
      if(history && !HistoryOrderSelect(ticket))
      {
         PrintFormat("Error: OrderSelect(%lld) failed: %s", ticket, E2S(_LastError));
      }
      else
      {
         ResetLastError();
         ready = true;
      }
   }
   ...

```

We need to call the ResetLastError function in a successful if branch in order to reset the possible error that could be set by the OrderSelect function (if the order is in history).

In fact, this version of the constructor contains a serious logical error, and we will return to it after a few paragraphs.

To read properties in get methods, we now call different built-in functions, depending on the value of the history variable.

```
   virtual long get(const ENUM_ORDER_PROPERTY_INTEGER property) const override
   {
      return history ? HistoryOrderGetInteger(ticket, property) : OrderGetInteger(property);
   }
   
   virtual double get(const ENUM_ORDER_PROPERTY_DOUBLE property) const override
   {
      return history ? HistoryOrderGetDouble(ticket, property) : OrderGetDouble(property);
   }
   
   virtual string get(const ENUM_ORDER_PROPERTY_STRING property) const override
   {
      return history ? HistoryOrderGetString(ticket, property) : OrderGetString(property);
   }
   ...

```

The main purpose of the OrderMonitor class is to supply data to other analytical classes. The OrderMonitor objects are used to filter active orders in the OrderFilter class, and we need a similar class for selecting orders by arbitrary conditions on the history: HistoryOrderFilter.

Let's write this class in the same file OrderFilter.mqh. It uses two new functions for working with history: HistoryOrdersTotal and HistoryOrderGetTicket.

```
class HistoryOrderFilter: public TradeFilter<OrderMonitor,
   ENUM_ORDER_PROPERTY_INTEGER,
   ENUM_ORDER_PROPERTY_DOUBLE,
   ENUM_ORDER_PROPERTY_STRING>
{
protected:
   virtual int total() const override
   {
      return HistoryOrdersTotal();
   }
   virtual ulong get(const int i) const override
   {
      return HistoryOrderGetTicket(i);
   }
};

```

This simple code inherits from the template class TradeFilter, where the class is passed as the first parameter of the template OrderMonitor to read the properties of the corresponding objects (we saw an analog for positions, and will soon create one for deals).

Here lies the problem with the OrderMonitor constructor. As we learned in the section [Selecting orders and deals from history](/en/book/automation/experts/experts_history_select), to analyze the account we must first set up the context with one of the functions such as HistorySelect. So here in the source code HistoryOrderFilter it is assumed that the MQL program has already selected the required history fragment. However, the new, intermediate version of the OrderMonitor constructor uses the HistoryOrderSelect call to check the existence of a ticket in history. Meanwhile, this function resets the previous context of historical orders and selects a single order.

So we need a helper method historyOrderSelectWeak to validate the ticket in a "soft" way without breaking the existing context. To do this, we can simply check if the ORDER_TICKET property is equal to the passed ticket t: (HistoryOrderGetInteger(t, ORDER_TICKET) == t). If such a ticket has already been selected (available), the check will succeed, and the monitor does not need to manipulate the history.

```
class OrderMonitor: public OrderMonitorInterface
{
   bool historyOrderSelectWeak(const ulong t) const
   {
      return (((HistoryOrderGetInteger(t, ORDER_TICKET) == t) ||
         (HistorySelect(0, LONG_MAX) && (HistoryOrderGetInteger(t, ORDER_TICKET) == t))));
   }
   bool history;
   
public:
   const ulong ticket;
   OrderMonitor(const long t): ticket(t), history(!OrderSelect(t))
   {
      if(history && !historyOrderSelectWeak(ticket))
      {
         PrintFormat("Error: OrderSelect(%lld) failed: %s", ticket, E2S(_LastError));
      }
      else
      {
         ResetLastError();
         ready = true;
      }
   }

```

An example of applying order filtering on history will be considered in the next section after we prepare a similar functionality for deals.
