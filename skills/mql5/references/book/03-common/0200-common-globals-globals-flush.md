# Flushing global variables to disk

To optimize performance, global variables reside in memory while the terminal is running. However, as we know, variables are stored between sessions in a special file. This applies to all global variables except [temporary](/en/book/common/globals/globals_temp) variables. Normally writing variables to a file happens when the terminal closes. However, if your computer suddenly crashes, your data may be lost. Therefore, it can be useful to forcibly initiate writing in order to guarantee the safety of data in any unforeseen situations. For this purpose, the MQL5 API provides the GlobalVariablesFlush function.

void GlobalVariablesFlush()

The function forces the contents of global variables to be written to disk. The function has no parameters and returns nothing.

The simplest example is given in the script GlobalsFlush.mq5.

```
void OnStart()
{
   GlobalVariablesFlush();
}

```

With it, you can flush variables to disk at any time, if necessary. You can use your preferred file manager and make sure that the date and time of the gvariables.dat file change immediately after the script is run. However, note that the file will only be updated if the global variables have been edited in any way or just read (this changes the access time) since the previous save.

This script is useful for those who keep the terminal turned on for a long time, and programs that modify global variables are executed in it.
