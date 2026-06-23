# Working with charts

Most MQL programs, such as scripts, indicators, and Expert Advisors, are executed on charts. Only services run in the background, without being tied to a schedule. A rich set of functions is provided for obtaining and changing the properties of graphs, analyzing their list, and searching for other running programs.

Since charts are the natural environment for indicators, we have already had a chance to get acquainted with some of these features in the previous indicator chapters. In this chapter, we will study all these functions in a targeted manner.

When working with charts, we will use the concept of a window. A window is a dedicated area that displays price charts and/or indicator charts. The top and, as a rule, the largest window contains price charts, has the number 0, and always exists. All additional windows added to the lower part when placing indicators are numbered from 1 and higher (numbering from top to bottom). Each subwindow exists only as long as it has at least one indicator.

Since the user can delete all indicators in an arbitrary subwindow, including the one that is not the last (the lowest), the indexes of the remaining subwindows can decrease.

The event model of charts related to receiving and processing notifications about events on charts and generating custom events will be discussed in a [separate chapter](/en/book/applications/events).

In addition to the "charts in windows" discussed here, MetaTrader 5 also allows you to create "charts in objects". We will deal with [graphical objects](/en/book/applications/objects) in the next chapter.
