# Deleting global variables

If necessary, an MQL program can delete a global variable or a group of them that has become redundant. The list of global variables consumes some computer resources, and the good programming style suggests that resources should be freed whenever possible.

bool GlobalVariableDel(const string name)

The function removes the 'name' global variable. On success, the function returns true, otherwise returns false.

int GlobalVariablesDeleteAll(const string prefix = NULL, datetime limit = 0)

The function deletes global variables with the specified prefix in the name and with a usage time older than the limit parameter value.

If the NULL prefix (default) or an empty string is specified, then all global variables that also match the deletion criterion by date (if it's set) fall under the deletion criterion.

If the limit parameter is zero (default), then global variables with any date taking into account the prefix are deleted.

If both parameters are specified, then global variables that match both, the prefix and the time criterion, are deleted.

Be careful: calling GlobalVariablesDeleteAll without parameters will remove all variables.

The function returns the number of deleted variables.

Consider the script GlobalsDelete.mq5, exploiting two new features.

```
void OnStart()
{
   PRTF(GlobalVariableDel("#123%"));
   PRTF(GlobalVariablesDeleteAll("#123%"));
   ...

```

In the beginning, an attempt is made to delete non-existent global variables by their exact name and prefix. Both have no effect on existing variables.

Calling GlobalVariablesDeleteAll with a filter by time in the past (more than 4 weeks ago) also has a zero result, because the terminal deletes such old variables automatically (such variables cannot exist).

```
   PRTF(GlobalVariablesDeleteAll(NULL, D'2021.01.01'));

```

Then, we create a variable with the name "abracadabra" (if it did not exist) and immediately delete it. These calls should succeed.

```
   PRTF(GlobalVariableSet(abracadabra, 0));
   PRTF(GlobalVariableDel(abracadabra));

```

Finally, let's delete the variables starting with the "GlobalsRun" prefix: they should have been created by the test scripts from the two previous sections on file names (respectively, "GlobalsRunCount.mq5" and "GlobalsRunCheck.mq5").

```
   PRTF(GlobalVariablesDeleteAll("GlobalsRun"));
   PRTF(GlobalVariablesTotal());
}

```

The script should output something like the following set of strings to the log (some indicators depend on external conditions and startup time).

```
GlobalVariableDel(#123%)=false / GLOBALVARIABLE_NOT_FOUND(4501)
GlobalVariablesDeleteAll(#123%)=0 / ok
GlobalVariablesDeleteAll(NULL,D'2021.01.01')=0 / ok
GlobalVariableSet(abracadabra,0)=2021.08.30 14:02:32 / ok
GlobalVariableDel(abracadabra)=true / ok
GlobalVariablesDeleteAll(GlobalsRun)=2 / ok
GlobalVariablesTotal()=0 / ok

```

In the end, we printed out the total number of remaining global variables (in this case, we got 0, i.e., there are no variables). It may differ for you if the global variables were created by other MQL programs or by the user.
