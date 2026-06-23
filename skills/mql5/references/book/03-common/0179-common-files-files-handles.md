# Managing file descriptors

Since we need to constantly remember about open files and to release local descriptors on any exit from functions, it would be efficient to entrust the entire routine to special objects.

This approach is well-known in programming and is called Resource Acquisition Is Initialization (RAII). Using RAII makes it easier to control resources and ensure they are in the correct state. In particular, this is especially effective if the function that opens the file (and creates an owner object for it) exits from several different places.

The scope of RAII is not limited to files. In the section [Object type templates](/en/book/oop/templates/templates_objects), we created the AutoPtr class, which manages a pointer to an object. It was another example of this concept, since a pointer is also a resource (memory), and it is very easy to lose it as well as it is resource-consuming to release it in several different branches of the algorithm.

A file wrapper class can be useful in another way as well. The file API does not provide a function that would allow you to get the name of a file by a descriptor (despite the fact that such a relationship certainly exists internally). At the same time, inside the object, we can store this name and implement our own binding to the descriptor.

In the simplest case, we need some class that stores a file descriptor and automatically closes it in the destructor. An example implementation is shown in the FileHandle.mqh file.

```
class FileHandle
{
   int handle;
public:
   FileHandle(const int h = INVALID_HANDLE) : handle(h)
   {
   }
   
   FileHandle(int &holder, const int h) : handle(h)
   {
      holder = h;
   }
   
   int operator=(const int h)
   {
      handle = h;
      return h;
   }
   ...

```

Two constructors, as well as an overloaded assignment operator, ensure that an object is bound to a file (descriptor). The second constructor allows you to pass a reference to a local variable (from the calling code), which will additionally get a new descriptor. This will be a kind of external alias for the same descriptor, which can be used in the usual way in other function calls.

But you can do without an alias too. For these cases, the class defines the operator '~', which returns the value of the internal handle variable.

```
   int operator~() const
   {
      return handle;
   }

```

Finally, the most important thing for which the class was implemented is the smart destructor:

```
   ~FileHandle()
   {
      if(handle != INVALID_HANDLE)
      {
         ResetLastError();
         // will set internal error code if handle is invalid
         FileGetInteger(handle, FILE_SIZE);
         if(_LastError == 0)
         {
            #ifdef FILE_DEBUG_PRINT
               Print(__FUNCTION__, ": Automatic close for handle: ", handle);
            #endif
            FileClose(handle);
         }
         else
         {
            PrintFormat("%s: handle %d is incorrect, %s(%d)", 
               __FUNCTION__, handle, E2S(_LastError), _LastError);
         }
      }
   }

```

In it, after several checks, FileClose is called for the controlled handle variable. The point is that the file can be explicitly closed elsewhere in the program, although this is no longer required with this class. As a result, the descriptor may become invalid by the time the destructor is called when the execution of the algorithm leaves the block in which the FileHandle object is defined. To find this out, a dummy call to the [FileGetInteger](/en/book/common/files/files_properties) function is used. It is a dummy because it doesn't do anything useful. If the internal error code remains 0 after the call, the descriptor is valid.

We can omit all these checks and simply write the following:

```
   ~FileHandle()
   {
      if(handle != INVALID_HANDLE)
      {
         FileClose(handle);
      }
   }

```

If the descriptor is corrupted, FileClose won't return any warning. But we have added checks to be able to output diagnostic information.

Let's try the FileHandle class in action. The test script for it is called FileHandle.mq5.

```
const string dummy = "MQL5Book/dummy";
   
void OnStart()
{
   // creating a new file or open an existing one and reset it
   FileHandle fh1(PRTF(FileOpen(dummy, 
      FILE_TXT | FILE_WRITE | FILE_SHARE_WRITE | FILE_SHARE_READ))); // 1
   // another way to connect the descriptor via '='
   int h = PRTF(FileOpen(dummy, 
      FILE_TXT | FILE_WRITE | FILE_SHARE_WRITE | FILE_SHARE_READ)); // 2
   FileHandle fh2 = h;
   // and another supported syntax:
   // int f;
   // FileHandle ff(f, FileOpen(dummy,
   //    FILE_TXT | FILE_WRITE | FILE_SHARE_WRITE | FILE_SHARE_READ));
   
   // data is supposed to be written here
   // ...
   
   // close the file manually (this is not necessary; only done to demonstrate 
   // that the FileHandle will detect this and won't try to close it again)
   FileClose(~fh1); // operator '~' applied to an object returns a handle
   
   // descriptor handle in variable 'h' bound to object 'fh2' is not manually closed
   // and will be automatically closed in the destructor
}

```

According to the output in the log, everything works as planned:

```
   FileHandle::~FileHandle: Automatic close for handle: 2
   FileHandle::~FileHandle: handle 1 is incorrect, INVALID_FILEHANDLE(5007)

```

However, if there are lots of files, creating a tracking object copy for each of them can become an inconvenience. For such situations, it makes sense to design a single object that collects all descriptors in a given context (for example, inside a function).

Such a class is implemented in the FileHolder.mqh file and is shown in the FileHolder.mq5 script. One copy of FileHolder itself creates upon request auxiliary observing objects of the FileOpener class, which shares common features with FileHandle, especially the destructor, as well as the handle field.

To open a file via FileHolder, you should use its FileOpen method (its signature repeats the signature of the standard FileOpen function).

```
class FileHolder
{
   static FileOpener *files[];
   int expand()
   {
      return ArrayResize(files, ArraySize(files) + 1) - 1;
   }
public:
   int FileOpen(const string filename, const int flags, 
                const ushort delimiter = '\t', const uint codepage = CP_ACP)
   {
      const int n = expand();
      if(n > -1)
      {
         files[n] = new FileOpener(filename, flags, delimiter, codepage);
         return files[n].handle;
      }
      return INVALID_HANDLE;
   }

```

All FileOpener objects add up in the files array for tracking their lifetime. In the same place, zero elements mark the moments of registration of local contexts (blocks of code) in which FileHolder objects are created. The FileHolder constructor is responsible for this.

```
   FileHolder()
   {
      const int n = expand();
      if(n > -1)
      {
         files[n] = NULL;
      }
   }

```

As we know, during the execution of a program, it enters nested code blocks (it calls functions). If they require the management of local file descriptors, the FileHolder objects (one per block or less) should be described there. According to the rules of the stack (first in, last out), all such descriptions add up at files and then are released in reverse order as the program leaves the contexts. The destructor is called at each such moment.

```
   ~FileHolder()
   {
      for(int i = ArraySize(files) - 1; i >= 0; --i)
      {
         if(files[i] == NULL)
         {
            // decrement array and exit
            ArrayResize(files, i);
            return;
         }
         
         delete files[i];
      }
   }

```

Its task is to remove the last FileOpener objects in the array up to the first encountered zero element, which indicates the boundary of the context (further in the array are descriptors from another, external context).

You can study the whole class on your own.

Let's look at its use in the test script FileHolder.mq5. In addition to the OnStart function, it has SubFunc. Operations with files are performed in both contexts.

```
const string dummy = "MQL5Book/dummy";
   
void SubFunc()
{
   Print(__FUNCTION__, " enter");
   FileHolder holder;
   int h = PRTF(holder.FileOpen(dummy, 
      FILE_BIN | FILE_WRITE | FILE_SHARE_WRITE | FILE_SHARE_READ));
   int f = PRTF(holder.FileOpen(dummy, 
      FILE_BIN | FILE_WRITE | FILE_SHARE_WRITE | FILE_SHARE_READ));
   // use h and f
   // ...
   // no need to manually close files and track early function exits
   Print(__FUNCTION__, " exit");
}
 
void OnStart()
{
   Print(__FUNCTION__, " enter");
   
   FileHolder holder;
   int h = PRTF(holder.FileOpen(dummy, 
      FILE_BIN | FILE_WRITE | FILE_SHARE_WRITE | FILE_SHARE_READ));
   // writing data and other actions on the file by descriptor
   // ...
   /*
   int a[] = {1, 2, 3};
   FileWriteArray(h, a);
   */
   
   SubFunc();
   SubFunc();
   
 if(rand() >32000) // simulate branching by conditions
   {
      // thanks to the holder we don't need an explicit call
      // FileClose(h);
      Print(__FUNCTION__, " return");
      return; // there can be many exits from the function
   }
   
   /*
     ... more code
   */
   
   // thanks to the holder we don't need an explicit call
   // FileClose(h);
   Print(__FUNCTION__, " exit");
}

```

We have not closed any handles manually, instances of FileHolder will do it automatically in the destructors.

Here is an example of logging output:

```
OnStart enter
holder.FileOpen(dummy,FILE_BIN|FILE_WRITE|FILE_SHARE_WRITE|FILE_SHARE_READ)=1 / ok
SubFunc enter
holder.FileOpen(dummy,FILE_BIN|FILE_WRITE|FILE_SHARE_WRITE|FILE_SHARE_READ)=2 / ok
holder.FileOpen(dummy,FILE_BIN|FILE_WRITE|FILE_SHARE_WRITE|FILE_SHARE_READ)=3 / ok
SubFunc exit
FileOpener::~FileOpener: Automatic close for handle: 3
FileOpener::~FileOpener: Automatic close for handle: 2
SubFunc enter
holder.FileOpen(dummy,FILE_BIN|FILE_WRITE|FILE_SHARE_WRITE|FILE_SHARE_READ)=2 / ok
holder.FileOpen(dummy,FILE_BIN|FILE_WRITE|FILE_SHARE_WRITE|FILE_SHARE_READ)=3 / ok
SubFunc exit
FileOpener::~FileOpener: Automatic close for handle: 3
FileOpener::~FileOpener: Automatic close for handle: 2
OnStart exit
FileOpener::~FileOpener: Automatic close for handle: 1

```
