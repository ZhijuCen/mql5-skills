# Working with Optimization Results

Functions for organizing custom processing of the optimization results in the strategy tester. They can be called during optimization in testing agents, as well as locally in Expert Advisors and scripts.

When you run an Expert Advisor in the strategy tester, you can create your own data array based on the simple types or [simple structures](/en/docs/basis/types/classes#simple_structure) (they do not contain strings, class objects or objects of dynamic arrays). This data set can be saved using the [FrameAdd()](/en/docs/optimization_frames/frameadd) function in a special structure called a frame. During the optimization of an Expert Advisor, each agent can send a series of frames to the terminal. All the received frames are written in the *.MQD file named as the Expert Advisor in the terminal_directory\MQL5\Files\Tester folder. They are written in the order they are received from the agents. Receipt of a frame in the client terminal from a testing agent generates the [TesterPass](/en/docs/runtime/event_fire#testerpass) event.

Frames can be stored in the computer memory and in a file with the specified name. The MQL5 language sets no limitations on the number of frames.

### Memory and disk space limits in MQL5 Cloud Network

The following limitation applies to optimizations run in the [MQL5 Cloud Network](https://www.metatrader5.com/en/terminal/help/algotrading/strategy_optimization#cloud_start): the Expert Advisor must not write to disk more than 4GB of information or use more than 4GB of RAM. If the limit is exceeded, the network agent will not be able to complete the calculation correctly, and you will not receive the result. However, you will be charged for all the time spent on the calculations.

If you need to get information from each optimization pass, [send frames](/en/docs/optimization_frames) without writing to disk. To avoid using [file operations](/en/docs/files) in Expert Advisors during calculations in the MQL5 Cloud Network, you can use the following check:

```
   int handle=INVALID_HANDLE;
   bool file_operations_allowed=true;
   if(MQLInfoInteger(MQL_OPTIMIZATION) || MQLInfoInteger(MQL_FORWARD))
      file_operations_allowed=false;
 
   if(file_operations_allowed)
     {
      ...
      handle=FileOpen(...);
      ...
     }

```

| Function | Action |
| --- | --- |
| FrameFirst | Moves a pointer of frame reading to the beginning and resets the previously set filter |
| FrameFilter | Sets the frame reading filter and moves the pointer to the beginning |
| FrameNext | Reads a frame and moves the pointer to the next one |
| FrameInputs | Receives  input parameters , on which the frame is formed |
| FrameAdd | Adds a frame with data |
| ParameterGetRange | Receives data on the values range and the change step for an  input variable  when optimizing an Expert Advisor in the Strategy Tester |
| ParameterSetRange | Specifies the use of  input variable  when optimizing an Expert Advisor in the Strategy Tester: value, change step, initial and final values |

See also

[Testing Statistics](/en/docs/constants/environment_state/statistics), [Properties of a Running MQL5 Program](/en/docs/constants/environment_state/mql5_programm_info)
