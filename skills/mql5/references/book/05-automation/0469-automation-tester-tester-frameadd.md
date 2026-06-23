# Sending data frames from agents to the terminal

MQL5 provides a group of functions for organizing the transfer and processing of your own (applied) optimization results, in addition to standard financial indicators and statistics. One of them, FrameAdd, is designed to send data from testing agents. Other functions are intended to receive data in the terminal.

The data exchange format is based on frames. This is a special internal structure that an Expert Advisor can fill in the tester based on an array of a simple type (which does not contain strings, class objects, or dynamic arrays) or using a file with a specified name (the file must first be created in the agent's sandbox). By calling the FrameAdd function multiple times, the Expert Advisor can send a series of frames to the terminal. There are no limits on the number of frames.

There are two versions of the FrameAdd function.

bool FrameAdd(const string name, ulong id, double value, const string filename)

bool FrameAdd(const string name, ulong id, double value, const void &data[])

The function adds a data frame to the buffer to be sent to the terminal. The name and id parameters are public labels that can be used to filter frames in the [FrameFilter](/en/book/automation/tester/tester_framenext) function. The value parameter allows you to pass an arbitrary numeric value that can be used when one value is enough. More bulky data is indicated either in the data array (may be an array of simple structures) or in a file named filename.

If there is no bulk data to transfer (for example, you only need to transfer the status of the process), use the first form of the function and specify NULL instead of a string with the file name or the second form with a dummy array of zero size.

The function returns true in case of success.

The function can only be called in the OnTester handler.

The function has no effect when called during a simple test, that is, outside of optimization.

You can send data only from agents to the terminal. There are no mechanisms in MQL5 for sending data in the opposite direction during optimization. All data that the Expert Advisor wants to send to agents must be prepared and available (in the form of input parameters or files connected by [directives](/en/book/automation/tester/tester_directives)) before starting the optimization.

We will look at an example of using FrameAdd after we get familiar with the functions of the host in the next section.
