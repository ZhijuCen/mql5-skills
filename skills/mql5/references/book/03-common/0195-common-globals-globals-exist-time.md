# Checking the existence and last activity time

As we saw in the previous section, you can check the existence of a global variable by trying to read its value: if this does not result in an error code in _LastError, then the global variable exists, and we have already obtained its value and can use it in the algorithm. However, if under some conditions you only need to check for the existence, but not read the global variable, it is more convenient to use another function specifically designed for this: GlobalVariableCheck.

There is another way to check, namely, using the GlobalVariableTime function. As its name implies, it allows you to find out the last time a variable was used. But if the variable does not exist, then the time of its use is absent, i.e., it is equal to 0.

bool GlobalVariableCheck(const string name)

The function checks for the existence of a global variable with the specified name and returns the result: true (the variable exists) or false (no variable).

datetime GlobalVariableTime(const string name)

The function returns the time the global variable with the specified name was last used. The fact of use can be represented by the modification or reading of the variable value.

Checking for the variable existence with GlobalVariableCheck or getting its time through GlobalVariableTime do not change the time of use.

In the script GlobalsRunCheck.mq5, we will slightly supplement the code from GlobalsRunCount.mq5 so that at the very beginning of the function OnStart check for the presence of a variable and the time of its use.

```
void OnStart()
{
   PRTF(GlobalVariableCheck(gv));
   PRTF(GlobalVariableTime(gv));
   ...

```

The code below is unchanged. Meanwhile, note that the gv variable defined via __FILE__ will this time contain the new script name "GlobalsRunCheck.mq5" as the name of the global variable (i.e., each script has its own global counter).

All runs except the very first one will show true from the GlobalVariableCheck function (the variable exists) and the time of the variable from the previous run. Here is an example log:

```
GlobalVariableCheck(gv)=false / ok
GlobalVariableTime(gv)=1970.01.01 00:00:00 / GLOBALVARIABLE_NOT_FOUND(4501)
GlobalVariableGet(gv)=0.0 / GLOBALVARIABLE_NOT_FOUND(4501)
GlobalVariableSet(gv,count)=2021.08.29 16:59:35 / ok
This script run count: 1
GlobalVariableCheck(gv)=true / ok
GlobalVariableTime(gv)=2021.08.29 16:59:35 / ok
GlobalVariableGet(gv)=1.0 / ok
GlobalVariableSet(gv,count)=2021.08.29 16:59:45 / ok
This script run count: 2
GlobalVariableCheck(gv)=true / ok
GlobalVariableTime(gv)=2021.08.29 16:59:45 / ok
GlobalVariableGet(gv)=2.0 / ok
GlobalVariableSet(gv,count)=2021.08.29 16:59:56 / ok
This script run count: 3

```
