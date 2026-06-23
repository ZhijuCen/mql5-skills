# Initialization and measurement of strings

As we know from the [String type](/en/book/basis/builtin_types/strings) section, it is enough to describe in the code a variable of type string, and it will be ready to go.

For any variable of string type 12 bytes are allocated for the service structure which is the internal representation of the string. The structure contains the memory address (pointer) where the text is stored, along with some other meta-information. The text itself also requires sufficient memory, but this buffer is allocated with some less obvious optimizations.

In particular, we can describe a string along with explicit initialization, including an empty literal:

```
string s = ""; // pointer to the literal containing '\0'

```

In that case, the pointer will be set directly to the literal, and no memory is allocated for the buffer (even if the literal is long). Obviously, static memory has already been allocated for the literal, and it can be used directly. The memory for the buffer will be allocated only if any instruction in the program changes the contents of the line. For example (note the addition operation '+' is allowed for strings):

```
int n = 1;
s += (string)n;    // pointer to memory containing "1"'\0'[plus reserve]

```

From this point on, the string actually contains the text "1" and, strictly speaking, requires memory for two characters: the digit "1" and the implicit terminal zero '\0' (terminator of the string). However, the system will allocate a larger buffer, with some space reserved.

When we declare a variable without an initial value, it is still implicitly initialized by the compiler, though in this case with a special NULL value:

```
string z; // memory for the pointer is not allocated, pointer = NULL

```

Such a string requires only 12 bytes per structure, and the pointer doesn't point anywhere: that's what NULL stands for.

In future versions of the MQL5 compiler, this behavior may change, and a small area of memory will always be initially allocated for an empty string, providing some reserved space.

In addition to these internal features, variables of the string type are no different from variables of other types. However, due to the fact that strings can be variable in length and, more importantly, they can change their length during the algorithm, this can adversely affect the efficiency of memory allocation and performance.

For example, if at some point the program needs to add a new word to a string, it may turn out that there is not enough memory allocated for the string. Then the MQL program execution environment, imperceptible to the user, will find a new free memory block of increased size and copy the old value there along with the added word. After that, the old address is replaced by a new one in the line's service structure.

If there are many such operations, slowdown due to copying can become noticeable, and in addition, program memory is subject to fragmentation: old small memory areas released after copying form voids that are not suitable in size for large strings, and therefore lead to waste of memory. Of course, the terminal is able to control such situations and reorganize the memory, but this also comes at a cost.

The most effective way to solve this problem is to explicitly indicate in advance the size of the buffer for the string and initialize it using the built-in MQL5 API functions, which we will consider later in this section.

The basis for this optimization is just that the size of the allocated memory may exceed the current (and, potentially, the future) length of the string, which is determined by the first null character in the text. Thus, we can allocate a buffer for 100 characters, but from the start put '\0' at the very beginning, which will give a zero-length string ("").

Naturally, it is assumed that in such cases the programmer can roughly calculate in advance the expected length of the string or its growth rate.

Since strings in MQL5 are based on double-byte characters (which ensures Unicode support), the size of the string and buffer in characters should be multiplied by 2 to get the amount of occupied and allocated memory in bytes.

A general example of using all functions (StringInit.mq5) will be given at the end of the section.

bool StringInit(string &variable, int capacity = 0, ushort character = 0)

The StringInit function is used to initialize (allocate and fill memory) and deinitialize (free memory) strings. The variable to be processed is passed in the first parameter.

If the capacity parameter is greater than 0, then a buffer (memory area) of the specified size is allocated for the string and is filled with the symbol character. If the character is 0, then the length of the string will be zero, because the first character is terminal.

If the capacity parameter is 0, then previously allocated memory is freed. The state of the variable becomes identical to how it was if just declared without initialization (the pointer to the buffer is NULL). More simply, the same can be done by setting the string variable to NULL.

The function returns a success indicator (true) or errors (false).

bool StringReserve(string &variable, uint capacity)

The StringReserve function increases or decreases the buffer size of the string variable, at least up to the number of characters specified in the capacity parameter. If the capacity value is less than the current string length, the function does nothing. In fact, the buffer size may be larger than requested: the environment does this for reasons of efficiency in future manipulations with the string. Thus, if the function is called with a reduced value for the buffer, it can ignore the request and still return true ("no errors").

The current buffer size can be obtained using the function StringBufferLen (see below).

On success, the function returns true, otherwise – false.

Unlike StringInit the StringReserve function does not change the contents of the string and does not fill it with characters.

bool StringFill(string &variable, ushort character)

The StringFill function fills the specified variable string with the character character for its entire current length (up to the first zero). If a buffer is allocated for a string, the modification is done in-place, without intermediate newline and copy operations.

The function returns a success indicator (true) or errors (false).

int StringBufferLen(const string &variable)

The function returns the size of the buffer allocated for the variable string.

Note that for a literal-initialized string, no buffer is initially allocated because the pointer points to the literal. Therefore, the function will return 0 even though the length of the StringLen string (see below) may be more.

The value -1 means that the line belongs to the client terminal and cannot be changed.

bool StringSetLength(string &variable, uint length)

The function sets the specified length in characters length for the variable string. The value of the length must not be greater than the current length of the string. In other words, the function only allows you to shorten the string, but not lengthen it. The length of the string is increased automatically when the [StringAdd](/en/book/common/strings/strings_concatenation) function is called, or the addition operation '+' is performed.

The equivalent of the function StringSetLength is the call StringSetCharacter(variable, length, 0) (see section [Working with symbols and code pages](/en/book/common/strings/strings_codepages)).

If a buffer has already been allocated for the string before the function call, the function does not change it. If the string did not have a buffer (it was pointing to a literal), decreasing the length results in allocating a new buffer and copying the shortened string into it.

The function returns true or false in case of success or failure, respectively.

int StringLen(const string text)

The function returns the number of characters in the string text. Terminal zero is not taken into account.

Please note that the parameter is passed by value, so you can calculate the length of strings not only in variables but also for any other intermediate values: calculation results or literals.

The StringInit.mq5 script has been created to demonstrate the above functions. It uses a special version of the PRT macro, PRTE, which parses the result of an expression into true or false, and in the case of the latter additionally outputs an error code:

```
#define PRTE(A) Print(#A, "=", (A) ? "true" : "false:" + (string)GetLastError())

```

For debug output to the log of a string and its current metrics (line length and buffer size), the StrOut function is implemented:

```
void StrOut(const string &s)
{
   Print("'", s, "' [", StringLen(s), "] ", StringBufferLen(s));
}

```

It uses the built-in StringLen and StringBufferLen functions.

The test script performs a series of actions on a string in OnStart:

```
void OnStart()
{
   string s = "message";
   StrOut(s);
   PRTE(StringReserve(s, 100)); // ok, but we get a buffer larger than requested: 260
   StrOut(s);
   PRTE(StringReserve(s, 500)); // ok, buffer is increased to 500
   StrOut(s);
   PRTE(StringSetLength(s, 4)); // ok: string is shortened
   StrOut(s);
   s += "age";
   PRTE(StringReserve(s, 100)); // ok: buffer remains at 500
   StrOut(s);
   PRTE(StringSetLength(s, 8)); // no: string lengthening is not supported
   StrOut(s);                   //     via StringSetLength
   PRTE(StringInit(s, 8, '$')); // ok: line increased by padding
   StrOut(s);                   //     buffer remains the same
   PRTE(StringFill(s, 0));      // ok: string collapsed to empty because
   StrOut(s);                   //     was filled with 0s, the buffer is the same
   PRTE(StringInit(s, 0));      // ok: line is zeroed, including buffer
                                // we could just write s = NULL;
   StrOut(s);
}

```

The script will log the following messages:

```
'message' [7] 0
StringReserve(s,100)=true
'message' [7] 260
StringReserve(s,500)=true
'message' [7] 500
StringSetLength(s,4)=true
'mess' [4] 500
StringReserve(s,10)=true
'message' [7] 500
StringSetLength(s,8)=false:5035
'message' [7] 500
StringInit(s,8,'$')=true
'$$$$$$$$' [8] 500
StringFill(s,0)=true
'' [0] 500
StringInit(s,0)=true
'' [0] 0

```

Please note that the call StringSetLength with increased string length ended with error 5035 (ERR_STRING_SMALL_LEN).
