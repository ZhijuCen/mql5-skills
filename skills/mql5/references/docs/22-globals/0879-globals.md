# Global Variables of the Client Terminal

There is a group set of functions for working with global variables.

Global variables of the client terminal should not be mixed up with variables declared in the [global scope](/en/docs/basis/variables/global) of the mql5 program.

Global variables are kept in the client terminal for 4 weeks since the last access, then they will be deleted automatically. An access to a global variable is not only setting of a new value, but reading of the global variable value, as well.

Global variables of the client terminal are accessible simultaneously from all mql5 programs launched in the client terminal.

| Function | Action |
| --- | --- |
| GlobalVariableCheck | Checks the existence of a global variable with the specified name |
| GlobalVariableTime | Returns time of the last accessing the global variable |
| GlobalVariableDel | Deletes a global variable |
| GlobalVariableGet | Returns the value of a global variable |
| GlobalVariableName | Returns the name of a global variable by its ordinal number in the list of global variables |
| GlobalVariableSet | Sets the new value to a global variable |
| GlobalVariablesFlush | Forcibly saves contents of all global variables to a disk |
| GlobalVariableTemp | Sets the new value to a global variable, that exists only in the current session of the terminal |
| GlobalVariableSetOnCondition | Sets the new value of the existing global variable by condition |
| GlobalVariablesDeleteAll | Deletes global variables with the specified prefix in their names |
| GlobalVariablesTotal | Returns the total number of global variables |
