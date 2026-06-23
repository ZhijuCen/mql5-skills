# Endianness control in integers

Various information systems, at the hardware level, use different byte orders when representing numbers in memory. Therefore, when integrating MQL programs with the "outside world", in particular, when implementing network communication protocols or reading/writing files of common formats, it may be necessary to change the byte order.

Windows computers apply little-endian (starting with the least significant byte), i.e., the lowest byte comes first in the memory cell allocated for the variable, then follows the byte with higher bits, and so on. The alternative big-endian (starting with the highest digit, the most significant byte) is widely used on the Internet. In this case, the first byte in the memory cell is the byte with the high bits, and the last byte is the low bit. It is this order that is similar to how we write numbers "from left to right" in ordinary life. For example, the value 1234 starts with 1 and stands for thousands, followed by a 2 for hundreds, a 3 for tens, and the last 4 is just four (low order).

Let's see the default byte order in MQL5. To do this, we will use the script MathSwap.mq5.

It describes a concatenation pattern that allows you to convert an integer to an array of bytes:

```
template<typename T>
union ByteOverlay
{
   T value;
   uchar bytes[sizeof(T)];
   ByteOverlay(const T v) : value(v) { }
   void operator=(const T v) { value = v; }
};

```

This code allows you to visually divide the number into bytes and enumerate them with indices from the array.

In OnStart, we describe the uint variable with the value 0x12345678 (note that the digits are hexadecimal; in such a notation they exactly correspond to byte boundaries: every 2 digits is a separate byte). Let's convert the number to an array and output it to the log.

```
void OnStart()
{
   const uint ui = 0x12345678;
   ByteOverlay<uint> bo(ui);
   ArrayPrint(bo.bytes); // 120  86  52  18 <==> 0x78 0x56 0x34 0x12
   ...

```

The ArrayPrint function can't print numbers in hexadecimal, so we see their decimal representation, but it's easy to convert them to base 16 and make sure they match the original bytes. Visually, they go in reverse order: i.e., under the 0th index in the array is 0x78, and then 0x56, 0x34 and 0x12. Obviously, this order starts with the least-significant byte (indeed, we are in the Windows environment).

Now let's get familiar with the function MathSwap, which MQL5 provides to change the byte order.

integer MathSwap(integer value)

The function returns an integer in which the byte order of the passed argument is reversed. The function takes parameters of type ushort/uint/ulong (i.e. 2, 4, 8 bytes in size).

Let's try the function in action:

```
   const uint ui = 0x12345678;
   PrintFormat("%I32X -> %I32X", ui, MathSwap(ui));
   const ulong ul = 0x0123456789ABCDEF;
   PrintFormat("%I64X -> %I64X", ul, MathSwap(ul));

```

Here is the result:

```
   12345678 -> 78563412
   123456789ABCDEF -> EFCDAB8967452301

```

Let's try to log an array of bytes after converting the value 0x12345678 with MathSwap:

```
   bo = MathSwap(ui);    // put the result of MathSwap into ByteOverlay
   ArrayPrint(bo.bytes); //  18  52  86 120 <==> 0x12 0x34 0x56 0x78

```

In a byte with index 0, where it used to be 0x78, there is now 0x12, and in elements with other numbers, the values are also exchanged.
