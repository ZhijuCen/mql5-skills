# OnTesterDeinit

The function is called in EAs when the [TesterDeinit](/en/docs/runtime/event_fire#testerdeinit) event occurs after EA optimization.

```
void  OnTesterDeinit(void);

```

Return Value

No return value

Note

The [TesterDeinit](/en/docs/runtime/event_fire#testerdeinit) event is generated after the end of EA optimization in the strategy tester.

An EA having OnTesterDeInit() or OnTesterPass() event handler is automatically downloaded on a separate terminal chart during the optimization start. It has the symbol and the period that have been specified in the tester. The function is designed for the final processing of all [optimization results](/en/docs/optimization_frames).

Keep in mind that optimization frames sent by test agents using the [FrameAdd()](/en/docs/optimization_frames/frameadd) function may come in bundles and take time to deliver. Therefore, not all frames, as well as [TesterPass](/en/docs/runtime/event_fire#testerpass) events, may arrive and be processed in [OnTesterPass()](/en/docs/event_handlers/ontesterpass) before the end of optimization. If you want to receive all belated frames in OnTesterDeinit(), place the code block using the [FrameNext()](/en/docs/optimization_frames/framenext) function.

See also

[Testing trading strategies](/en/docs/runtime/testing), [Working with optimization results](/en/docs/optimization_frames), [TesterStatistics](/en/docs/common/testerstatistics), [OnTesterInit](/en/docs/event_handlers/ontesterinit), [OnTesterPass](/en/docs/event_handlers/ontesterpass), [ParameterGetRange](/en/docs/optimization_frames/parametergetrange), [ParameterSetRange](/en/docs/optimization_frames/parametersetrange)
