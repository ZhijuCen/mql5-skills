# Two types of indicators: for main window and subwindow

As you know, indicators in MetaTrader 5 can display their lines in two places: in the main chart window on top of the quotes or in a separate window created below the price chart. These two modes are mutually exclusive: each indicator is designed either for the main window or for a subwindow, but cannot combine both methods.

There are several alternative solutions for the cases when the program is required to visualize data in both windows. For example, a project can be implemented in the form of two interacting indicators (the technical side of the interaction remains open: these can be [resources](/en/book/advanced/resources), [files](/en/book/common/files), [DBMS](/en/book/advanced/sqlite), or shared memory accessed via a DLL). Another approach involves using indicator buffers in one of the windows, for example, in the bottom panel, and performing visualization on the main chart using [graphic objects](/en/book/applications/objects).

Multiple indicators can be applied both in the main window and in the subwindow. If the indicator is designed to work in a separate window, then dragging it with the mouse from the Navigator to the main window will automatically create a new window for this indicator. However, if the window already has a subwindow with another indicator, then the new one can be dragged to the same place, thereby aligning two or more indicators. In this case, various modes of scaling indicators in one window are possible. By default, the constructions of each indicator are scaled automatically and independently of each other to the full height of the panel, but this can be changed (see example SubScaler.mq5 in the [section about keyboard events](/en/book/applications/events/events_keyboard)).

The indicator display window is selected using one of two compilation directives.

```
#property indicator_chart_window     // display the indicator in the chart window
#property indicator_separate_window  // display the indicator in a separate window

```

The indicator developer should insert one of them at the beginning of the source code. If none of the directives is present, the default option will output it to the main window, but the compiler will generate a warning. We saw this in the previous section. In the following examples, we will be sure to indicate #property indicator_chart_window or #property indicator_separate_window.

Second compilation warning IndStub.mq5 concerned the missing buffers and charts setting. We will deal with them in the next section.

The action of the Apply to dropdown list in the indicator settings depends on the window it was designed for.  

   

An indicator for an individual window can be Applied to the indicator in the subwindow, but not to the indicator in the main window.  

   

However, the indicator for the main window can be Applied to any indicator, both to the one in the main window and in the subwindow.
