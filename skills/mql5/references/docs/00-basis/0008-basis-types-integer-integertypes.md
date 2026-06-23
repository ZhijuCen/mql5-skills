# Char, Short, Int and Long Types

## char  #

The char type takes 1 byte of memory (8 bits) and allows expressing in the binary notation 2^8=256 values. The char type can contain both positive and negative values. The range of values is from -128 to 127.

## uchar  #

The uchar integer type also occupies 1 byte of memory, as well as the char type, but unlike it uchar is intended only for positive values. The minimum value is zero, the maximum value is 255. The first letter u in the name of the uchar type is the abbreviation for unsigned.

## short  #

The size of the short type is 2 bytes (16 bits) and, accordingly, it allows expressing the range of values equal to 2 to the power 16: 2^16 = 65 536.Since the short type is a signed one, and contains both positive and negative values, the range of values is between -32 768 and 32 767.

## ushort  #

The unsigned short type is the type ushort, which also has a size of 2 bytes. The minimum value is 0, the maximum value is 65 535.

## int  #

The size of the int type is 4 bytes (32 bits). The minimal value is -2 147 483 648, the maximal one is 2 147 483 647.

## uint  #

The unsigned integer type is uint. It takes 4 bytes of memory and allows expressing integers from 0 to 4 294 967 295.

## long  #

The size of the long type is 8 bytes (64 bits). The minimum value is -9 223 372 036 854 775 808, the maximum value is 9 223 372 036 854 775 807.

## ulong  #

The ulong type also occupies 8 bytes and can store values from 0 to 18 446 744 073 709 551 615.

Examples:

```
char  ch=12;
short sh=-5000;
int   in=2445777;

```

Since the unsigned integer types are not designed for storing negative values, the attempt to set a negative value can lead to unexpected consequences. Such a simple script will lead to an infinite loop:

```
//--- Infinite loop
void OnStart()
  {
   uchar  u_ch;
 
   for(char ch=-128;ch<128;ch++)
     {
      u_ch=ch;
      Print("ch = ",ch," u_ch = ",u_ch);
     }
  }

```

The correct variant is:

```
//--- Correct variant
void OnStart()
  {
   uchar  u_ch;
 
   for(char ch=-128;ch<=127;ch++)
     {
      u_ch=ch;
      Print("ch = ",ch," u_ch = ",u_ch);
      if(ch==127) break;
     }
  }

```

Result:

```
   ch= -128  u_ch= 128
   ch= -127  u_ch= 129
   ch= -126  u_ch= 130
   ch= -125  u_ch= 131
   ch= -124  u_ch= 132
   ch= -123  u_ch= 133
   ch= -122  u_ch= 134
   ch= -121  u_ch= 135
   ch= -120  u_ch= 136
   ch= -119  u_ch= 137
   ch= -118  u_ch= 138
   ch= -117  u_ch= 139
   ch= -116  u_ch= 140
   ch= -115  u_ch= 141
   ch= -114  u_ch= 142
   ch= -113  u_ch= 143
   ch= -112  u_ch= 144
   ch= -111  u_ch= 145
    ... 

```

Examples:

```
//--- Negative values can not be stored in unsigned types
uchar  u_ch=-120;
ushort u_sh=-5000;
uint   u_in=-401280;

```

Hexadecimal: numbers 0-9, the letters a-f or A-F for the values of 10-15; start with 0x or 0X.

Examples:

```
0x0A, 0x12, 0X12, 0x2f, 0xA3, 0Xa3, 0X7C7

```

For integer variables, the values can be set in binary form using B prefix. For example, you can encode the working hours of a trading session into int type variable and use information about them according to the required algorithm:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- set 1 for working hours and 0 for nonworking ones
   int AsianSession   =B'111111111'; // Asian session from 0:00 to 9:00
   int EuropeanSession=B'111111111000000000'; // European session 9:00 - 18:00
   int AmericanSession =B'111111110000000000000011'; // American session 16:00 - 02:00
//--- derive numerical values of the sessions
   PrintFormat("Asian session hours as value =%d",AsianSession);
   PrintFormat("European session hours as value is %d",EuropeanSession);
   PrintFormat("American session hours as value is %d",AmericanSession);
//--- and now let's display string representations of the sessions' working hours
   Print("Asian session ",GetHoursForSession(AsianSession));
   Print("European session ",GetHoursForSession(EuropeanSession));
   Print("American session ",GetHoursForSession(AmericanSession));   
//---
  }
//+------------------------------------------------------------------+
//| return the session's working hours as a string                   |
//+------------------------------------------------------------------+
string GetHoursForSession(int session)
  {
//--- in order to check, use AND bit operations and left shift by 1 bit <<=1
//--- start checking from the lowest bit
   int bit=1;
   string out="working hours: ";
//--- check all 24 bits starting from the zero and up to 23 inclusively  
   for(int i=0;i<24;i++)
     {
      //--- receive bit state in number
      bool workinghour=(session&bit)==bit;
      //--- add the hour's number to the message
      if(workinghour )out=out+StringFormat("%d ",i); 
      //--- shift by one bit to the left to check the value of the next one
      bit<<=1;
     }
//--- result string
   return out;
  }

```

See also

[Typecasting](/en/docs/basis/types/casting)
