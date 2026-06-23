# Alerts

In this section, the signal will mean the Alert function to issue warnings to the terminal user.

The term "alert" has multiple meanings in MetaTrader 5. There are 2 contexts in which it is used:

- User-configurable (manually) alerts in the Alerts tab in the Toolbox panel. Using them, you can track the triggering of simple conditions for exceeding the set values by price, volume or time, and issue notifications in various ways.
- Program "alerts" generated from the MQL code by the Alert function. They have nothing to do with the previous ones.

void Alert(argument, ...)

The function displays a message in a non-modal dialog box, accompanied by a standard sound signal (according to the selection in the Options dialog, on the tab Events, in the terminal). If the window is hidden, it will be shown on top of the main terminal window (it can then be closed, minimized, or moved away while continuing to work with the main window). The message is also added to the Expert log, marked as "Alert".

There is no command in the MetaTrader 5 interface to manually open the alert window if it was previously closed. To see the list of warnings again (in its pure form, without the need to filter the log), you will need to generate a new signal somehow.

Passing arguments, displaying information and the general principles of the function are exactly the same as what was stated for the [Print](/en/book/common/output/output_print) function.

Demonstration of the Alert function with a screenshot was shown in the introductory greetings example in the first chapter, in the section [Data output](/en/book/intro/a_data_output).

Use Alert instead of Print in cases where it is necessary to draw the user's attention to the displayed information. However, it should not be abused, since the frequent appearance of the window can hinder the user's work, force them to ignore messages or stop the MQL program. Provide an algorithm in your program to limit the frequency of possible message generation.
