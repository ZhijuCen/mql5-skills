# MQL program execution environment

As we know, the source texts of an MQL program after compilation into a binary executable code in the format ex5 are ready to work in the terminal or on test agents. Thus, a terminal or a tester provides a common environment within which MQL programs "live".

Recall that the built-in tester supports only 2 types of MQL programs: Expert Advisors and indicators. We will talk in detail about the types of MQL programs and their features in the fifth part of the book. Meanwhile, in this chapter, we will focus on those MQL5 API functions that are common to all types, and allow you to analyze the execution environment and, to some extent, control it.

Most environment properties are read-only through functions TerminalInfoInteger, TerminalInfoDouble, TerminalInfoString, MQLInfoInteger, and MQLInfoString. From the names you can understand that each function returns values of a certain type. Such an architecture leads to the fact that the applied meaning of the properties combined in one function can be very different. Another grouping can be provided by the implementation of your own object layer in MQL5 (an example will be given a little later, in the section on using [properties for binding to the program environment](/en/book/common/environment/env_signature)).

The specified set of functions has an explicit logical division into general terminal properties (with the "Terminal" prefix) and properties of a separate MQL program (with the "MQL" prefix). However, in many cases, it is required to jointly analyze the similar characteristics of both the terminal and the program. For example, permissions to use a DLL, or perform trading operations are issued both to the terminal as a whole and to a specific program. That is why it makes sense to consider the functions from this in a complex, as a whole.

Only some of the environment properties associated with error codes are writable, in particular, resetting a previous error (ResetLastError) and setting a user error (SetUserError).

Also in this chapter, we will look at the functions for closing the terminal within a program (TerminalClose, SetReturnError) and pausing the program in the debugger (Debug Break).
