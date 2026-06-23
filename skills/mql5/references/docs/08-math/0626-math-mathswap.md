# MathSwap

Change the order of bytes in the [ushort](/en/docs/basis/types/integer/integertypes) type value.

```
ushort  MathSwap(
   ushort  value      // value
   );

```

Parameters

value

[in]  Value for changing the order of bytes.

Return Value

ushort value with the reverse byte order.

# MathSwap

Change the order of bytes in the [uint](/en/docs/basis/types/integer/integertypes) type value.

```
uint  MathSwap(
   uint   value      // value
   );

```

Parameters

value

[in]  Value for changing the order of bytes.

Return Value

uint value with the reverse byte order.

# MathSwap

Change the order of bytes in the [ulong](/en/docs/basis/types/integer/integertypes) type value.

```
ulong  MathSwap(
   ulong  value      // value
   );

```

Parameters

value

[in]  Value for changing the order of bytes.

Return Value

ulong value with the reverse byte order.

Example:

```
#property script_show_inputs
 
input ulong  InpLongValue  =  1;    // Enter any ulong value here
input uint   InpIntValue   =  2;    // Enter any uint value here
input ushort InpShortValue =  3;    // Enter any ushort value here
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
 
//--- print the values entered and converted by MathSwap() in decimal and binary representation in the journal
   Print(ValueDescription(InpLongValue));
   Print(ValueDescription(InpIntValue));
   Print(ValueDescription(InpShortValue));
   /*
   result:
   ulong value: 1
   ulong value: 72057594037927936 using MathSwap()
   binary ulong value: 0000000000000000000000000000000000000000000000000000000000000001
   binary ulong value: 0000000100000000000000000000000000000000000000000000000000000000 using MathSwap()
   
   uint value: 2
   uint value: 33554432 using MathSwap()
   binary uint value: 00000000000000000000000000000010
   binary uint value: 00000010000000000000000000000000 using MathSwap()
   
   ushort value: 3
   ushort value: 768 using MathSwap()
   binary ushort value: 0000000000000011
   binary ushort value: 0000001100000000 using MathSwap()
   */
  }
//+------------------------------------------------------------------+
//| Return the text describing the variable values                   |
//+------------------------------------------------------------------+
template <typename T>
string ValueDescription(T x)
  {
   int    num_bits   = sizeof(T)*8;
   string type_name  = typename(T);
   string bin_x      = NumberToBinaryString(x);
   string bin_swap_x = NumberToBinaryString(MathSwap(x));
   return(StringFormat("%s value: %lld\n%s value: %lld using MathSwap()\nbinary %s value: %0*s\nbinary %s value: %0*s using MathSwap()\n", 
                       type_name, x, type_name, MathSwap(x), type_name, num_bits, bin_x, type_name, num_bits, bin_swap_x));
  }
//+------------------------------------------------------------------+
//| Return the binary representation of a number as a string         |
//+------------------------------------------------------------------+
template <typename T>
string NumberToBinaryString(T x)
  {
   string res  = "";
   int    i    = -1;
   uchar  size = sizeof(T)*8-1;
   ulong  mask = (ulong)1<<size;
   while(!((x<<++i)& mask));
   for(; i <=size; i++)
      res += !((x<<i)& mask) ? "0" : "1";
   return res;
  }

```

See also

[Network functions](/en/docs/network), [SocketRead](/en/docs/network/socketread), [SocketSend](/en/docs/network/socketsend), [SocketTlsRead](/en/docs/network/sockettlsread), [SocketTlsReadAvailable](/en/docs/network/sockettlsreadavailable), [SocketTlsSend](/en/docs/network/sockettlssend)
