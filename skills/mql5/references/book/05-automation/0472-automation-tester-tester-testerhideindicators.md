# Managing indicator visibility: TesterHideIndicators

By default, the visual testing chart shows all the indicators that are created in the Expert Advisor being tested. Also, these indicators are shown on the chart, which automatically opens at the end of testing. All this applies only to those indicators that are directly created in your code: nested indicators that can be used in the calculation of the main indicators do not apply here.

The visibility of indicators is not always desirable from the developer's point of view, who may want to hide the implementation details of an Expert Advisor. In such cases, the function TesterHideIndicators will disable the display of the used indicators on the chart.

void TesterHideIndicators(bool hide)

Boolean parameter hide instructs either to hide (by value true) or display (by value false) indicators. The set state is remembered by the MQL program execution environment until it is changed by calling the function again with the inverse parameter value. The current state of this setting affects all newly created indicators.

In other words, the function TesterHideIndicators with the required flag value hide should be called before creating descriptors of the corresponding indicators. In particular, after calling the function with the true parameter, new indicators will be marked with a hidden flag and will not be shown during visual testing and on the chart, which is automatically opened when testing is completed.

To disable the mode of hiding newly created indicators, call TesterHideIndicators with false.

The function is applicable only in the tester.

The function has some specifics related to its performance, provided that special tpl templates are created for the tester or Expert Advisor in the folder /MQL5/Profiles/Templates.

If there is a special template in the folder <expert_name>.tpl, then during visual testing and on the testing chart, only indicators from this template will be shown. In this case, no indicators used in the tested Expert Advisor will be displayed, even if the function was called in the Expert Advisor code TesterHideIndicators with false.

If there is a template in the tester.tpl folder, then during visual testing and on the testing chart, indicators from the tester.tpl template will be shown, plus those indicators from the Expert Advisor that are not prohibited by the TesterHideIndicators call. The TesterHideIndicators function does not affect the indicators in the template.

If there is no template tester.tpl, but there is a template default.tpl, then the indicators from it are processed according to a similar principle.

We will demonstrate how the function works in the [Big Expert Advisor example](/en/book/automation/tester/tester_example_ea) a little later.
