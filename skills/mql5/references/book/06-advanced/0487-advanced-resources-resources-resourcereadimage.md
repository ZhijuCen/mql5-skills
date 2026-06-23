# Reading and modifying resource data: ResourceReadImage

The ResourceReadImage function allows reading the data of the resource created by the [ResourceCreate](/en/book/advanced/resources/resources_resourcecreate) function or embedded into the executable at compile time according to the [#resource](/en/book/advanced/resources/resources_directive) directive. Despite the suffix "Image" in the name, the function works with any data arrays, including custom ones (see the example of Reservoir.mq5 below).

bool ResourceReadImage(const string resource, uint &data[], uint &width, uint &height)

The name of the resource is specified in the resource parameter. To access your own resources, the short form "::resource_name" is sufficient. To read a resource from another compiled file, you need the full name followed by the path according to the path resolution rules described in the section on [resources](/en/book/advanced/resources/resources_directive). In particular, a path starting with a backslash means the path from the MQL5 root folder (this way "\\path\\filename.ex5::resource_name" is searched for in the file /MQL5/path/filename.ex5 under the name "resource_name"), and the path without this leading character means the path relative to the folder where the executed program is located.

The internal information of the resource will be written into the receiving data array, and the width and height parameters will receive, respectively, the width and height, that is, the size of the array (width*height) indirectly. Separately, width and height are only relevant if the image is stored in the resource. The array must be dynamic or fixed, but of sufficient size. Otherwise, we will get a SMALL_ARRAY (5052) error.

If in the future you want to create a graphic resource based on the data array, then the source resource should use the COLOR_FORMAT_ARGB_NORMALIZE or COLOR_FORMAT_XRGB_NOALPHA color format. If the data array contains arbitrary application data, use COLOR_FORMAT_XRGB_NOALPHA.

As a first example, let's consider the script ResourceReadImage.mq5. It demonstrates several aspects of working with graphic resources:

- Creating an image resource from an external file
- Reading and modifying the data of this image in another dynamically created resource
- Preserving created resources in the terminal memory between script launches
- Using resources in objects on the chart
- Deleting an object and resources

Image modifying in this particular case means the inversion of all colors (as the most visual).

All of the above methods of work are performed in three stages: each stage is performed in one run of the script. The script determines the current stage by analyzing the available resources and the object:

1. In the absence of the required graphic resources, the script will create them (one original image and one inverted image).
2. If there are resources but there is no graphic object, the script will create an object with two images from the first step for on/off states (they can be switched by mouse click).
3. If there is an object, the script will delete the object and resources.

The main function of the script starts by defining the names of the resources and of the object on the chart.

```
void OnStart()
{
   const static string resource = "::Images\\pseudo.bmp";
   const static string inverted = resource + "_inv";
   const static string object = "object";
   ...

```

Note that we have chosen a name for the original resource that looks like the location of the bmp file in the standard Images folder, but there is no such file. This emphasizes the virtual nature of resources and allows you to make substitutions to meet technical requirements or to make it difficult to reverse engineer your programs.

The next ResourceReadImage call is used to check if the resource already exists. In the initial state (on the first run), we will get a negative result (false) and start the first step: we create the original resource from the file "\\Images\\dollar.bmp", and then invert it in a new resource with the "_inv" suffix.

```
   uint data[], width, height;
   // check for resource existence
   if(!PRTF(ResourceReadImage(resource, data, width, height)))
   {
      Print("Initial state: Creating 2 bitmaps");
      PRTF(ResourceCreate(resource, "\\Images\\dollar.bmp")); // try "argb.bmp"
      ResourceCreateInverted(resource, inverted);
   }
   ...

```

The source code of the helper function ResourceCreateInverted will be presented below.

If the resource is found (second run), the script checks for the existence of the object and, if necessary, creates it, including setting properties with image resources in the ShowBitmap function (see below).

```
   else
   {
      Print("Resources (bitmaps) are detected");
      if(PRTF(ObjectFind(0, object) < 0))
      {
         Print("Active state: Creating object to draw 2 bitmaps");
         ShowBitmap(object, resource, inverted);
      }
      ...

```

If both the resources and the object are already on the chart, then we are at the final stage and must remove all resources.

```
      else
      {
         Print("Cleanup state: Removing object and resources");
         PRTF(ObjectDelete(0, object));
         PRTF(ResourceFree(resource));
         PRTF(ResourceFree(inverted));
      }
   }
}

```

The ResourceCreateInverted function uses the ResourceReadImage call to get an array of pixels and then inverts the color into them using the '^' (XOR) operator and an operand with all singular bits in the color components.

```
bool ResourceCreateInverted(const string resource, const string inverted)
{
   uint data[], width, height;
   PRTF(ResourceReadImage(resource, data, width, height));
   for(int i = 0; i < ArraySize(data); ++i)
   {
      data[i] = data[i] ^ 0x00FFFFFF;
   }
   return PRTF(ResourceCreate(inverted, data, width, height, 0, 0, 0,
      COLOR_FORMAT_ARGB_NORMALIZE));
}

```

The new array data is transferred to ResourceCreate to create the second image.

The ShowBitmap function creates a graphic object in the usual way (in the lower right corner of the graph) and sets its properties for on and off states to the original and inverted images, respectively.

```
void ShowBitmap(const string name, const string resourceOn, const string resourceOff = NULL)
{
   ObjectCreate(0, name, OBJ_BITMAP_LABEL, 0, 0, 0);
   
   ObjectSetString(0, name, OBJPROP_BMPFILE, 0, resourceOn);
   if(resourceOff != NULL) ObjectSetString(0, name, OBJPROP_BMPFILE, 1, resourceOff);
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, 50);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, 50);
   ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_RIGHT_LOWER);
   ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER);
}

```

Since the newly created object is off by default, we will first see the inverted image and we can switch it to the original one on a mouse click. But let's remind you that our script performs actions step by step, and therefore, before the image appears on the chart, the script must be run twice. At all stages, the current status and actions performed (along with a success or error indication) are logged.

After the first launch, the following entries will appear in the log:

```
ResourceReadImage(resource,data,width,height)=false / RESOURCE_NOT_FOUND(4016)
Initial state: Creating 2 bitmaps
ResourceCreate(resource,\Images\dollar.bmp)=true / ok
ResourceReadImage(resource,data,width,height)=true / ok
ResourceCreate(inverted,data,width,height,0,0,0,COLOR_FORMAT_XRGB_NOALPHA)=true / ok

```

The logs indicate that the resources have not been found and that's why the script has created them. After the second run, the log will say that resources have been found (which were left in memory from the previous run of the script) but the object is not there yet, and the script will create it based on the resources.

```
ResourceReadImage(resource,data,width,height)=true / ok
Resources (bitmaps) are detected
ObjectFind(0,object)<0=true / OBJECT_NOT_FOUND(4202)
Active state: Creating object to draw 2 bitmaps

```

We will see an object and an image on the chart. Switching states is available by mouse click ([events](/en/book/applications/events/events_objects) about changes of the state are not handled here).

![Inverted and original images in an object on a chart](pics/inverted_vs_original.png)

Inverted and original images in an object on a chart

Finally, during the third run, the script will detect the object and delete all its developments.

```
ResourceReadImage(resource,data,width,height)=true / ok
Resources (bitmaps) are detected
ObjectFind(0,object)<0=false / ok
Cleanup state: Removing object and resources
ObjectDelete(0,object)=true / ok
ResourceFree(resource)=true / ok
ResourceFree(inverted)=true / ok

```

Then you can repeat the cycle.

The second example of the section will consider the use of resources for storing arbitrary application data, that is, a kind of clipboard inside the terminal (in theory, there can be any number of such buffers, since each of them is a separate named resource). Due to the universality of the problem, we will create the Reservoir class with the main functionality (in the file Reservoir.mqh), and on its basis we will write a demo script (Reservoir.mq5).

Before "diving" directly into Reservoir, let's introduce an auxiliary union ByteOverlay which will be required often. A union will allow any simple built-in type (including simple structures) to be converted to a byte array and vice versa. By "simple" we mean all built-in numeric types, date and time, enumerations, color, and boolean flags. However, objects and dynamic arrays are no longer simple and will not be supported by our new storage (due to technical limitations of the platform). Strings are also not considered simple but for them, we will make an exception and will process them in a special way.

```
template<typename T>
union ByteOverlay
{
   uchar buffer[sizeof(T)];
   T value;
   
   ByteOverlay(const T &v)
   {
      value = v;
   }
   
   ByteOverlay(const uchar &bytes[], const int offset = 0)
   {
      ArrayCopy(buffer, bytes, 0, offset, sizeof(T));
   }
};

```

As we know, resources are built on the basis of arrays of type uint, so we describe such an array (storage) in the Reservoir class. There we will add all the data to be subsequently written to the resource. The current position in the array where data is written or read from is stored in the offset field.

```
class Reservoir
{
   uint storage[];
   int offset;
public:
   Reservoir(): offset(0) { }
   ...

```

To place an array of data of arbitrary type into storage, you can use the template method packArray. In the first half of it, we convert the passed array into a byte array using ByteOverlay.

```
   template<typename T>
   int packArray(const T &data[])
   {
      const int bytesize = ArraySize(data) * sizeof(T); // TODO: check for overflow
      uchar buffer[];
      ArrayResize(buffer, bytesize);
      for(int i = 0; i < ArraySize(data); ++i)
      {
         ByteOverlay<T> overlay(data[i]);
         ArrayCopy(buffer, overlay.buffer, i * sizeof(T));
      }
      ...

```

In the second half, we convert the byte array into a sequence of uint values, which are written in storage with an offset. The number of required elements uint is determined by taking into account whether there is a remainder after dividing the size of the data in bytes by the size of uint: optionally we add one additional element.

```
      const int size = bytesize / sizeof(uint) + (bool)(bytesize % sizeof(uint));
      ArrayResize(storage, offset + size + 1);
      storage[offset] = bytesize;       // write the size of the data before the data
      for(int i = 0; i < size; ++i)
      {
         ByteOverlay<uint> word(buffer, i * sizeof(uint));
         storage[offset + i + 1] = word.value;
      }
      
      offset = ArraySize(storage);
      
      return offset;
   }

```

Before the data itself, we write the size of the data in bytes: this is the smallest possible protocol for error checking when recovering data. In the future, it would be possible to write the typename(T) data in the storage as well.

The method returns the current position in the storage after writing.

Based on packArray, it's easy to implement a method to save strings:

```
   int packString(const string text)
   {
      uchar data[];
      StringToCharArray(text, data, 0, -1, CP_UTF8);
      return packArray(data);
   }

```

There is also an option to store a separate number:

```
   template<typename T>
   int packNumber(const T number)
   {
      T array[1] = {number};
      return packArray(array);
   }

```

A method for restoring an array of arbitrary type T from the storage of type uint "loses" all operations in the opposite direction. If inconsistencies are found in the readable type and amount of data with the storage, the method returns 0 (an error sign). In normal mode, the current position in the array storage is returned (it is always greater than 0 if something was successfully read).

```
   template<typename T>
   int unpackArray(T &output[])
   {
      if(offset >= ArraySize(storage)) return 0; // out of array bounds
      const int bytesize = (int)storage[offset];
      if(bytesize % sizeof(T) != 0) return 0;    // wrong data type
      if(bytesize > (ArraySize(storage) - offset) * sizeof(uint)) return 0;
      
      uchar buffer[];
      ArrayResize(buffer, bytesize);
      for(int i = 0, k = 0; i < ArraySize(storage) - 1 - offset
         && k < bytesize; ++i, k += sizeof(uint))
      {
         ByteOverlay<uint> word(storage[i + 1 + offset]);
         ArrayCopy(buffer, word.buffer, k);
      }
      
      int n = bytesize / sizeof(T);
      n = ArrayResize(output, n);
      for(int i = 0; i < n; ++i)
      {
         ByteOverlay<T> overlay(buffer, i * sizeof(T));
         output[i] = overlay.value;
      }
      
      offset += 1 + bytesize / sizeof(uint) + (bool)(bytesize % sizeof(uint));
      
      return offset;
   }

```

Unpacking strings and numbers is done by calling unpackArray.

```
   int unpackString(string &output)
   {
      uchar bytes[];
      const int p = unpackArray(bytes);
      if(p == offset)
      {
         output = CharArrayToString(bytes, 0, -1, CP_UTF8);
      }
      return p;
   }
   
   template<typename T>
   int unpackNumber(T &number)
   {
      T array[1] = {};
      const int p = unpackArray(array);
      number = array[0];
      return p;
   }

```

Simple helper methods allow you to find out the size of the storage and the current position in it, as well as clear it.

```
   int size() const
   {
      return ArraySize(storage);
   }
   
   int cursor() const
   {
      return offset;
   }
   
   void clear()
   {
      ArrayFree(storage);
      offset = 0;
   }

```

Now we come to the most interesting: interaction with resources.

Having filled the storage array with application data, it is easy to "move" it to a provided resource.

```
   bool submit(const string resource)
   {
      return ResourceCreate(resource, storage, ArraySize(storage), 1,
         0, 0, 0, COLOR_FORMAT_XRGB_NOALPHA);
   }

```

Also, we can just read data from a resource into an internal array storage.

```
   bool acquire(const string resource)
   {
      uint width, height;
      if(ResourceReadImage(resource, storage, width, height))
      {
         return true;
      }
      return false;
   }

```

We will show in the script Reservoir.mq5, how to use it.

In the first half of OnStart, we describe the name for the storage resource and the class object Reservoir, and then sequentially "pack" into this object a string, structure MqlTick, and number double. The structure is "wrapped" in an array of one element to explicitly demonstrate the packArray method. In addition, we will then need to compare the restored data with the original ones, and MQL5 does not provide the '==' operator for structures. Therefore it will be more convenient to use the ArrayCompare function.

```
#include <MQL5Book/Reservoir.mqh>
#include <MQL5Book/PRTF.mqh>
   
void OnStart()
{
   const string resource = "::reservoir";
   
   Reservoir res1;
   string message = "message1";     // string to write to the resource
   PRTF(res1.packString(message));
   
   MqlTick tick1[1];                // add a simple structure
   SymbolInfoTick(_Symbol, tick1[0]);
   PRTF(res1.packArray(tick1));
   PRTF(res1.packNumber(DBL_MAX));  // real number
   ...

```

When all the necessary data is "packed" into the object, write it to the resource and clear the object.

```
   res1.submit(resource);           // create a resource with storage data
   res1.clear();                    // clear the object, but not the resource

```

In the second half of OnStart let's perform the reverse operations of reading data from the resource.

```
   string reply;                    // new variable for message
   MqlTick tick2[1];                // new structure for tick
   double result;                   // new variable for number
   
   PRTF(res1.acquire(resource));    // connect the object to the given resource
   PRTF(res1.unpackString(reply));  // read line
   PRTF(res1.unpackArray(tick2));   // read simple structure
   PRTF(res1.unpackNumber(result)); // read number
   
   // output and compare data element by element
   PRTF(reply);
   PRTF(ArrayCompare(tick1, tick2));
   ArrayPrint(tick2);
   PRTF(result == DBL_MAX);
   
   // make sure the storage is read completely
   PRTF(res1.size());
   PRTF(res1.cursor());
   ...

```

In the end, we clean up the resource, since this is a test. In practical tasks, an MQL program will most likely leave the created resource in memory so that it can be read by other programs. In the naming hierarchy, resources are declared nested in the program that created them. Therefore, for access from other programs, you must specify the name of the resource along with the name of the program and optionally the path (if the program-creator and the program-reader are in different folders). For example, to read a newly created resource from outside, the full path "\\Scripts\\MQL5Book\\p7\\Reservoir.ex5::reservoir" will do the job.

```
   PrintFormat("Cleaning up local storage '%s'", resource);
   ResourceFree(resource);
}

```

Since all major method calls are controlled by the PRTF macro, when we run the script, we will see a detailed progress "report" in the log.

```
res1.packString(message)=4 / ok
res1.packArray(tick1)=20 / ok
res1.packNumber(DBL_MAX)=23 / ok
res1.acquire(resource)=true / ok
res1.unpackString(reply)=4 / ok
res1.unpackArray(tick2)=20 / ok
res1.unpackNumber(result)=23 / ok
reply=message1 / ok
ArrayCompare(tick1,tick2)=0 / ok
                 [time]   [bid]   [ask] [last] [volume]    [time_msc] [flags] [volume_real]
[0] 2022.05.19 23:09:32 1.05867 1.05873 0.0000        0 1653001772050       6       0.00000
result==DBL_MAX=true / ok
res1.size()=23 / ok
res1.cursor()=23 / ok
Cleaning up local storage '::reservoir'

```

The data was successfully copied to the resource and then restored from there.

Programs can use this approach to exchange bulky data that does not fit in custom messages (events[CHARTEVENT_CUSTOM+](/en/book/applications/events/events_custom)). It is enough to send in a string parameter sparam the name of the resource to read. To post back data, create your own resource with it and send a response message.
