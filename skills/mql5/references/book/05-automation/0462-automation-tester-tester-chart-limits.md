# Testing visualization: chart, objects, indicators

The tester allows testing in two different ways: with and without visualization. The method is selected by choosing a corresponding option on the main settings tab of the tester.

When visualization is enabled, the tester opens a separate window in which it reproduces trading operations and displays indicators and objects. Though it is visual, we don't need to see it for every case, but only for programs with a user interface (for example, trading panels or controlled markup made by graphical objects). For other Expert Advisors, only the execution of the algorithm according to the established strategy is important. This can be checked without visualization, which can significantly speed up the process. By the way, it is in this mode that test runs are made during optimization.

During such "background" testing and optimization, no graphical objects are built. Therefore, when accessing the properties of objects, the Expert Advisor will receive zero values. Thus, you can check the work with objects and the chart only when testing in the visual mode.

Previously, in the [Testing indicators](/en/book/applications/indicators_make/indicators_test) section, we have seen the specific behavior of indicators in the tester. To increase the efficiency of non-visual testing and optimization of Expert Advisors (using indicators), indicators can be calculated not on every tick, but only when we request data from them. Recalculation on each tick occurs only if there are EventChartCustom, OnChartEvent, OnTimer functions or tester_everytick_calculate directives in the indicator (see [Preprocessor directives for the tester](/en/book/automation/tester/tester_directives)). In the visual tester window online indicators always receive OnCalculate events on every tick.

If testing is carried out in a non-visual mode, after its completion, the symbol chart automatically opens in the terminal, which displays completed deals and indicators that were used in the Expert Advisor. This helps to correlate the market entry and exit moments with indicator values. However, here we mean only indicators that work on the symbol and timeframe of testing. If the Expert Advisor created indicators on other symbols or timeframes, they will not be shown.

It is important to note that the indicators displayed on the chart automatically opened after testing is completed are recalculated after the end of testing. This happens even if these indicators were used in the tested Expert Advisor and were previously calculated "on the go", as the bars were forming.

In some cases, the programmer may need to hide information about which indicators are used in the trading algorithm, and therefore their visualization on the chart is undesirable. The [IndicatorRelease](/en/book/applications/indicators_use/indicators_indicatorrelease) function can be used for this.

The IndicatorRelease function is originally intended to release the calculated part of the indicator if it is no longer needed. This saves memory and processor resources. Its second purpose is to prohibit the display of the indicator on the testing chart after completing a single run.

To disable the display of the indicator on the chart at the end of testing, just call IndicatorRelease with the indicator handle in the OnDeinit handler. The OnDeinit function is always called in Expert Advisors after completion and before displaying the test chart. Neither OnDeinit nor the destructors of global and static objects are called in the indicators themselves in the tester — this is what the developers of MetaTrader 5 agreed on.

In addition, the MQL5 API includes a special function [TesterHideIndicators](/en/book/automation/tester/tester_testerhideindicators) with a similar purpose, which we will consider later.

At the same time, it should be taken into account that tpl templates (if they are created) can additionally influence the external representation of the testing graph.

So if there is a tester.tpl template in the MQL5/Profiles/Templates directory, it will be applied to the opened chart. If the Expert Advisor used other indicators in its work and did not prohibit their display, then the indicators from the template and from the Expert Advisor will be combined on the chart.

When tester.tpl is absent, the default template (default.tpl) is applied.

If the MQL5/Profiles/Templates folder contains a tpl template with the same name as the Expert Advisor (for example, ExpertMACD.tpl), then during visual testing or on the chart opened after testing, only indicators from this template will be shown. In this case, no indicators used in the tested Expert Advisor will be shown.
