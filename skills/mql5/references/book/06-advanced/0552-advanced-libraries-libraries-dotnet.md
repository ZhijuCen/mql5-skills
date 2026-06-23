# Importing functions from .NET libraries

MQL5 provides a special service for working with .NET library functions: you can simply import the DLL itself without specifying certain functions. MetaEditor automatically imports all the functions that you can work with:

- Plain Old Data (POD) — structures that contain only simple data types;
- Public static functions whose parameters use only simple POD types and structures or their arrays.

Unfortunately, at the moment, it is not possible to see function prototypes as they are recognized by MetaEditor.

For example, we have the following C# code of the Inc function of the TestClass class in the TestLib.dll library:

```
public class TestClass
{ 
   public static void Inc(ref int x)
   {
      x++;
   }
}

```

Then, to import and call it, it is enough to write:

```
#import "TestLib.dll"
   
void OnStart()
{
   int x = 1;
   TestClass::Inc(x);
   Print(x);
}

```

After execution, the script will return the value of 2.
