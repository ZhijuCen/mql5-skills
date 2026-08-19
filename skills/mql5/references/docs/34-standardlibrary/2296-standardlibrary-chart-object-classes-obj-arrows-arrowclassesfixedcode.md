# Arrows with fixed code

"Arrows with fixed code" are classes for simplified access to the properties of the following graphical objects:

| Class name | Arrow object name |
| --- | --- |
| CChartObjectArrowCheck | "Arrow Check" |
| CChartObjectArrowDown | "Arrow Down" |
| CChartObjectArrowUp | "Arrow Up" |
| CChartObjectArrowStop | "Arrow Stop" |
| CChartObjectArrowThumbDown | "Good" ("Thumbs up") |
| CChartObjectArrowThumbUp | "Bad" ("Thumbs down") |
| CChartObjectArrowLeftPrice | "Left price" arrow |
| CChartObjectArrowRightPrice | "Right price" arrow |

### Description

"Arrows with fixed code" classes provide access to the object properties.

### Declarations

```
   class CChartObjectArrowCheck      : public CChartObjectArrow;
   class CChartObjectArrowDown       : public CChartObjectArrow;
   class CChartObjectArrowUp         : public CChartObjectArrow;
   class CChartObjectArrowStop       : public CChartObjectArrow;
   class CChartObjectArrowThumbDown  : public CChartObjectArrow;
   class CChartObjectArrowThumbUp    : public CChartObjectArrow;
   class CChartObjectArrowLeftPrice  : public CChartObjectArrow;
   class CChartObjectArrowRightPrice : public CChartObjectArrow;

```

### Title

```
   <ChartObjects\ChartObjectsArrows.mqh>

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates the graphical object matching the class |
| Properties |  |
| ArrowCode | "Stub" for symbol code change method |
| Input/output |  |
| virtual  Type | Virtual method of identification |

See also

[Object types](/en/docs/constants/objectconstants/enum_object), [Methods of object binding](/en/docs/constants/objectconstants/enum_anchorpoint), [Graphic objects](/en/docs/objects)
