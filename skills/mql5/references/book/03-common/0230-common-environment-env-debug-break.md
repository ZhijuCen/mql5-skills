# Debug management

The built-in debugger in MetaEditor allows setting breakpoints in the source code, which are the lines on which the program execution should be suspended. Sometimes this system fails, i.e., the pause does not work, and then you can use the DebugBreak function explicitly enforces the stop.

void DebugBreak()

Calling the function pauses the program and activates the editor window in the debug mode, with all the tools for viewing variables and the call stack and for continuing further execution step by step.

Program execution is interrupted only if the program is launched from the editor in the debug mode (by commands Debug -> Start on Real Data or Start in History Data). In all other modes, including regular launch (in the terminal) and profiling, the function has no effect.
