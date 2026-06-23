# Overview of object property access functions

Objects have various types of properties that can be read and set using ObjectGet and ObjectSet functions. As we know, this principle has already been applied to the chart  (see the [Overview of functions for working with the full set of chart properties](/en/book/applications/charts/charts_properties_overview) section).

All such functions take as their first three parameters a chart identifier, an object name, and a property identifier, which must be a member of one of the ENUM_OBJECT_PROPERTY_INTEGER, ENUM_OBJECT_PROPERTY_DOUBLE, or ENUM_OBJECT_PROPERTY_STRING enumerations. We will study specific properties gradually in the following sections. Their complete pivot tables can be found in the MQL5 documentation, on the page with [Object Properties](https://www.mql5.com/en/docs/constants/objectconstants/enum_object_property).

It should be noted that property identifiers in all three enumerations do not intersect, which makes it possible to combine their joint processing into a single unified code. We will use this in the examples.

Some properties are read-only and will be marked "r/o" (read-only).

As in the case of the plotting API, the property read functions have a short form and a long form: the short form directly returns the requested value, and the long form returns a boolean success (true) or errors (false), and the value itself is placed in the last parameter passed by reference. The absence of an error when calling the short form should be checked using the built-in _LastError variable.

When accessing some properties, you must specify an additional parameter (modifier), which is used to indicate the value number or level if the property is multivalued. For example, if an object has several anchor points, then the modifier allows you to select a specific one.

Following are the function prototypes for reading and writing integer properties. Note that the type of values in them is long, which allows you to store properties not only of the int or long types, but also bool, color, datetime, and various enumerations (see below).

bool ObjectSetInteger(long chartId, const string name, ENUM_OBJECT_PROPERTY_INTEGER property, long value)

bool ObjectSetInteger(long chartId, const string name, ENUM_OBJECT_PROPERTY_INTEGER property, int modifier, long value)

long ObjectGetInteger(long chartId, const string name, ENUM_OBJECT_PROPERTY_INTEGER property, int modifier = 0)

bool ObjectGetInteger(long chartId, const string name, ENUM_OBJECT_PROPERTY_INTEGER property, int modifier, long &value)

Functions for real properties are described similarly.

bool ObjectSetDouble(long chartId, const string name, ENUM_OBJECT_PROPERTY_DOUBLE property, double value)

bool ObjectSetDouble(long chartId, const string name, ENUM_OBJECT_PROPERTY_DOUBLE property, int modifier, double value)

double ObjectGetDouble(long chartId, const string name, ENUM_OBJECT_PROPERTY_DOUBLE property, int modifier = 0)

bool ObjectGetDouble(long chartId, const string name, ENUM_OBJECT_PROPERTY_DOUBLE property, int modifier, double &value)

Finally, four of the same functions exist for strings.

bool ObjectSetString(long chartId, const string name, ENUM_OBJECT_PROPERTY_STRING property, const string value)

bool ObjectSetString(long chartId, const string name, ENUM_OBJECT_PROPERTY_STRING property, int modifier, const string value)

string ObjectGetString(long chartId, const string name, ENUM_OBJECT_PROPERTY_STRING property, int modifier = 0)

bool ObjectGetString(long chartId, const string name, ENUM_OBJECT_PROPERTY_STRING property, int modifier, string &value)

To enhance performance, all functions for setting object properties (ObjectSetInteger, ObjectSetDouble, and ObjectSetString) are asynchronous and essentially send commands to the chart to modify the object. Upon successful execution of these functions, the commands are placed in the shared event queue of the chart, indicated by the returned result of true. When an error occurs, the functions will return false, and the error code must be checked in the _LastError variable.

Object properties are changed with some delay, during the processing of the chart event queue. To force the update of the appearance and properties of objects on the chart, especially after changing many objects at once, use the [ChartRedraw](/en/book/applications/charts/charts_redraw) function.

The functions for getting chart properties (ObjectGetInteger, ObjectGetDouble, and ObjectGetString) are synchronous, that is, the calling code waits for the result of their execution. In this case, all commands in the chart queue are executed to get the actual value of the properties.

Let's go back to the example of the script for [deleting objects](/en/book/applications/objects/objects_delete), more precisely, to its new version, ObjectCleanup2.mq5. Recall that in the CustomDeleteAllObjects function, we wanted to implement the ability to select objects based on their properties. Let's say that these properties should be the color and anchor point. To get them, use the ObjectGetInteger function and a pair of ENUM_OBJECT_PROPERTY_INTEGER enumeration elements: OBJPROP_COLOR and OBJPROP_ANCHOR. We will look at them in detail later.

Given this information, the code would be supplemented with the following checks (here, for simplicity, the color and anchor point are given by the clrRed and ANCHOR_TOP constants. In fact, we will provide input variables for them).

```
int CustomDeleteAllObjects(const long chart, const string prefix,
   const int window = -1, const int type = -1)
{
   int count = 0;
   
   for(int i = ObjectsTotal(chart, window, type) - 1; i >= 0; --i)
   {
      const string name = ObjectName(chart, i, window, type);
      // condition on the name and additional properties, such as color and anchor point
      if((StringLen(prefix) == 0 || StringFind(name, prefix) == 0)
         && ObjectGetInteger(0, name, OBJPROP_COLOR) == clrRed
         && ObjectGetInteger(0, name, OBJPROP_ANCHOR) == ANCHOR_TOP)
      {
         count += ObjectDelete(chart, name);
      }
   }
   return count;
}

```

Pay attention to the lines with ObjectGetInteger.

Their entry is long and contains some tautology because specific properties are tied to ObjectGet functions of known types. Also, as the number of conditions increases, it may seem redundant to repeat the chart ID and object name.

To simplify the record, let's turn to the technology that we tested in the ChartModeMonitor.mqh file in the section on [Chart Display Modes](/en/book/applications/charts/charts_mode). Its meaning is to describe an intermediary class with method overloads for reading and writing properties of all types. Let's name the new ObjectMonitor.mqh header file.

The ObjectProxy class closely replicates the structure of the ChartModeMonitorInterface class for charts. The main difference is the presence of virtual methods for setting and getting the chart ID and object name.

```
class ObjectProxy
{
public:
   long get(const ENUM_OBJECT_PROPERTY_INTEGER property, const int modifier = 0)
   {
      return ObjectGetInteger(chart(), name(), property, modifier);
   }
   double get(const ENUM_OBJECT_PROPERTY_DOUBLE property, const int modifier = 0)
   {
      return ObjectGetDouble(chart(), name(), property, modifier);
   }
   string get(const ENUM_OBJECT_PROPERTY_STRING property, const int modifier = 0)
   {
      return ObjectGetString(chart(), name(), property, modifier);
   }
   bool set(const ENUM_OBJECT_PROPERTY_INTEGER property, const long value,
      const int modifier = 0)
   {
      return ObjectSetInteger(chart(), name(), property, modifier, value);
   }
   bool set(const ENUM_OBJECT_PROPERTY_DOUBLE property, const double value,
      const int modifier = 0)
   {
      return ObjectSetDouble(chart(), name(), property, modifier, value);
   }
   bool set(const ENUM_OBJECT_PROPERTY_STRING property, const string value,
      const int modifier = 0)
   {
      return ObjectSetString(chart(), name(), property, modifier, value);
   }
   
   virtual string name() = 0;
   virtual void name(const string) { }
   virtual long chart() { return 0; }
   virtual void chart(const long) { }
};

```

Let's implement these methods in the descendant class (later we will supplement the class hierarchy with the object property monitor, similar to the chart property monitor).

```
class ObjectSelector: public ObjectProxy
{
protected:
   long host; // chart ID
   string id; // chart ID
public:
   ObjectSelector(const string _id, const long _chart = 0): id(_id), host(_chart) { }
   
   virtual string name()
   {
      return id;
   }
   virtual void name(const string _id)
   {
      id = _id;
   }
   virtual void chart(const long _chart) override
   {
      host = _chart;
   }
};

```

We have separated the abstract interface ObjectProxy and its minimal implementation in ObjectSelector because later we may need to implement an array of proxies for multiple objects of the same type, for example. Then it is enough to store an array of names or their common prefix in the new "multiselector" class and ensure that one of them is returned from the name method by calling the overloaded operator []:multiSelector[i].get(OBJPROP_XYZ).

Now let's go back to the ObjectCleanup2.mq5 script and describe two input variables for specifying a color and an anchor point as additional conditions for selecting objects to be deleted.

```
// ObjectCleanup2.mq5
...
input color CustomColor = clrRed;
input ENUM_ARROW_ANCHOR CustomAnchor = ANCHOR_TOP;

```

Let's pass these values to the CustomDeleteAllObjects function, and the new condition checks in the loop over objects can be formulated more compactly thanks to the mediator class.

```
#include <MQL5Book/ObjectMonitor.mqh>
   
void OnStart()
{
   const int n = UseCustomDeleteAll ?
      CustomDeleteAllObjects(0, ObjNamePrefix, CustomColor, CustomAnchor) :
      ObjectsDeleteAll(0, ObjNamePrefix);
   PrintFormat("%d objects deleted", n);
}
   
int CustomDeleteAllObjects(const long chart, const string prefix,
   color clr, ENUM_ARROW_ANCHOR anchor,
   const int window = -1, const int type = -1)
{
   int count = 0;
   for(int i = ObjectsTotal(chart, window, type) - 1; i >= 0; --i)
   {
      const string name = ObjectName(chart, i, window, type);
      
      ObjectSelector s(name);
      ResetLastError();
      if((StringLen(prefix) == 0 || StringFind(s.get(OBJPROP_NAME), prefix) == 0)
      && s.get(OBJPROP_COLOR) == CustomColor
      && s.get(OBJPROP_ANCHOR) == CustomAnchor
      && _LastError != 4203) // OBJECT_WRONG_PROPERTY
      {
         count += ObjectDelete(chart, name);
      }
   }
   return count;
}

```

It is important to note that we specify the name of the object (and the implicit identifier of the current chart 0) only once when creating the ObjectSelector object. Further, all properties are requested by the get method with a single parameter describing the desired property, and the appropriate ObjectGet function will be chosen by the compiler automatically.

The additional check for error code 4203 (OBJECT_WRONG_PROPERTY) allows filtering out objects that do not have the requested property, such as OBJPROP_ANCHOR. In this way, in particular, it is possible to make a selection in which all types of arrows will fall (without the need to separately request different types of OBJ_ARROW_XYZ), but lines and "events" will be excluded from processing.

This is easy to check by first running the ObjectSimpleShowcase.mq5 script on the chart (it will create 14 objects of different types) and then ObjectCleanup2.mq5. If you turn on the UseCustomDeleteAll mode, there will be 5 non-deleted objects on the chart: OBJ_VLINE, OBJ_HLINE, OBJ_ARROW_BUY, OBJ_ARROW_SELL, and OBJ_EVENT. The first two and the last do not have the OBJPROP_ANCHOR property, and the buy and sell arrows do not pass by color (it is assumed that the color of all other created objects is red by default).

However, ObjectSelector is provided not only for the sake of the above simple application. It is the basis for creating a property monitor for a single object, similar to what was implemented for charts. So the ObjectMonitor.mqh header file contains something more interesting.

```
class ObjectMonitorInterface: public ObjectSelector
{
public:
   ObjectMonitorInterface(const string _id, const long _chart = 0):
      ObjectSelector(_id, _chart) { }
   virtual int snapshot() = 0;
   virtual void print() { };
   virtual int backup() { return 0; }
   virtual void restore() { }
   virtual void applyChanges(ObjectMonitorInterface *reference) { }
};

```

This set of methods should remind you ChartModeMonitorInterface from ChartModeMonitor.mqh. The only innovation is the applyChanges method, which copies the properties of one object to another.

Based on ObjectMonitorInterface, here is the description of the basic implementation of a property monitor for a pair of template types: a property value type (one of long, double, or string) and the enumeration type (one of ENUM_OBJECT_PROPERTY_-ish).

```
template<typename T,typename E>
class ObjectMonitorBase: public ObjectMonitorInterface
{
protected:
   MapArray<E,T> data;  // array of pairs [property, value], current state
   MapArray<E,T> store; // backup (filled on demand)
   MapArray<E,T> change;// committed changes between two states
   ...

```

The ObjectMonitorBase constructor has two parameters: the name of the object and an array of flags with identifiers of the properties to be observed in the specified object. A significant portion of this code is almost identical to ChartModeMonitor. In particular, as before, an array of flags is passed to the helper method detect, the main purpose of which is to identify those integer constants that are elements of the E enumeration, and weed out all the rest. The only addition that needs to be clarified is getting a property with the number of levels in an object via ObjectGetInteger(0, id, OBJPROP_LEVELS). This is necessary to support iteration of properties with multiple values due to the presence of levels (for example, Fibonacci). For objects without levels, we will get the quantity 0, and such a property will be the usual, scalar one.

```
public:
   ObjectMonitorBase(const string _id, const int &flags[]): ObjectMonitorInterface(_id)
   {
      const int levels = (int)ObjectGetInteger(0, id, OBJPROP_LEVELS);
      for(int i = 0; i < ArraySize(flags); ++i)
      {
         detect(flags[i], levels);
      }
   }
   ...

```

Of course, the detect method is somewhat different from what we saw in ChartModeMonitor. Recall that to begin with, it contains a fragment with a check if the v constant belongs to the E enumeration, using a call to the EnumToString function: if there is no such element in the enumeration, an error code will be raised. If the element exists, we add the value of the corresponding property to the data array.

```
   // ChartModeMonitor.mqh
   bool detect(const int v)
   {
      ResetLastError();
      conststrings = EnumToString((E)v); // resulting string is not important
      if(_LastError == 0)                // analyze the error code
      {
         data.put((E)v, get((E)v));
         return true;
      }
      return false;
   }

```

In the object monitor, we are forced to complicate this scheme, since some properties are multi-valued due to the modifier parameter in the ObjectGet and ObjectSet functions.

So we introduce a static array modifiables with a list of those properties that modifiers support (each property will be discussed in detail later). The bottom line is that for such multi-valued properties, you need to read them and store them in the data array not once, but several times.

```
// ObjectMonitor.mqh
   bool detect(const int v, const int levels)
   {
      // the following properties support multiple values
      static const int modifiables[] =
      {
         OBJPROP_TIME,        // anchor point by time
         OBJPROP_PRICE,       // anchor point by price
         OBJPROP_LEVELVALUE,  // level value
         OBJPROP_LEVELTEXT,   // inscription on the level line
         // NB: the following properties do not generate errors when exceeded
         // actual number of levels or files
         OBJPROP_LEVELCOLOR,  // level line color
         OBJPROP_LEVELSTYLE,  // level line style
         OBJPROP_LEVELWIDTH,  // width of the level line
         OBJPROP_BMPFILE,     // image files
      };
      ...

```

Here, we also use the trick with EnumToString to check the existence of a property with the v identifier. If successful, we check if it is in the list of modifiables and set the corresponding flag modifiable to true or false.

```
      bool result = false;
      ResetLastError();
 conststrings =EnumToString((E)v); // resulting string is not important
 if(_LastError ==0)// analyze the error code
      {
         bool modifiable = false;
         for(int i = 0; i < ArraySize(modifiables); ++i)
         {
            if(v == modifiables[i])
            {
               modifiable = true;
               break;
            }
         }
         ...

```

By default, any property is considered unambiguous and therefore the required number of readings through the ObjectGet function or entries via the ObjectSet function is equal to 1 (the k variable below).

```
         int k = 1;
         // for properties with modifiers, set the correct amount
         if(modifiable)
         {
            if(levels > 0) k = levels;
            else if(v == OBJPROP_TIME || v == OBJPROP_PRICE) k = MOD_MAX;
            else if(v == OBJPROP_BMPFILE) k = 2;
         }

```

If an object supports levels, we limit the potential number of reads/writes with the levels parameter (as we recall, it is obtained in the calling code from the OBJPROP_LEVELS property).

For the OBJPROP_BMPFILE property, as we will soon learn, only two states are allowed: on (button pressed, flag set) or off (button released, flag cleared), so k = 2.

Finally, object coordinates - OBJPROP_TIME and OBJPROP_PRICE - are convenient because they generate an error when trying to read/write a non-existent anchor point. Therefore we assign to k some obviously large value of MOD_MAX, and then we can interrupt the cycle of reading points at a non-zero value _LastError.

```
         // read property value - one or many
         for(int i = 0; i < k; ++i)
         {
            ResetLastError();
            T temp = get((E)v, i);
            // if there is no i-th modifier, we will get an error and break the loop
            if(_LastError != 0) break;
            data.put((E)MOD_COMBINE(v, i), temp);
            result = true;
         }
      }
      return result;
   }

```

Since one property can have several values, which are read in a loop up to k, we can no longer simply write data.put((E)v, get((E)v)). We need to somehow combine the property identifier v and its modification number i. Fortunately, the number of properties is also limited in an integer constant (typeint) no more than two lower bytes are occupied. So we can use bitwise operators to put i to the top byte. The MOD_COMBINE macro has been developed for this purpose.

```
#define MOD_COMBINE(V,I) (V | (I << 24))

```

Of course, reverse macros are provided to retrieve the property ID and revision number.

```
#define MOD_GET_NAME(V)  (V & 0xFFFFFF)
#define MOD_GET_INDEX(V) (V >> 24)

```

For example, here we can see how they are used in the snapshot method.

```
   virtual int snapshot() override
   {
      MapArray<E,T> temp;
      change.reset();
      
      // collect all required properties in temp
      for(int i = 0; i < data.getSize(); ++i)
      {
         const E e = (E)MOD_GET_NAME(data.getKey(i));
         const int m = MOD_GET_INDEX(data.getKey(i));
         temp.put((E)data.getKey(i), get(e, m));
      }
      
      int changes = 0;
      // compare previous and new state
      for(int i = 0; i < data.getSize(); ++i)
      {
         if(data[i] != temp[i])
         {
            // save the differences in the change array
            if(changes == 0) Print(id);
            const E e = (E)MOD_GET_NAME(data.getKey(i));
            const int m = MOD_GET_INDEX(data.getKey(i));
            Print(EnumToString(e), (m > 0 ? (string)m : ""), " ", data[i], " -> ", temp[i]);
            change.put(data.getKey(i), temp[i]);
            changes++;
         }
      }
      
      // save the new state as current
      data = temp;
      return changes;
   }

```

This method repeats all the logic of the method of the same name in ChartModeMonitor.mqh, however, to read properties everywhere, you must first extract the property name from the stored key using MOD_GET_NAME and the number using MOD_GET_INDEX.

A similar complication has to be done in the restore method.

```
   virtual void restore() override
   {
      data = store;
      for(int i = 0; i < data.getSize(); ++i)
      {
         const E e = (E)MOD_GET_NAME(data.getKey(i));
         const int m = MOD_GET_INDEX(data.getKey(i));
         set(e, data[i], m);
      }
   }

```

The most interesting innovation of ObjectMonitorBase is how it works with changes.

```
   MapArray<E,T> * const getChanges()
   {
      return &change;
   }
   
   virtual void applyChanges(ObjectMonitorInterface *intf) override
   {
      ObjectMonitorBase *reference = dynamic_cast<ObjectMonitorBase<T,E> *>(intf);
      if(reference)
      {
         MapArray<E,T> *event = reference.getChanges();
         if(event.getSize() > 0)
         {
            Print("Modifing ", id, " by ", event.getSize(), " changes");
            for(int i = 0; i < event.getSize(); ++i)
            {
               data.put(event.getKey(i), event[i]);
               const E e = (E)MOD_GET_NAME(event.getKey(i));
               const int m = MOD_GET_INDEX(event.getKey(i));
               Print(EnumToString(e), " ", m, " ", event[i]);
               set(e, event[i], m);
            }
         }
      }
   }

```

Passing to the applyChanges method states of the monitor of another object, we can adopt all the latest changes from it.

To support properties of all three basic types (long,double,string), we need to implement the ObjectMonitor class (analog of ChartModeMonitor from ChartModeMonitor.mqh).

```
class ObjectMonitor: public ObjectMonitorInterface
{
protected:
   AutoPtr<ObjectMonitorInterface> m[3];
   
   ObjectMonitorInterface *getBase(const int i)
   {
      return m[i][];
   }
   
public:
   ObjectMonitor(const string objid, const int &flags[]): ObjectMonitorInterface(objid)
   {
      m[0] = new ObjectMonitorBase<long,ENUM_OBJECT_PROPERTY_INTEGER>(objid, flags);
      m[1] = new ObjectMonitorBase<double,ENUM_OBJECT_PROPERTY_DOUBLE>(objid, flags);
      m[2] = new ObjectMonitorBase<string,ENUM_OBJECT_PROPERTY_STRING>(objid, flags);
   }
   ...

```

The previous code structure is also preserved here, and only methods have been added to support changes and names (charts, as we remember, do not have names).

```
   ...
   virtual string name() override
   {
      return m[0][].name();
   }
   
   virtual void name(const string objid) override
   {
      m[0][].name(objid);
      m[1][].name(objid);
      m[2][].name(objid);
   }
   
   virtual void applyChanges(ObjectMonitorInterface *intf) override
   {
      ObjectMonitor *monitor = dynamic_cast<ObjectMonitor *>(intf);
      if(monitor)
      {
         m[0][].applyChanges(monitor.getBase(0));
         m[1][].applyChanges(monitor.getBase(1));
         m[2][].applyChanges(monitor.getBase(2));
      }
   }

```

Based on the created object monitor, it is easy to implement several tricks that are not supported in the terminal. In particular, this is the creation of copies of objects and group editing of objects.

Script ObjectCopy

The ObjectCopy.mq5 script demonstrates how to copy selected objects. At the beginning of its OnStart function, we fill the flags array with consecutive integers that are candidates for elements of ENUM_OBJECT_PROPERTY_ enumerations of different types. The numbering of the enumeration elements has a pronounced grouping by purpose, and there are large gaps between the groups (apparently, a margin for future elements), so the formed array is quite large: 2048 elements.

```
#include <MQL5Book/ObjectMonitor.mqh>
   
#define PUSH(A,V) (A[ArrayResize(A, ArraySize(A) + 1) - 1] = V)
   
void OnStart()
{
   int flags[2048];
   // filling the array with consecutive integers, which will be
   // checked against the elements of enumerations of object properties,
   // invalid values will be discarded in the monitor's detect method
   for(int i = 0; i < ArraySize(flags); ++i)
   {
      flags[i] = i;
   }
   ...

```

Next, we collect into an array the names of objects that are currently selected on the chart. For this, we use the OBJPROP_SELECTED property.

```
   string selected[];
   const int n = ObjectsTotal(0);
   for(int i = 0; i < n; ++i)
   {
      const string name = ObjectName(0, i);
      if(ObjectGetInteger(0, name, OBJPROP_SELECTED))
      {
         PUSH(selected, name);
      }
   }
   ...

```

Finally, in the main loop over the selected elements, we read the properties of each object, form the name of its copy, and create an object under it with the same set of attributes.

```
   for(int i = 0; i < ArraySize(selected); ++i)
   {
      const string name = selected[i];
      
     // make a backup of the properties of the current object using the monitor
      ObjectMonitor object(name, flags);
      object.print();
      object.backup();
      // form a correct, appropriate name for the copy
      const string copy = GetFreeName(name);
      
      if(StringLen(copy) > 0)
      {
         Print("Copy name: ", copy);
         // create an object of the same type OBJPROP_TYPE
         ObjectCreate(0, copy,
            (ENUM_OBJECT)ObjectGetInteger(0, name, OBJPROP_TYPE),
            ObjectFind(0, name), 0, 0);
         // change the name of the object in the monitor to a new one
         object.name(copy);
         // restore all properties from the backup to a new object
         object.restore();
      }
      else
      {
         Print("Can't create copy name for: ", name);
      }
   }
}

```

It is important to note here that the OBJPROP_TYPE property is one of the few read-only properties, and therefore it is vital to create an object of the required type to begin with.

The helper function GetFreeName tries to append the string "/Copy #x" to the object name, where x is the copy number. Thus, by running the script several times, you can create the 2nd, 3rd, and so on copies.

```
string GetFreeName(const string name)
{
   const string suffix = "/Copy №";
   // check if there is a copy in the suffix name
   const int pos = StringFind(name, suffix);
   string prefix;
   int n;
   
   if(pos <= 0)
   {
      // if suffix is not found, assume copy number 1
      const string candidate = name + suffix + "1";
      // checking if the copy name is free, and if so, return it
      if(ObjectFind(0, candidate) < 0)
      {
         return candidate;
      }
      // otherwise, prepare for a loop with iteration of copy numbers
      prefix = name;
      n = 0;
   }
   else
   {
      // if the suffix is found, select the name without it
      prefix = StringSubstr(name, 0, pos);
      // and find the copy number in the string
      n = (int)StringToInteger(StringSubstr(name, pos + StringLen(suffix)));
   }
   
   Print("Found: ", prefix, " ", n);
   // loop trying to find a free copy number above n, but no more than 1000
   for(int i = n + 1; i < 1000; ++i)
   {
      const string candidate = prefix + suffix + (string)i;
      // check for the existence of an object with a name ending "Copy #i"
      if(ObjectFind(0, candidate) < 0)
      {
         return candidate; // return vacant copy name
      }
   }
   return NULL; // too many copies
}

```

The terminal remembers the last settings of a particular type of object, and if they are created one after the other, this is equivalent to copying. However, the settings usually change in the process of working with different charts, and if after a while there is a need to duplicate some "old" object, then the settings for it, as a rule, have to be done completely. This is especially expensive for object types with a large number of properties, for example, Fibonacci tools. In such cases, this script will come in handy.

Some of the pictures from this chapter, which contain objects of the same type, were created using this script.

ObjectGroupEdit indicator

The second example of using ObjectMonitor is the ObjectGroupEdit.mq5 indicator, which allows you to edit the properties of a group of selected objects at once.

Imagine that we have selected several objects on the chart (not necessarily of the same type), for which it is necessary to uniformly change one or another property. Next, we open the properties dialog of any of these objects, configure it, and by clicking OK these changes are applied to all selected objects. This is how our next MQL program works.

We needed an indicator as a type of program because it involves chart events. For this aspect of MQL5 programming, there will be a whole dedicated [chapter](/en/book/applications/events), but we will get to know some of the basics right now.

Since the indicator does not have charts, the #property directives contain zeros and the OnCalculate function is virtually empty.

```
#property indicator_chart_window
#property indicator_buffers 0
#property indicator_plots   0
   
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const int begin,
                const double &price[])
{
   return rates_total;
}

```

To automatically generate a complete set of all properties for an object, we will again use an array of 2048 elements with consecutive integer values. We will also provide an array for the names of the selected elements and an array of monitor objects of the ObjectMonitor class.

```
int consts[2048];
string selected[];
ObjectMonitor *objects[];

```

In the OnInit handler, we initialize the array of numbers and start the timer.

```
void OnInit()
{
   for(int i = 0; i < ArraySize(consts); ++i)
   {
      consts[i] = i;
   }
   
   EventSetTimer(1);
}

```

In the timer handler, we save the names of the selected objects in an array. If the selection list has changed, you need to reconfigure the monitor objects, for which the auxiliary TrackSelectedObjects function is called.

```
void OnTimer()
{
   string updates[];
   const int n = ObjectsTotal(0);
   for(int i = 0; i < n; ++i)
   {
      const string name = ObjectName(0, i);
      if(ObjectGetInteger(0, name, OBJPROP_SELECTED))
      {
         PUSH(updates, name);
      }
   }
   
   if(ArraySize(selected) != ArraySize(updates))
   {
      ArraySwap(selected, updates);
      Comment("Selected objects: ", ArraySize(selected));
      TrackSelectedObjects();
   }
}

```

The TrackSelectedObjects function itself is quite simple: delete the old monitors and create new ones. If you wish, you can make it more intelligent by maintaining the unchanged part of the selection.

```
void TrackSelectedObjects()
{
   for(int j = 0; j < ArraySize(objects); ++j)
   {
      delete objects[j];
   }
   
   ArrayResize(objects, 0);
   
   for(int i = 0; i < ArraySize(selected); ++i)
   {
      const string name = selected[i];
      PUSH(objects, new ObjectMonitor(name, consts));
   }
}

```

Recall that when creating a monitor object, it immediately takes a "cast" of all the properties of the corresponding graphical object.

Now we finally get to the part where events come into play. As was already mentioned in the [overview of event functions](/en/book/applications/runtime/runtime_events_overview), the handler is responsible for the OnChartEvent events on the chart. In this example, we are interested in a specific CHARTEVENT_OBJECT_CHANGE event: it occurs when the user changes any attributes in the object's properties dialog. The name of the modified object is passed in the sparam parameter.

If this name matches one of the monitored objects, we ask the monitor to make a new snapshot of its properties, that is, we call objects[i].snapshot().

```
void OnChartEvent(const int id,
   const long &lparam, const double &dparam, const string &sparam)
{
   if(id == CHARTEVENT_OBJECT_CHANGE)
   {
      Print("Object changed: ", sparam);
      for(int i = 0; i < ArraySize(selected); ++i)
      {
         if(sparam == selected[i])
         {
            const int changes = objects[i].snapshot();
            if(changes > 0)
            {
               for(int j = 0; j < ArraySize(objects); ++j)
               {
                  if(j != i)
                  {
                     objects[j].applyChanges(objects[i]);
                  }
               }
            }
            ChartRedraw();
            break;
         }
      }
   }
}

```

If the changes are confirmed (and it is unlikely otherwise), their number in the changes variable will be greater than 0. Then a loop is started over all the selected objects, and the detected changes are applied to each of them, except for the original one.

Since we can potentially change many objects, we call the chart redraw request with ChartRedraw.

In the OnDeinit handler, we remove all monitors.

```
void OnDeinit(const int)
{
   for(int j = 0; j < ArraySize(objects); ++j)
   {
      delete objects[j];
   }
   Comment("");
}

```

That's all: the new tool is ready.

This indicator allowed you to customize the general appearance of several groups of label objects in the section on [Defining the object anchor point](/en/book/applications/objects/objects_anchor).

By the way, according to a similar principle with the help of ObjectMonitor you can make another popular tool that is not available in the terminal: to undo edits to object properties, as the restore method is ready now.
