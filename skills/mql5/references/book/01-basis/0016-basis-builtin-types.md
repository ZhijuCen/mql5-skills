# Built-In Data Types

The data type is a fundamental concept we comfortably use in our everyday life without even thinking of its existence. It is implied based on the meaning of the information we exchange and on the processing procedures admissible for it. For example, controlling our household assets, we add and deduct numbers representing our revenues and expenses. Here, the 'number' describes a type, for which we realize fully its possible values and arithmetic operations on them. In the trading context, there is a similar value, the current account balance, in MetaTrader 5; therefore, MQL5 provides a mechanism to create and manipulate numbers.

Unlike numbers, text information, such as the name of a trading instrument, conforms to other rules. Here we can build a word of letters or a sentence of words, but it is impossible to compute the progressive total or arithmetic mean of several lines. Thus, 'line' or 'string' is another data type, not a numeric one.

Along with the purpose and a typical set of operations that are meaningful for each type, there is another important thing that differs types from each other. It's their size. For instance, the week number cannot exceed 52 within a year, while the number of seconds that have elapsed from the beginning of the year represents an astronomical shape. Therefore, to efficiently store and process such different values in the computer memory, differently sized segments can be singled out. This leads us to understand that, in fact, the generalizing concept of a 'number' may hide different types.

MQL5 allows the used of some number types differing both in the sizes of memory cells allocated for them and in some additional features. In particular, some numbers may take negative values, such as floating profit in pips, while the other ones may not, such as account numbers. Moreover, some values cannot have a fractional part and therefore, it is more cost-efficient to represent them with a stricter type of 'integers', as opposed to those of random 'numbers with a decimal point'. For instance, an account balance or the price of a trading instrument generally have values with a decimal point. At the same time, the number of orders in history or, again, the account number is always an integer.

MQL5 supports a set of universal types similar to those available in the vast majority of programming languages. The set includes integer types (different sizes), two types of real numbers (with a decimal point) of different precision, strings, and single characters, as well as the logical type that only has two possible values: true and false. Moreover, MQL5 provides its own, specific types operating with time and color.

For the sake of completeness, let's note that MQL5 allows expanding the set of types, declaring applied types in the code, i.e., structures, classes, and other entities typical of OOP; but we are going to consider them later.

Since the size of the cell where the value is stored is an important type attribute, let's touch on memory methodology.

The smallest unit of computer memory is a byte. In other words, a byte is the smallest size of a cell that a program can allocate for a separate value. A byte consists of 8 smaller 'particles', bits, each being able to be in two states: Enabled (1) or disabled (0). All modern computers use such bits at the lower level because such a binary representation of information is convenient to be embodied in hardware(in random-access memory, in processors, or while transferring the data by network cables or via WiFi).

Processing the values of different types is ensured due to the different interpretations of the bit states in memory cells. The compiler deals with this. Programmers usually do not go as low as bits; however, the language provides tools for that (see [Bitwise operations](/en/book/basis/expressions/operators_bitwise)).

There are special reserved words in MQL5 to describe data types. We have already known some of them, such as void, int, and string, from Part 1. A complete list of types is given below, each with a quick reference and size in bytes.

By their purpose, they can be conditionally divided into numeric and character-coded data (marked in the relevant columns), as well as other, specialized types, such as strings, logical (or boolean) types, date/time, and color. Type void stands apart and indicates there is no value at all. In addition to scalar types, MQL5 provides object types for operations with complex numbers, matrices, and vectors: complex, vector, and matrix. These types are used to solve various problems in linear algebra, mathematical modeling, machine learning, and other areas. We will study them in detail in Part 4 of the book.

| Type | Size 
 (bytes) | Number | Character | Note |
| --- | --- | --- | --- | --- |
| char | 1 | + | + | Single-byte character or a signed integer |
| uchar | 1 | + | + | Single-byte character or an unsigned integer |
| short | 2 | + | + | Two-byte character or a signed integer |
| ushort | 2 | + | + | Two-byte character or an unsigned integer |
| int | 4 | + |  | Signed integer |
| uint | 4 | + |  | Unsigned integer |
| long | 8 | + |  | Signed integer |
| ulong | 8 | + |  | Unsigned integer |
| float | 4 | + |  | Signed floating-point number |
| double | 8 | + |  | Signed floating-point number |
| enum | 4 | (int) |  | Enumeration |
| datetime | 8 | (ulong) |  | Date and time |
| color | 4 | (uint) |  | Color |
| bool | 1 | (uchar) |  | Logical |
| string | 10+ 
 variable |  |  | String |
| void | 0 |  |  | Void |
| complex | 16 | + |  | Structure with two double-type fields |
| vector | vector length x type size | + |  | One-dimensional array of real or complex type |
| matrix | rows x columns x type size | + |  | Two-dimensional array of real or complex type |

Depending on its size, different value ranges may be stored in the numeric type. Along with the above, the range may considerably vary for the integers and floating-point numbers of the same size, because different internal representations are used for them. All these cobwebs will be considered in the sections dealing with specific types.

A programmer is free to choose a numeric type based on the anticipated values, efficiency considerations, or for reasons of economy. Particularly, the smaller type size allows fitting more values of this type in memory, while integers are processed faster than floating-point numbers.

Please note that numeric and character-coded types are partly crossed. This happens because a character is stored in memory as an integer, i.e., a code in the relevant table of characters: ANSI for single-byte chars or Unicode for two-byte ones. ANSI is a standard named after an institute (American National Standards Institute), while Unicode, you guessed it, means Universal Code (Character Set). Unicode characters are used in MQL5 to make strings (type string). Single-byte characters are usually required in integrating the programs with external data sources, such as those from the Internet.

As mentioned above, numeric types can be divided into integers and floating-point numbers. Let's consider them in more detail.
