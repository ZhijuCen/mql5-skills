# Overview of functions for getting account properties

The full set of account properties is logically divided into three groups depending on their type. String properties are summarized in the ENUM_ACCOUNT_INFO_STRING enumeration and are queried by the AccountInfoString function. Real-type properties are combined in the ENUM_ACCOUNT_INFO_DOUBLE enumeration, and the function that works for them is AccountInfoDouble. The ENUM_ACCOUNT_INFO_INTEGER enumeration used in the AccountInfoInteger function contains identifiers of integer and boolean properties (flags), as well as several applied ENUM_ACCOUNT_INFO enumerations.

double AccountInfoDouble(ENUM_ACCOUNT_INFO_DOUBLE property)

long AccountInfoInteger(ENUM_ACCOUNT_INFO_INTEGER property)

string AccountInfoString(ENUM_ACCOUNT_INFO_STRING property)

We have created the AccountMonitor class (AccountMonitor.mqh) to simplify the reading of properties. By overloading get methods, the class provides the automatic call of the required API function depending on the element of a specific enumeration passed in the parameter.

```
class AccountMonitor
{
public:
   long get(const ENUM_ACCOUNT_INFO_INTEGER property) const
   {
      return AccountInfoInteger(property);
   }
   
   double get(const ENUM_ACCOUNT_INFO_DOUBLE property) const
   {
      return AccountInfoDouble(property);
   }
   
   string get(const ENUM_ACCOUNT_INFO_STRING property) const
   {
      return AccountInfoString(property);
   }
   
   long get(const int property, const long) const
   {
      return AccountInfoInteger((ENUM_ACCOUNT_INFO_INTEGER)property);
   }
   
   double get(const int property, const double) const
   {
      return AccountInfoDouble((ENUM_ACCOUNT_INFO_DOUBLE)property);
   }
   
   string get(const int property, const string) const
   {
      return AccountInfoString((ENUM_ACCOUNT_INFO_STRING)property);
   }
   ...

```

In addition, it has several overloads of the stringify method, which form a user-friendly string representation of property values (in particular, it is useful for applied enumerations, which would otherwise be displayed as uninformative numbers). The features of each property will be discussed in the following sections.

```
   static string boolean(const long v)
   {
      return v ? "true" : "false";
   }
   
   template<typename E>
   static string enumstr(const long v)
   {
      return EnumToString((E)v);
   }
   
   // "decode" properties according to subtype inside integer values
   static string stringify(const long v, const ENUM_ACCOUNT_INFO_INTEGER property)
   {
      switch(property)
      {
         case ACCOUNT_TRADE_ALLOWED:
         case ACCOUNT_TRADE_EXPERT:
         case ACCOUNT_FIFO_CLOSE:
            return boolean(v);
         case ACCOUNT_TRADE_MODE:
            return enumstr<ENUM_ACCOUNT_TRADE_MODE>(v);
         case ACCOUNT_MARGIN_MODE:
            return enumstr<ENUM_ACCOUNT_MARGIN_MODE>(v);
         case ACCOUNT_MARGIN_SO_MODE:
            return enumstr<ENUM_ACCOUNT_STOPOUT_MODE>(v);
      }
      
      return (string)v;
   }
   
   string stringify(const ENUM_ACCOUNT_INFO_INTEGER property) const
   {
      return stringify(AccountInfoInteger(property), property);
   }
   
   string stringify(const ENUM_ACCOUNT_INFO_DOUBLE property, const string format = NULL) const
   {
      if(format == NULL) return DoubleToString(AccountInfoDouble(property),
         (int)get(ACCOUNT_CURRENCY_DIGITS));
      return StringFormat(format, AccountInfoDouble(property));
   }
   
   string stringify(const ENUM_ACCOUNT_INFO_STRING property) const
   {
      return AccountInfoString(property);
   }
   ...

```

Finally, there is a template method list2log that allows getting comprehensive information about the account.

```
   // list of names and values of all properties of enum type E
   template<typename E>
   void list2log()
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
};

```

We'll test the new class in action in the next section.
