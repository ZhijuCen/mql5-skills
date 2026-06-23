# Limitations of functions in the tester

When using the tester, you should take into account some restrictions imposed on built-in functions. Some of the MQL5 API functions are never executed in the strategy tester and some work only in single passes but not during optimization.

So, to increase performance when optimizing Expert Advisors, the [Comment](/en/book/common/output/output_comment), [Print](/en/book/common/output/output_print), and [PrintFormat](/en/book/common/output/output_print) functions are not executed.

The exception is the use of these functions inside the OnInit handler which is done to make it easier to find possible causes of initialization errors.

Functions that provide interaction with the "world" are not executed in the strategy tester. These include [MessageBox](/en/book/common/output/output_messagebox), [PlaySound](/en/book/common/output/output_sound), [SendFTP](/en/book/advanced/network/network_ftp), [SendMail](/en/book/advanced/network/network_email), [SendNotification](/en/book/advanced/network/network_push), [WebRequest](/en/book/advanced/network/network_http), and functions for working with [sockets](/en/book/advanced/network/network_socket_create_connect).

In addition, many functions for working with charts and objects have no effect. In particular, you will not be able to change the symbol or period of the current chart by calling [ChartSetSymbolPeriod](/en/book/applications/charts/charts_set_symbol_period), list all indicators (including subordinate ones) with [ChartIndicatorGet](/en/book/applications/charts/charts_indicators), work with templates [ChartSaveTemplate](/en/book/applications/charts/charts_tpl), and so on.

In the tester, even in the visual mode, interactive chart, object, keyboard and mouse events are not generated for the [OnChartEvent](/en/book/applications/events/events_onchartevent) handler.
