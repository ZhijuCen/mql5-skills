# Writing and reading arrays

Two MQL5 functions are intended for writing and reading arrays: FileWriteArray and FileReadArray. With binary files, they allow you to handle arrays of any built-in type other than strings, as well as arrays of simple structures that do not contain string fields, objects, pointers, and dynamic arrays. These limitations are related to the optimization of the writing and reading processes, which is possible due to the exclusion of types with variable lengths. Strings, objects, and dynamic arrays are just like that.

At the same time, when working with text files, these functions are able to operate on arrays of type string (other types of arrays in files with FILE_TXT/FILE_CSV mode are not allowed by these functions). Such arrays are stored in a file in the following format: one element per line.

If you need to store structures or classes without type restrictions in a file, use type-specific functions that process one value per call. They are described in two sections on writing and reading variables of built-in types: for [binary](/en/book/common/files/files_bin_atomic) and [text](/en/book/common/files/files_txt_atomic) files.

In addition, support for structures with strings can be organized through internal optimization of information storage. For example, instead of string fields, you can use integer fields, which will contain the indices of the corresponding strings in a separate array with strings. Given the possibility of redefining many operations (in particular, the assignment) using OOP tools and obtaining a structural element of an array by number, the appearance of the algorithm will practically not change. But when writing, you can first open a file in binary mode and call FileWriteArray for an array with a simplified structure type and then reopen the file in text mode and add an array of all strings to it using the second FileWriteArray call. To read such a file, you should provide a header at the beginning of it containing the number of elements in the arrays in order to pass it as the count parameter into FileReadArray (see further along).

If you need to save or read not an array of structures, but a single structure, use the FileWriteStruct and FileReadStruct functions which are described in the [next section](/en/book/common/files/files_bin_structs).

Let's study function signatures and then consider a general example (FileArray.mq5).

uint FileWriteArray(int handle, const void &array[], int start = 0, int count = WHOLE_ARRAY)

The function writes the array array to a file with the handle descriptor. The array can be multidimensional. The start and count parameters allow to set the range of elements; by default, it is equal to the entire array. In the case of multidimensional arrays, the start index and the number of elements count refer to continuous numbering across all dimensions, not the first dimension of the array. For example, if the array has the configuration [][5], then the start value equal to 7 will point to the element with indexes [1][2], and count = 2 will add the element [1][3] to it.

The function returns the number of written elements. In case of an error, it will be 0.

If handle is received in binary mode, arrays can be of any built-in type except strings, or simple structure types. If handle is opened in any of the text modes, the array must be of type string.

uint FileReadArray(int handle, const void &array[], int start = 0, int count = WHOLE_ARRAY)

The function reads data from a file with the handle descriptor into an array. The array can be multidimensional and dynamic. For multidimensional arrays, the start and count parameters work on the basis of the continuous numbering of elements in all dimensions, described above. A dynamic array, if necessary, automatically increases in size to fit the data being read. If start is greater than the original length of the array, these intermediate elements will contain random data after memory allocation (see the example).

Pay attention that the function cannot control whether the configuration of the array used when writing the file matches the configuration of the receiving array when reading. Basically, there is no guarantee that the file being read was written with FileWriteArray.  

   

To check the validity of the data structure, some predefined formats of initial headers or other descriptors inside files are usually used. The functions themselves will read any contents of the file within its size and place it in the specified array.

If handle is received in binary mode, arrays can be any of the built-in non-string types or simple structure types. If handle is opened in text mode, the array must be of type string.

Let's check the work both in binary and in text mode using the FileArray.mq5 script. To do this, we will reserve two file names.

```
const string raw = "MQL5Book/array.raw";
const string txt = "MQL5Book/array.txt";

```

Three arrays of type long and two arrays of type string are described in the OnStart function. Only the first array of each type is filled with data, and all the rest will be checked for reading after the files are written.

```
void OnStart()
{
   long numbers1[][2] = {{1, 4}, {2, 5}, {3, 6}};
   long numbers2[][2];
   long numbers3[][2];
   
   string text1[][2] = {{"1.0", "abc"}, {"2.0", "def"}, {"3.0", "ghi"}};
   string text2[][2];
   ...

```

In addition, to test operations with structures, the following 3 types are defined:

```
struct TT
{
   string s1;
   string s2;
};
  
struct B
{
private:
   int b;
public:
   void setB(const int v) { b = v; }
};
  
struct XYZ : public B
{
   color x, y, z;
};

```

We will not be able to use a structure of the TT type in the described functions because it contains string fields. It is needed to demonstrate a potential compilation error in a commented statement (see further along). Inheritance between structures B and XYZ, as well as the presence of a closed field, are not an obstacle for the functions FileWriteArray and FileReadArray.

The structures are used to declare a pair of arrays:

```
 TTtt[]; // empty, because data is not important
   XYZ xyz[1];
   xyz[0].setB(-1);
   xyz[0].x = xyz[0].y = xyz[0].z = clrRed;

```

Let's start with binary mode. Let's create a new file or open an existing file, dumping its contents. Then, in three FileWriteArray calls, we will try to write three arrays: numbers1, text1 and xyz.

```
   int writer = PRTF(FileOpen(raw, FILE_BIN | FILE_WRITE)); // 1 / ok
   PRTF(FileWriteArray(writer, numbers1)); // 6 / ok
   PRTF(FileWriteArray(writer, text1)); // 0 / FILE_NOTTXT(5012)
   PRTF(FileWriteArray(writer, xyz)); // 1 / ok
   FileClose(writer);
   ArrayPrint(numbers1);

```

Arrays numbers1 and xyz are written successfully, as indicated by the number of items written. The text1 array fails with a FILE_NOTTXT(5012) error because string arrays require the file to be opened in text mode. Therefore the content xyz will be located in the file immediately after all elements of numbers1.

Note that each write (or read) function starts writing (or reading) data to the current position within the file, and shifts it by the size of the written or read data. If this pointer is at the end of the file before the write operation, the file size is increased. If the end of the file is reached while reading, the pointer no longer moves and the system raises a special internal error code 5027 (FILE_ENDOFFILE). In a new file of the zero size, the beginning and end are the same.

From an array text1, 0 items were written, so nothing in the file reminds you that between two successful calls FileWriteArray there was one failure.

In the test script, we simply output the result of the function and the status (error code) to the log, but in a real program, we should analyze problems on the go and take some actions: fix something in the parameters, in the file settings, or interrupt the process with a message to the user.

Let's read a file into the numbers2 array.

```
   int reader = PRTF(FileOpen(raw, FILE_BIN | FILE_READ)); // 1 / ok
   PRTF(FileReadArray(reader, numbers2)); // 8 / ok
   ArrayPrint(numbers2);

```

Since two different arrays were written to the file (not only numbers1, but also xyz), 8 elements were read into the receiving array (i.e., the entire file to the end, because otherwise was not specified using parameters).

Indeed, the size of the structure XYZ is 16 bytes (4 fields of 4 bytes: one int and three color), which corresponds to one row in the array numbers2 (2 elements of type long). In this case, it's a coincidence. As noted above, the functions have no idea about the configuration and size of the raw data and can read anything into any array: the programmer must monitor the validity of the operation.

Let's compare the initial and received states. Source array numbers1:

```
       [,0][,1]
   [0,]   1   4
   [1,]   2   5
   [2,]   3   6

```

Resulting array numbers2:

```
                 [,0]          [,1]
   [0,]             1             4
   [1,]             2             5
   [2,]             3             6
   [3,] 1099511627775 1095216660735

```

The beginning of the numbers2 array completely matches the original numbers1 array, i.e., writing and reading through the file work properly.

The last row is entirely occupied by a single structure XYZ (with correct values, but incorrect representation as two numbers of type long).

Now we get to the file beginning (using the FileSeek function, which we will discuss later in the section [Position control within a file](/en/book/common/files/files_cursor)) and call FileReadArray indicating the number and quantity of elements, i.e., we perform a partial reading.

```
   PRTF(FileSeek(reader, 0, SEEK_SET)); // true
   PRTF(FileReadArray(reader, numbers3, 10, 3));
   FileClose(reader);
   ArrayPrint(numbers3);

```

Three elements are read from the file and placed, starting at index 10, into the receiving array numbers3. Since the file is read from the beginning, these elements are the values 1, 4, 2. And since a two-dimensional array has the configuration [][2], the through index 10 points to the element [5,0]. Here's what it looks like in memory:

```
       [,0][,1]
   [0,]   1   4
   [1,]   1   4
   [2,]   2   6
   [3,]   0   0
   [4,]   0   0
   [5,]   1   4
   [6,]   2   0

```

Items marked in yellow are random (may change for different script runs). It is possible that they will all be zero, but this is not guaranteed. The numbers3 array initially was empty and the FileReadArray call initiated an allocation of memory required to receive 3 elements at offset 10 (total 13). The selected block is not filled with anything, and only 3 numbers are read from the file. Therefore, elements with through indices from 0 to 9 (i.e. the first 5 rows), as well as the last one, with index 13, contain garbage.

Multidimensional arrays are scaled along the first dimension, and therefore an increase of 1 number means adding the entire configuration along higher dimensions. In this case, the distribution concerns a series of two numbers ([][2]). In other words, the requested size 13 is rounded up to a multiple of two, that is, 14.

Finally, let's test how the functions work with string arrays. Let's create a new file or open an existing file, dumping its contents. Then, in two FileWriteArray calls, we will write the text1 and numbers1 arrays.

```
   writer = PRTF(FileOpen(txt, FILE_TXT | FILE_ANSI | FILE_WRITE)); // 1 / ok
   PRTF(FileWriteArray(writer, text1)); // 6 / ok
   PRTF(FileWriteArray(writer, numbers1)); // 0 / FILE_NOTBIN(5011)
   FileClose(writer);

```

The string array is saved successfully. The numeric array is ignored with a FILE_NOTBIN(5011) error because it must open the file in binary mode.

When trying to write an array of structures tt, we get a compilation error with a lengthy message "structures or classes with objects are not allowed". What the compiler actually means is that it doesn't like fields like string (it is assumed that strings and dynamic arrays have an internal representation of some service objects). Thus, despite the fact that the file is opened in text mode and there are only text fields in the structure, this combination is not supported in MQL5.

```
   // COMPILATION ERROR: structures or classes containing objects are not allowed
   FileWriteArray(writer, tt);

```

The presence of string fields makes the structure "complicated" and unsuitable for working with functions FileWriteArray/FileReadArray in any mode.

After running the script, you can change to the directory MQL5/Files/MQL5Book and examine the contents of the generated files.

Earlier, in the section [Writing and reading files in simplified mode](/en/book/common/files/files_save_load), we discussed the FileSave and FileLoad functions. In the test script (FileSaveLoad.mq5), we have implemented the equivalent versions of these functions using FileWriteArray and FileReadArray. But we have not seen them in detail. Since we are now familiar with these new functions, we can examine the source code:

```
template<typename T>
bool MyFileSave(const string name, const T &array[], const int flags = 0)
{
   const int h = FileOpen(name, FILE_BIN | FILE_WRITE | flags);
   if(h == INVALID_HANDLE) return false;
   FileWriteArray(h, array);
   FileClose(h);
   return true;
}
   
template<typename T>
long MyFileLoad(const string name, T &array[], const int flags = 0)
{
   const int h = FileOpen(name, FILE_BIN | FILE_READ | flags);
   if(h == INVALID_HANDLE) return -1;
   const uint n = FileReadArray(h, array, 0, (int)(FileSize(h) / sizeof(T)));
   // this version has the following check added compared to the standard FileLoad:
   // if the file size is not a multiple of the structure size, print a warning
   const ulong leftover = FileSize(h) - FileTell(h);
   if(leftover != 0)
   {
      PrintFormat("Warning from %s: Some data left unread: %d bytes", 
         __FUNCTION__, leftover);
      SetUserError((ushort)leftover);
   }
   FileClose(h);
   return n;
}

```

MyFileSave is built on a single call of FileWriteArray, and MyFileLoad on FileReadArray call, between a pair of FileOpen/FileClose calls. In both cases, all available data is written and read. Thanks to templates, our functions are also able to accept arrays of arbitrary types. But if any unsupported type (for example, a class) is deduced as a meta parameter T, then a compilation error will occur, as is the case with incorrect access to built-in functions.
