# Writing and reading global variables

The MQL5 API provides 2 functions to write and read global variables: GlobalVariableSet and GlobalVariableGet (in two versions).

datetime GlobalVariableSet(const string name, double value)

The function sets a new value to the 'name' global variable. If the variable did not exist before the function was called, it will be created. If the variable already exists, the previous value will be replaced by value.

If successful, the function returns the variable modification time (the current local time of the computer). In case of an error, we get 0.

double GlobalVariableGet(const string name)

bool GlobalVariableGet(const string name, double &value)

The function returns the value of the 'name' global variable. The result of calling the first version of the function contains just the value of the variable (in case of success) or 0 (in case of error). Since the variable can contain the value of 0 (which is the same as an error indication), this option requires parsing the internal error code [_LastError](/en/book/common/environment/env_last_error) if zero is received, to distinguish the standard version from the non-standard one. In particular, if an attempt is made to read a variable that does not exist, an internal error 4501 (GLOBALVARIABLE_NOT_FOUND) is generated.

This function version is convenient to use in algorithms where getting zero is a suitable analog of the default initialization for a previously nonexistent variable (see example below). If the absence of a variable needs to be handled in a special way (in particular, to calculate some other starting value), you should first check the existence of the variable using the [GlobalVariableCheck](/en/book/common/globals/globals_exist_time) function and, depending on its result, execute different code branches. Optionally, you can use the second version.

The second version of the function returns true or false depending on the success of the execution. If successful, the value of the global variable of the terminal is placed in the receiving value variable, passed by reference as the second parameter. If there is no variable, we get false.

In the test script GlobalsRunCount.mq5, we use a global variable to count the number of times it ran. The name of the variable is the name of the source file.

```
const string gv = __FILE__;

```

Recall that the built-in macro __FILE__ (see [Predefined constants](/en/book/basis/preprocessor/preprocessor_predefined)) is expanded by the compiler into the name of the compiled file, i.e., in this case, "GlobalsRunCount.mq5".

In the OnStart function, we will try to read the given global variable and save the result in the local count variable. If there was no global variable yet, we get 0, which is okay for us (we start counting from zero).

Before saving the value in count, it is necessary to typecast it to (int), since the GlobalVariableGet function returns double, and without the cast, the compiler generates a warning about potential data loss (it doesn't know that we plan to store only integers).

```
void OnStart()
{
   int count = (int)PRTF(GlobalVariableGet(gv));
   count++;
   PRTF(GlobalVariableSet(gv, count));
   Print("This script run count: ", count);
}

```

Then we increment the counter by 1 and write it back to the global variable with GlobalVariableSet. If we run the script several times, we will get something like the following log entries (your timestamps will be different):

```
GlobalVariableGet(gv)=0.0 / GLOBALVARIABLE_NOT_FOUND(4501)
GlobalVariableSet(gv,count)=2021.08.29 16:04:40 / ok
This script run count: 1
GlobalVariableGet(gv)=1.0 / ok
GlobalVariableSet(gv,count)=2021.08.29 16:05:00 / ok
This script run count: 2
GlobalVariableGet(gv)=2.0 / ok
GlobalVariableSet(gv,count)=2021.08.29 16:05:21 / ok
This script run count: 3

```

It is important to note that on the first run, we received a value of 0, and the internal error flag 4501 was generated. All subsequent calls are executed without problems since the variable exists (it can be seen in the "Global Variables" window of the terminal). Those who wish may close the terminal, restart it and execute the script again: the counter will continue to increase from the previous value.
