# Writing and reading files in simplified mode

Among the MQL5 file functions that are intended for writing and reading data, there is a division into 2 unequal groups. The first of these includes two functions: FileSave and FileLoad, which allow you to write or read data in binary mode in a single function call. On the one hand, this approach has an undeniable advantage, the simplicity, but on the other hand, it has some limitations (more on those below). In the second large group, all file functions are used differently: it is required to call several of them sequentially in order to perform a logically complete read or write operation. This seems more complex, but it provides flexibility and control over the process. The functions of the second group operate with special integers — file descriptors, which should be obtained using the FileOpen function (see the [next section](/en/book/common/files/files_open_close)).

Let's view the formal description of these two functions, and then consider their example (FileSaveLoad.mq5).

bool FileSave(const string filename, const void &data[], const int flag = 0)

The function writes all elements of the passed data array to a binary file named filename. The filename parameter may contain not only the file name but also the names of folders of several levels of nesting: the function will create the specified folders if they do not already exist. If the file exists, it will be overwritten (unless occupied by another program).

As the data parameter, an array of any built-in types can be passed, except for strings. It can also be an array of simple structures containing fields of built-in types with the exception of strings, dynamic arrays, and pointers. Classes are also not supported.

The flag parameter may, if necessary, contain the predefined constant FILE_COMMON, which means creating and writing a file to the common data directory of all terminals (Common/Files/). If the flag is not specified (which corresponds to the default value of 0), then the file is written to the regular data directory (if the MQL program is running in the terminal) or to the testing agent directory (if it happens in the tester). In the last two cases, the MQL5/Files/ sandbox is used inside the directory, as described at the beginning of the chapter.

The function returns an indication of operation success (true) or error (false).

long FileLoad(const string filename, void &data[], const int flag = 0)

The function reads the entire contents of a binary file filename to the specified data array. The file name may include a folder hierarchy within the MQL5/Files or Common/Files sandbox.

The data array must be of any built-in type except string, or a simple structure type (see above).

The flag parameter controls the selection of the directory where the file is searched and opened: by default (with a value of 0) it is the standard sandbox, but if the value FILE_COMMON is set, then it is the sandbox shared by all terminals.

The function returns the number of items read, or -1 on error.

Note that the data from the file is read in blocks of one array element. If the file size is not a multiple of the element size, then the remaining data is skipped (not read). For example, if the file size is 10 bytes, reading it into an array of double type (sizeof(double)=8) will result in only 8 bytes actually being loaded, i.e. 1 element (and the function will return 1). The remaining 2 bytes at the end of the file will be ignored.

In the FileSaveLoad.mq5 script we define two structures for tests.

```
struct Pair
{
   short x, y;
};
  
struct Simple
{
   double d;
   int i;
   datetime t;
   color c;
   uchar a[10]; // fixed size array allowed
   bool b;
   Pair p;      // compound fields (nested simple structures) are also allowed
   
   // strings and dynamic arrays will cause a compilation error when used
   // FileSave/FileLoad: structures or classes containing objects are not allowed
   // string s;
   // uchar a[];
   
   // pointers are also not supported
   // void *ptr;
};

```

The Simple structure contains fields of most allowed types, as well as a composite field with the Pair structure type. In the OnStart function, we fill in a small array of the Simple type.

```
void OnStart()
{
   Simple write[] =
   {
      {+1.0, -1, D'2021.01.01', clrBlue, {'a'}, true, {1000, 16000}},
      {-1.0, -2, D'2021.01.01', clrRed,  {'b'}, true, {1000, 16000}},
   };
   ...

```

We will select the file for writing data together with the MQL5Book subfolder so that our experiments do not mix with your working files:

```
   const string filename = "MQL5Book/rawdata";

```

Let's write an array to a file, read it into another array, and compare them.

```
   PRT(FileSave(filename, write/*, FILE_COMMON*/)); // true
   
   Simple read[];
   PRT(FileLoad(filename, read/*, FILE_COMMON*/)); // 2
   
   PRT(ArrayCompare(write, read)); // 0

```

FileLoad returned 2, i.e., 2 elements (2 structures) were read. If the comparison result is 0, that means that the data matched. You can open the folder in your favorite file manager MQL5/Files/MQL5Book and make sure that there is the 'rawdata' file (it is not recommended to view its contents using a text editor, we suggest using a viewer that supports binary mode).

Further in the script, we convert the read array of structures into bytes and output them to the log in the form of hexadecimal codes. This is a kind of memory dump, and it allows you to understand what binary files are.

```
   uchar bytes[];
   for(int i = 0; i < ArraySize(read); ++i)
   {
      uchar temp[];
      PRT(StructToCharArray(read[i], temp));
      ArrayCopy(bytes, temp, ArraySize(bytes));
   }
   ByteArrayPrint(bytes);

```

Result:

```
 [00] 00 | 00 | 00 | 00 | 00 | 00 | F0 | 3F | FF | FF | FF | FF | 00 | 66 | EE | 5F | 
 [16] 00 | 00 | 00 | 00 | 00 | 00 | FF | 00 | 61 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 
 [32] 00 | 00 | 01 | E8 | 03 | 80 | 3E | 00 | 00 | 00 | 00 | 00 | 00 | F0 | BF | FE | 
 [48] FF | FF | FF | 00 | 66 | EE | 5F | 00 | 00 | 00 | 00 | FF | 00 | 00 | 00 | 62 | 
 [64] 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 01 | E8 | 03 | 80 | 3E | 

```

Because the built-in ArrayPrint function can't print in hexadecimal format, we had to develop our own function ByteArrayPrint (here we will not give its source code, see the attached file).

Next, let's remember that FileLoad is able to load data into an array of any type, so we will read the same file using it directly into an array of bytes.

```
   uchar bytes2[];
   PRT(FileLoad(filename, bytes2/*, FILE_COMMON*/)); // 78,  39 * 2
   PRT(ArrayCompare(bytes, bytes2)); // 0, equality

```

A successful comparison of two byte arrays shows that FileLoad can operate with raw data from the file in an arbitrary way, in which it is instructed (there is no information in the file that it stores an array of Simple structures).

It is important to note here that since the byte type has a minimum size (1), it is a multiple of any file size. Therefore, any file is always read into a byte array without a remainder. Here the FileLoad function has returned the number 78 (the number of elements is equal to the number of bytes). This is the size of the file (two structures of 39 bytes each).

Basically, the ability of FileLoad to interpret data for any type requires care and checks on the part of the programmer. In particular, further in the script, we read the same file into an array of structures MqlDateTime. This, of course, is wrong, but it works without errors.

```
   MqlDateTime mdt[];
   PRT(sizeof(MqlDateTime)); // 32
   PRT(FileLoad(filename, mdt)); // 2
 // attention: 14 bytes left unread
   ArrayPrint(mdt);

```

The result contains a meaningless set of numbers:

```
        [year]      [mon] [day]     [hour]    [min]    [sec] [day_of_week] [day_of_year]
[0]          0 1072693248    -1 1609459200        0 16711680            97             0
[1] -402587648    4096003     0  -20975616 16777215  6286950     -16777216    1644167168

```

Because the size of MqlDateTime is 32, then only two such structures fit in a 78-byte file, and 14 more bytes remain superfluous. The presence of a residue indicates a problem. But even if there is no residue, this does not guarantee the meaningfulness of the operation performed, because two different sizes can, purely by chance, fit an integer (but different) number of times in the length of the file. Moreover, two structures that are different in meaning can have the same size, but this does not mean that they should be written and read from one to the other.

Not surprisingly, the log of the array of structures MqlDateTime shows strange values, since it was, in fact, a completely different data type.

To make reading somewhat more careful, the script implements an analog of the FileLoad function — MyFileLoad. We will analyze this function in detail, as well as its pair MyFileSave, in the following sections, when learning new file functions and using them to model the internal structure FileSave/FileLoad. In the meantime, just note that in our version, we can check for the presence of an unread remainder in the file and display a warning.

To conclude, let's look at a couple more potential errors demonstrated in the script.

```
   /*
  // compilation error, string type not supported here
   string texts[];
   FileSave("any", texts); // parameter conversion not allowed
   */
   
   double data[];
   PRT(FileLoad("any", data)); // -1
   PRT(_LastError); // 5004, ERR_CANNOT_OPEN_FILE

```

The first one happens at compile time (which is why the code block is commented out) because string arrays are not allowed.

The second is to read a non-existent file, which is why FileLoad returns -1. An explanatory error code can be easily obtained using GetLastError (or [_LastError](/en/book/common/environment/env_last_error)).
