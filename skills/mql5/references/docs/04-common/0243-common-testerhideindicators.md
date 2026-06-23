# TesterHideIndicators

Sets the mode of displaying/hiding indicators used in an EA. The function is intended for managing the visibility of used indicators only during testing.

```
void  TesterHideIndicators(
   bool      hide     // flag
   );

```

Parameters

hide

[in]  Flag for hiding indicators when testing. Set true to hide created indicators, otherwise false.

Return Value

None.

Note

By default, all indicators created in a tested EA are displayed on the visual testing chart.  Besides, these indicators are displayed on the chart that is automatically opened when testing is complete. The TesterHideIndicators() function allows developers to implement the ability to disable the display of used indicators.

To disable the display of an applied indicator when testing an EA, call TesterHideIndicators() equal to true before creating the EA's handle – all indicators created after that are marked with the hide flag. These indicators are not displayed during a visual test and on the chart that is automatically opened upon completion of the test.

To disable the hide mode of the newly created indicators, call TesterHideIndicators() equal to false. Only indicators generated directly from the tested EA can be displayed on the testing chart. This rule applies only to cases where there is not a single template in <data_folder>MQL5\Profiles\Templates.

If the <data_folder>MQL5\Profiles\Templates directory contains a special template <EA_name>.tpl, only the indicators from this template are displayed during a visual testing and on the testing chart. In this case, no indicators applied in the tested EA are displayed. This behavior remains even if TesterHideIndicators() equal to true is called in the EA code.

If the <data_folder>MQL5\Profiles\Templates directory contains no special <EA_name>.tpl template having tester.tpl instead, indicators from the tester.tpl and the ones from the EA not disabled by the TesterHideIndicators() function are displayed during a visual testing and on the testing chart. If there is no tester.tpl template, indicators from the default.tpl template are used instead.

If the strategy tester finds no suitable template (<EA_name>.tpl, tester.tpl or default.tpl), display of the indicators applied in the EA is fully managed by the TesterHideIndicators() function.

Example:

```
bool CSampleExpert::InitIndicators(void)
  {
   TesterHideIndicators(true);
//--- create MACD indicator
   if(m_handle_macd==INVALID_HANDLE)
      if((m_handle_macd=iMACD(NULL,0,12,26,9,PRICE_CLOSE))==INVALID_HANDLE)
        {
         printf("Error creating MACD indicator");
         return(false);
        }
   TesterHideIndicators(false);
//--- create EMA indicator and add it to collection
   if(m_handle_ema==INVALID_HANDLE)
      if((m_handle_ema=iMA(NULL,0,InpMATrendPeriod,0,MODE_EMA,PRICE_CLOSE))==INVALID_HANDLE)
        {
         printf("Error creating EMA indicator");
         return(false);
        }
//--- succeed
   return(true);
  }

```

See also

[IndicatorRelease](/en/docs/series/indicatorrelease)
