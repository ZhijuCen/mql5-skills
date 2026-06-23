# Forced test stop: TesterStop

If necessary, depending on the conditions observed, the developer can stop testing the Expert Advisor earlier. For example, this can be done when a specified number of losing deals or a drawdown level is reached. For this purpose, the API provides the TesterStop function.

void TesterStop()

The function gives a command to terminate the tester, i.e., the stop will occur only after the program returns control to the execution environment.

Calling TesterStop is considered a normal end of testing, and so this will call the [OnTester](/en/book/automation/tester/tester_ontester) function and return all accumulated trading statistics and the value of the optimization criterion to the strategy tester.

There is also an alternative regular way to interrupt testing: using the previously considered [ExpertRemove](/en/book/applications/runtime/runtime_remove) function. The call of ExpertRemove also returns trading statistics collected by the time the function is called. However, there are some differences.

As a result of the ExpertRemove call, the Expert Advisor is unloaded from the agent's memory. Therefore, if you need to run a new pass with a new set of parameters, some time will be taken to reload the MQL program. When using TesterStop, this does not happen, and this method is preferable in terms of performance.

On the other hand, the ExpertRemove call sets the [_IsStopped](/en/book/common/environment/env_stop) stop flag in the MQL program, which can be used in a standard way in different parts of the program for finalizing ("cleaning up" resources). But calling TesterStop does not set this flag, and therefore the developer may need to introduce their own global variable to indicate early termination and handle it in a specific way.

It is important to note that TesterStop is designed to stop only one pass of the tester.   

   

MQL5 does not provide functions for the early termination of optimization. Therefore, for example, if your Expert Advisor detects that the optimization has been launched on the wrong tick generation model, and this can be detected only after the optimization has been launched (OnTesterInit does not help here), then the TesterStop or ExpertRemove calls will interrupt new passes, but the passes themselves will continue to be initiated, generating mass null results. We will see it in the section [Big Expert Advisor example](/en/book/automation/tester/tester_example_ea), which will use protection from launching at open prices.   

   

It could be assumed that the ExpertRemove call in the Expert Advisor instance running in the terminal and actually serving an optimization manager would stop the optimization. But this is not the case. Even closing the chart with this Expert Advisor working in the frame mode does not stop the optimization.

It is suggested that you try these functions in action yourself.
