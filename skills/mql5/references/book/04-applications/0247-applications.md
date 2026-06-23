# Creating application programs in MQL5

In this part, we will closely study those sections of the API that are related to solving applied problems of algorithmic trading: analysis and processing of financial data, their visualization and markup using graphic objects, automation of routine actions, and interactive user interaction.

Let's start with the general principles of creating MQL programs, their types, features, and the event model in the terminal. Then we will touch on access to timeseries, work with charts and graphical objects. Finally, let's analyze the principles of creating and using each type of MQL program separately.

Active users of MetaTrader 5 undoubtedly remember that the terminal supports five types of programs:

- Technical indicators for calculating arbitrary indicators in the form of time series, with the possibility of their visualization in the main chart window, or in a separate panel (sub-window);
- Expert Advisors providing automatic or semi-automatic trading;
- Scripts for performing auxiliary one-time tasks on demand;
- Services for performing background tasks in continuous mode;
- Libraries, which are compiled modules with a specific, separate functionality, which are connected to other types of MQL programs during their loading, dynamically (which fundamentally distinguishes libraries from header files that are included statically at the compilation stage).

In the previous parts of the book, as we mastered the basics of programming and common built-in functions, we already had to turn to the implementation of scripts and services as examples. These types of programs were chosen as being simpler than the others. Now we will describe them purposefully and add more functional and popular indicators to them.

With the help of indicators and charts, we will learn some techniques that will be applicable to Expert Advisors as well. However, we will postpone the actual development of Expert Advisors, which is a more complex task in its essence, and move it to a separate, following Part 6, which includes not only automatic execution of orders and formalization of trading strategies, but also their backtesting and optimization.

As far as indicators are concerned, MetaTrader 5 is known to come with a set of built-in standard indicators. In this part, we will learn how to use them programmatically, as well as create our own indicators both from scratch, and based on other indicators.

All compiled indicators, Expert Advisors, scripts and services are displayed in the Navigator in MetaTrader 5. Libraries are not independent programs, and therefore do not have a dedicated branch in the hierarchy, although, of course, this would be convenient from the point of view of uniform management of all binary modules. As we will see later, those programs that depend on a particular library cannot run without it. But now you can check the existence of the library only in the file manager.

```
MQL5 Programming for Traders — Source Codes from the Book. Part 5

Examples from the book are also available in the public project \MQL5\Shared Projects\MQL5Book

```
