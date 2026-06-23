# Trading automation

In this part, we will study the most complex and important component of the MQL5 API which allows the automation of trading actions.

We will start by describing the entities without which it is impossible to write a proper Expert Advisor. These include [financial symbols](/en/book/automation/symbols) and [trading account](/en/book/automation/account) settings.

Then we will look at built-in [trading functions](/en/book/automation/experts) and data structures, along with robot-specific [events](/en/book/automation/experts/experts_ontick) and operating modes. In particular, the key feature of Expert Advisors is integration with the [tester](/en/book/automation/tester), which allows users to evaluate financial performance and optimize trading strategies. We will consider the internal optimization mechanisms and optimization management through the API.

The strategy tester is an essential tool for developing MQL programs since it provides the ability to debug programs in various modes, including bars and ticks, based on modeled or real ticks, with or without visualization of the price stream.

We've already tried to [test indicators](/en/book/applications/indicators_make/indicators_test) in visual mode. However, the set of testing parameters is limited for indicators. When developing Expert Advisors, we will have access to the full range of tester capabilities.

In addition, we will be introduced to a new form of market information: the [Depth of Market](/en/book/automation/marketbook) and its software interface.

```
MQL5 Programming for Traders — Source Codes from the Book. Part 6

Examples from the book are also available in the public project \MQL5\Shared Projects\MQL5Book

```
