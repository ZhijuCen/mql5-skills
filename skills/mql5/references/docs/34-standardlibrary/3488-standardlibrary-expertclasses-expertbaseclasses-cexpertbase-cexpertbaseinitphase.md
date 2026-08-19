# InitPhase

Gets the current phase of the object initialization.

```
ENUM_INIT_PHASE  InitPhase()

```

Return Value

Current phase of the object initialization.

Note

The object initialization consist of several phases:

1. Start initialization.

- start              - after finish of the constructor  

   - finish             - after successful completion of the [Init(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbaseinit) method.  

   - allowed          - call of the [Init(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbaseinit) method  

   - not allowed    - call of the [ValidationSettings()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbasevalidationsettings) method and other initialization methods

2. Parameters setting phase. In this phase you need to set all the object parameters, used for creation of indicators.

- start             - after successful completion of the [Init(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbaseinit) method  

   - finish            - after successful completion of the [ValidationSettings()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbasevalidationsettings) method  

   - allowed         - call of [Symbol(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbasesymbol) and [Period(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbaseperiod) methods  

   - not allowed   - call of the [Init(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbaseinit), [SetPriceSeries(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbasesetpriceseries), [SetOtherSeries(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbasesetotherseries) and [InitIndicators(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbaseinitindicators) methods

3. Checking of parameters.

- start             - after successful completion of the [ValidationSettings()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbasevalidationsettings) method  

   - finish            - after successful completion of the [InitIndicators(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbaseinitindicators) method  

   - allowed         - call of the [Symbol(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbasesymbol), [Period(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbaseperiod) and [InitIndicators(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbaseinitindicators) methods  

   - not allowed   - call of any other initialization methods

4. Finish of initialization.

- start             - after successful completion of the [InitIndicators(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbaseinitindicators) method  

   - not allowed    - call of initialization methods
