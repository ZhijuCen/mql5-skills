# Creating Expert Advisors

In this chapter, we begin to study the MQL5 trading API used to implement Expert Advisors. This type of program is perhaps the most complex and demanding in terms of error-free coding and the number and variety of technologies involved. In particular, we will need to utilize many of the skills acquired from the previous chapters, ranging from OOP to the applied aspects of working with graphical objects, indicators, symbols, and software environment settings.

Depending on the chosen trading strategy, the Expert Advisor developer may need to pay special attention to the following:

- Decision-making and order-sending speed (for HFT, High-Frequency Trading)
- Selecting the optimal portfolio of instruments based on their correlations and volatility (for cluster trading)
- Dynamically calculating lots and distance between orders (for martingale and grid strategies)
- Analysis of news or external data sources (this will be discussed in the 7th part of the book)

All such features should be optimally applied by the developer to the described trading mechanisms provided by the MQL5 API.

Next, we will consider in detail built-in functions for managing trading activity, the Expert Advisor event model, and specific data structures, and recall the basic principles of interaction between the terminal and the server, as well as the basic concepts for algorithmic trading in MetaTrader 5: order, deal, and position.

At the same time, due to the versatility of the material, many important nuances of Expert Advisor development, such as testing and optimization, are highlighted in the next chapter.

We have previously considered the [Design of MQL programs of various types](/en/book/applications/runtime/runtime_features_by_progtype), including Expert Advisors, as well as started [Features of starting and stopping programs](/en/book/applications/runtime/runtime_lifecycle). Despite the fact that an Expert Advisor is launched on a specific chart, for which a working symbol is defined, there are no obstacles to centrally manage trading of an arbitrary set of financial instruments. Such Expert Advisors are traditionally referred to as multicurrency, although in fact, their portfolio may include CFDs, stocks, commodities, and tickers of other markets.

In Expert Advisors, as well as in indicators, there are [Key events ](/en/book/applications/runtime/runtime_oninit_ondeinit)[OnInit](/en/book/applications/runtime/runtime_oninit_ondeinit)[ and ](/en/book/applications/runtime/runtime_oninit_ondeinit)[OnDeinit](/en/book/applications/runtime/runtime_oninit_ondeinit). They are not mandatory, but, as a rule, they are present in the code for the preparation and regular completion of the program: we used them and will continue using them in the examples. In a separate section, we provided an [Overview of all event handling functions](/en/book/applications/runtime/runtime_events_overview): we have already studied some of them in detail by now (for example, [OnCalculate](/en/book/applications/indicators_make/indicators_oncalculate) indicator events and the [OnTimer](/en/book/applications/timer/timer_ontimer) timer).  Expert Advisor-specific events ([OnTick](/en/book/automation/experts/experts_ontick), [ontrade](/en/book/automation/experts/experts_ontrade), [OnTradeTransaction](/en/book/automation/experts/experts_ontradetransaction)) will be described in this chapter.

Expert Advisors can use the widest range of source data as trading signals: [quotes](/en/book/applications/timeseries/timeseries_copy_funcs_overview), [ticks](/en/book/applications/timeseries/timeseries_ticks_mqltick), [depth of market](/en/book/automation/marketbook), [trading account history](/en/book/automation/experts/experts_history_select), or indicator readings. In the latter case, the principles of creating indicator instances and reading values from their buffers are no different from those discussed in the chapter [Using ready-made indicators from MQL programs](/en/book/applications/indicators_use). In the Expert Advisor examples in the following sections, we will demonstrate most of these tricks.

It should be noted that trading functions can be used not only in Expert Advisors but also in scripts. We will see examples for both options.
