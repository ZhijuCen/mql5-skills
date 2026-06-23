# Programmatic removal of Expert Advisors and scripts: ExpertRemove

If necessary, the developer can organize the stopping and unloading of MQL programs of two types: Expert Advisors and scripts. This is done using the ExpertRemove function.

void ExpertRemove()

The function has no parameters and does not return a value. It sends a request to the MQL program execution environment to delete the current program. In fact, this leads to setting the [_StopFlag](/en/book/common/environment/env_stop) flag and stopping the reception (and processing) of all subsequent events. After that, the program is given 3 seconds to properly complete its work: release resources, break loops in algorithms, etc. If the program does not do this, it will be unloaded forcibly, with the loss of intermediate data.

This function does not work in indicators and services (the program continues to run).

For each function call, the log will contain the entry "ExpertRemove() function called".

The function is primarily used in Expert Advisors that cannot be interrupted in any other way. In the case of scripts, it is usually easier to break the loop (if there is one) with the [break](/en/book/basis/statements/statements_break) statement. But if the loops are nested, or the algorithm uses many function calls from one another, it is easier to take into account the stop flag at different levels in the conditions for continuing calculations, and in case of an erroneous situation, set this flag using ExpertRemove. If you do not use this built-in flag, in any case, you would have to introduce a global variable of the same purpose.

The script ScriptRemove.mq5 provides the ExpertRemove usage example.

A potential problem in the operation of the algorithm, which leads to the need to unload the script, is emulated by the ProblemSource class. ExpertRemove is randomly called in its constructor.

```
class ProblemSource
{
public:
   ProblemSource()
   {
      // simulating a problem during object creation, for example,
      // with the capture of some resources, such as a file, etc.
      if(rand() > 20000)
      {
         ExpertRemove(); // will set _StopFlag to true
      }
   }
};

```

Further along, objects of this class are created at the global level and inside the helper function.

```
ProblemSource global; // object may throw an error
   
void SubFunction()
{
   ProblemSource local; //object may throw an error
   // simulate some work (we need to check the integrity of the object!)
   Sleep(1000);
}

```

Now we use SubFunction in the OnStart operation, inside the loop with the IsStopped condition.

```
void OnStart()
{
   int count = 0;
   // loop until stopped by the user or the program itself
   while(!IsStopped())
   {
      SubFunction();
      Print(++count);
   }
}

```

Here is a log example (each run will be different due to randomness):

```
1
2
3
ExpertRemove() function called
4

```

Note that if an error occurs while creating the global object, the loop will never execute.

Because Exert Advisors can run in the [tester](/en/book/automation/tester), the ExpertRemove function can also be used in the tester. Its effect depends on the place of the function call. If this is done inside the [OnInit](/en/book/applications/runtime/runtime_oninit_ondeinit) handler, the function will cancel testing, that is, one run of the tester on the current set of the Expert Advisor parameters. Such termination is treated as an initialization error. When ExpertRemove is called in any other place of the algorithm, the Expert Advisor testing will be interrupted early, but will be processed in a regular way, with [OnDeinit](/en/book/applications/runtime/runtime_oninit_ondeinit) and [OnTester](/en/book/automation/tester/tester_ontester) calls. In this case, the accumulated trading statistics and the value of the optimization criterion will be obtained, taking into account that the emulated server time [TimeCurrent](/en/book/common/timing/timing_local_server) does not reach the end date in the tester settings.
