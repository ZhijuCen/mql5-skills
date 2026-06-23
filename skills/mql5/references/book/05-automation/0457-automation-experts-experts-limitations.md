# Limitations and benefits of Expert Advisors

Due to their specific operation, Expert Advisors have some limitations, as well as advantages over other types of MQL programs. In particular, all functions intended for indicators are banned in Expert Advisors:

- [SetIndexBuffer](/en/book/applications/indicators_make/indicators_setindexbuffer)
- [IndicatorSetDouble](/en/book/applications/indicators_make/indicators_separate_window)
- [IndicatorSetInteger](/en/book/applications/indicators_make/indicators_separate_window)
- [IndicatorSetString](/en/book/applications/indicators_make/indicators_separate_window)
- [PlotIndexSetDouble](/en/book/applications/indicators_make/indicators_empty_value)
- [PlotIndexSetInteger](/en/book/applications/indicators_make/indicators_plotindexsetinteger)
- [PlotIndexSetString](/en/book/applications/indicators_make/indicators_labels)
- [PlotIndexGetInteger](/en/book/applications/indicators_make/indicators_plotindexsetinteger)

Also, Expert Advisors should not describe event handlers that are typical for other types of programs: OnStart (scripts and services) and OnCalculate (indicators).

Unlike indicators, only one Expert Advisor can be placed on each chart.

At the same time, Expert Advisors are the only type of MQL programs that in addition to testing (which we have already done for both indicators and Expert Advisors), can also be optimized. The optimizer allows finding the best input parameters according to various criteria, both trading and abstract mathematical ones. For these purposes, the API includes additional functions and several specific event handlers. We will study this material in the next chapter.

In addition, groups of built-in MQL5 functions for working with the network at the socket level and various Internet protocols (HTTP, FTP, SMTP) are available in Expert Advisors (as well as in scripts and services, that is, in all types of programs except indicators). We will consider them in the seventh part of the book.
