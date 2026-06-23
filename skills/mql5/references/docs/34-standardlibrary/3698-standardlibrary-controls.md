# Classes for Creating Control Panels and Dialogs

This section contains technical details of working with classes for creation of controls panels and dialogs, as well as description of the relevant components of the MQL5 standard library.

The use of these classes will save time when developing custom interactive MQL5 applications, including Expert Advisors and indicators.

MQL5 Standard Library (in terms of classes for creation of control panels and dialogs) is placed in the terminal data folder, in the MQL5\Include\Controls.

Find the examples of working with classes in the following articles:

- [How to create a graphical panel of any complexity level](https://www.mql5.com/en/articles/4503)
- [Improving Panels: Adding transparency, changing background color and inheriting from CAppDialog/CWndClient](https://www.mql5.com/en/articles/4575)
- [Adding a control panel to an indicator or an Expert Advisor in no time](https://www.mql5.com/en/articles/2171)
- [Create your own graphical panels in MQL5](https://www.mql5.com/en/articles/345)
- [Creating active control panels in MQL5 for trading](https://www.mql5.com/en/articles/62)

The sample Expert Advisor, which illustrates the operation of these classes, can be found in MQL5\Expert\Examples\Controls.

| Auxiliary structures | Description |
| --- | --- |
| CRect | Structure of the rectangular area |
| CDateTime | Structure for working with date and time |

| Base classes | Description |
| --- | --- |
| CWnd | Base class for all controls |
| CWndObj | Base class for controls and dialogs |
| CWndContainer | Base class for complex controls |

| Simple controls | Description |
| --- | --- |
| CLabel | Control, based on "Text label" graphic object |
| CBmpButton | Control, based on "Bitmap label" graphic object |
| CButton | Control, based on "Button" graphic object |
| CEdit | Control, based on "Edit field" graphic object |
| CPanel | Control, based on "Rectangle label" |
| CPicture | Control, based on "Bitmap label" |

| Complex controls | Description |
| --- | --- |
| CScroll | Base class of the scroll bar |
| CScrollV | Vertical scroll bar |
| CScrollH | Horizontal scroll bar |
| CWndClient | Base class of the client area with scroll bars |
| CListView | List view |
| CComboBox | Combo box |
| CCheckBox | Check box |
| CCheckGroup | Check group |
| CRadioButton | Radio button |
| CRadioGroup | Radio group |
| CSpinEdit | Increment/decrement field |
| CDialog | Dialog |
| CAppDialog | Main dialog of MQL5 application |
