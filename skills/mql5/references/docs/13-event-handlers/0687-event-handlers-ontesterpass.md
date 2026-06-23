# OnTesterPass

The function is called in EAs when the [TesterPass](/en/docs/runtime/event_fire#testerpass) event occurs for handling a new data frame during EA optimization.

```
void  OnTesterPass(void);

```

Return Value

No return value

Note

The [TesterPass](/en/docs/runtime/event_fire#testerpass) event is generated automatically when receiving a frame during an Expert Advisor optimization in the strategy tester.

An EA having OnTesterDeInit() or OnTesterPass() event handler is automatically downloaded on a separate terminal chart during the optimization start. It has the symbol and the period that have been specified in the tester. The function is meant for handling frames received from test agents during optimization. The frame containing test results should be sent from the [OnTester()](/en/docs/event_handlers/ontester) handler using the [FrameAdd()](/en/docs/optimization_frames/frameadd) function.

Keep in mind that optimization frames sent by test agents using the [FrameAdd()](/en/docs/optimization_frames/frameadd) function may come in bundles and take time to deliver. Therefore, not all frames, as well as [TesterPass](/en/docs/runtime/event_fire#testerpass) events, may arrive and be processed in [OnTesterPass()](/en/docs/event_handlers/ontesterpass) before the end of optimization. If you want to receive all belated frames in OnTesterDeinit(), place the code block using the [FrameNext()](/en/docs/optimization_frames/framenext) function.

After completing OnTesterDeinit() optimization, it is possible to sort all received frames again using the [FrameFirst()](/en/docs/optimization_frames/framefirst)/[FrameFilter](/en/docs/optimization_frames/framefilter) and [FrameNext()](/en/docs/optimization_frames/framenext) functions.

See also

[Testing trading strategies](/en/docs/runtime/testing), [Working with optimization results](/en/docs/optimization_frames), [OnTesterInit](/en/docs/event_handlers/ontesterinit), [OnTesterDeinit](/en/docs/event_handlers/ontesterdeinit), [FrameFirst](/en/docs/optimization_frames/framefirst), [FrameFilter](/en/docs/optimization_frames/framefilter), [FrameNext](/en/docs/optimization_frames/framenext), [FrameInputs](/en/docs/optimization_frames/frameinputs)
