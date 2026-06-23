# Temporary global variables

In the global variables subsystem of the terminal, it is possible to make some variables temporary: they are stored only in memory and are not written to disk when the terminal is closed.

Due to their specific nature, temporary global variables are used exclusively for data exchange between MQL programs and are not suitable for saving states between MetaTrader 5 launches. One of the most obvious uses for temporary variables is various metrics of operational activity (for example, counters of running program copies) that should be dynamically recalculated on every startup, rather than being restored from disk.

A global variable should be declared temporary in advance, before assigning any value to it, using the function GlobalVariableTemp.

Unfortunately, it is impossible to find out by the name of a global variable whether it is temporary: MQL5 does not provide means for this.

Temporary variables can only be created using MQL programs. Temporary variables are displayed in the "Global Variables" window along with ordinary (persistent) global variables, but the user does not have the ability to add their own temporary variable from the GUI.

bool GlobalVariableTemp(const string name)

The function creates a new global variable with the specified name, which will exist only until the end of the current terminal session.

If a variable with the same name already exists, it will not be converted to a temporary variable.

However, if a variable does not exist yet, it will get the value 0. After that, you can work with it as usual, in particular, assign other values using the GlobalVariableSet function.

We will show an example of this function along with the functions of the next section.
