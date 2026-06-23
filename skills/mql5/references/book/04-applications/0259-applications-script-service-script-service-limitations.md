# Restrictions for scripts and services

All functions included in the group for working with indicators are prohibited in scripts and service. These functions will be described in the corresponding [chapter](/en/book/applications/indicators_make):

- [SetIndexBuffer](/en/book/applications/indicators_make/indicators_setindexbuffer)
- [IndicatorSetDouble](/en/book/applications/indicators_make/indicators_separate_window)
- [IndicatorSetInteger](/en/book/applications/indicators_make/indicators_separate_window)
- [IndicatorSetString](/en/book/applications/indicators_make/indicators_separate_window)
- [PlotIndexSetDouble](/en/book/applications/indicators_make/indicators_empty_value)
- [PlotIndexSetInteger](/en/book/applications/indicators_make/indicators_plotindexsetinteger)
- [PlotIndexSetString](/en/book/applications/indicators_make/indicators_labels)
- [PlotIndexGetInteger](/en/book/applications/indicators_make/indicators_plotindexsetinteger)

Also, in scripts and services, there is no point to use the OnTimer handler (like any other handlers) and [timer](/en/book/applications/timer) functions:

- [EventSetMillisecondTimer](/en/book/applications/timer/timer_event_set_millisecond)
- [EventSetTimer](/en/book/applications/timer/timer_event_set)
- [EventKillTimer](/en/book/applications/timer/timer_event_set)

Since scripts and services are not supported by the tester, they cannot use [Tester](/en/book/automation/tester)[ functions](/en/book/automation/tester); they will cause errors ERR_FUNCTION_NOT_ALLOWED (4014).
