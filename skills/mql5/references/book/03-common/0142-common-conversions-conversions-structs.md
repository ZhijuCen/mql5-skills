# Structures

When integrating MQL programs with external systems, in particular, when sending or receiving data via the Internet, it becomes necessary to convert data structures into byte arrays. For these purposes, the MQL5 API provides two functions: StructToCharArray and CharArrayToStruct.

In both cases, it is assumed that a structure contains only simple [built-in types](/en/book/basis/builtin_types), that is, all built-in types except [lines](/en/book/basis/builtin_types/strings) and dynamic [arrays](/en/book/basis/arrays/arrays_overview). A structure can also contain other simple structures. Class objects and pointers are not allowed. Such structures are also called POD (Plain Old Data).

bool StructToCharArray(const void &object, uchar &array[], uint pos = 0)

The StructToCharArray function copies the POD structure object into the array array of type uchar. Optionally, using the parameter pos you can specify the position in the array, starting from which the bytes will be placed. By default, copying goes to the beginning of the array, and the dynamic array will be automatically increased in size if its current size is not enough for the entire structure.

The function returns a success indicator (true) or errors (false).

Let's check its performance with the script ConversionStruct.mq5. Let's create a new structure type DateTimeMsc, which includes the standard structure MqlDateTime (field mdt) and an additional field msc of type int to store milliseconds.

```
struct DateTimeMsc
{
   MqlDateTime mdt;
   int msc;
   DateTimeMsc(MqlDateTime &init, int m = 0) : msc(m)
   {
      mdt = init;
   }
};

```

Inside the OnStart function, let's convert a test value datetime to our structure, and then to the byte array.

```
MqlDateTime TimeToStructInplace(datetime dt)
{
   static MqlDateTime m;
   if(!TimeToStruct(dt, m))
   {
      // the error code, _LastError, can be displayed
      // but here we just return zero time
      static MqlDateTime z = {};
      return z;
   }
   return m;
}
 
#define MDT(T) TimeToStructInplace(T)
 
void OnStart()
{
   DateTimeMsc test(MDT(D'2021.01.01 10:10:15'), 123);
   uchar a[];
   Print(StructToCharArray(test, a));
   Print(ArraySize(a));
   ArrayPrint(a);
}

```

We will get the following result in the log (the array is reformatted with additional line breaks to emphasize the correspondence of bytes to each of the fields):

```
   true
   36
   229   7   0   0
     1   0   0   0
     1   0   0   0
    10   0   0   0
    10   0   0   0
    15   0   0   0
     5   0   0   0
     0   0   0   0
   123   0   0   0

```

bool CharArrayToStruct(void &object, const uchar &array[], uint pos = 0)

The CharArrayToStruct function copies the array array of the uchar type to the POD structure object. Using the pos parameter, you can specify the position in the array from which to start reading bytes.

The function returns a success indicator (true) or errors (false).

Continuing the same example (ConversionStruct.mq5), we can restore the original date and time from the byte array.

```
void OnStart()
{
   ...
   DateTimeMsc receiver;
   Print(CharArrayToStruct(receiver, a));                 // true
   Print(StructToTime(receiver.mdt), "'", receiver.msc);  // 2021.01.01 10:10:15'123
}

```
