# Getting a list of global variables

Quite often, an MQL program is required to look through the existing global variables and select those meeting some criteria. For example, if a program uses part of a variable name to store textual information, then only the prefix is known in advance. The purpose of this prefix is to identify "its own" variable, and the "payload" attached to the prefix does not allow searching for a variable by the exact name.

The MQL5 API has two functions that allow you to enumerate global variables.

int GlobalVariablesTotal()

The function returns the total number of global variables.

string GlobalVariableName(int index)

The function returns the name of the global variable by its index number in the list of global variables. The index parameter with the number of the requested variable must be in the range from 0 to GlobalVariablesTotal() - 1.

In case of an error, the function will return NULL, and the error code can be obtained from the service variable _LastError or the [GetLastError](/en/book/common/environment/env_last_error) function.

Let's test this pair of functions using the script GlobalsList.mq5.

```
void OnStart()
{
   PRTF(GlobalVariableName(1000000));
   int n = PRTF(GlobalVariablesTotal());
   for(int i = 0; i < n; ++i)
   {
      const string name = GlobalVariableName(i);
      PrintFormat("%d %s=%f", i, name, GlobalVariableGet(name));
   }
}

```

The first string deliberately asks for the name of a variable with a large number, which, most likely, does not exist, and that fact should cause an error. Next, a request is made for the real number of variables and a loop through all of them, with the output of the name and value. The log below includes variables created by previous test scripts and one third-party variable.

```
GlobalVariableName(1000000)= / GLOBALVARIABLE_NOT_FOUND(4501)
GlobalVariablesTotal()=3 / ok
0 GlobalsRunCheck.mq5=3.000000
1 GlobalsRunCount.mq5=4.000000
2 abracadabra=0.000000

```

The order in which the terminal returns variables by an index is not defined.
