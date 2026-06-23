# Checking keyboard status

The TerminalInfoInteger function can be used to find out the state of the control keys, which are also called virtual. These include, in particular, Ctrl, Alt, Shift, Enter, Ins, Del, Esc, arrows, and so on. They are called virtual because keyboards, as a rule, provide several ways to generate the same control action. For example, Ctrl, Shift, and Alt are duplicated to the left and right of the spacebar, while the cursor can be moved both by dedicated keys and by the main ones when Fn is pressed. Thus, this function cannot distinguish between control methods at the physical level (for example, the left and right Shift).

The API defines constants for the following keys:

| Identifier | Description |
| --- | --- |
| TERMINAL_KEYSTATE_LEFT | Left Arrow |
| TERMINAL_KEYSTATE_UP | Up Arrow |
| TERMINAL_KEYSTATE_RIGHT | Right Arrow |
| TERMINAL_KEYSTATE_DOWN | Down Arrow |
| TERMINAL_KEYSTATE_SHIFT | Shift |
| TERMINAL_KEYSTATE_CONTROL | Ctrl |
| TERMINAL_KEYSTATE_MENU | Windows |
| TERMINAL_KEYSTATE_CAPSLOCK | CapsLock |
| TERMINAL_KEYSTATE_NUMLOCK | NumLock |
| TERMINAL_KEYSTATE_SCRLOCK | ScrollLock |
| TERMINAL_KEYSTATE_ENTER | Enter |
| TERMINAL_KEYSTATE_INSERT | Insert |
| TERMINAL_KEYSTATE_DELETE | Delete |
| TERMINAL_KEYSTATE_HOME | Home |
| TERMINAL_KEYSTATE_END | End |
| TERMINAL_KEYSTATE_TAB | Tab |
| TERMINAL_KEYSTATE_PAGEUP | PageUp |
| TERMINAL_KEYSTATE_PAGEDOWN | PageDown |
| TERMINAL_KEYSTATE_ESCAPE | Escape |

The function returns a two-byte integer value that reports the current state of the requested key using a pair of bits.

The least significant bit keeps track of keystrokes since the last function call. For example, if TerminalInfoInteger(TERMINAL_KEYSTATE_ESCAPE) returned 0 at some point, and then the user pressed Escape, then on the next call, TerminalInfoInteger(TERMINAL_KEYSTATE_ESCAPE) will return 1. If the key is pressed again, the value will return to 0.

For keys responsible for switching input modes, such as CapsLock, NumLock, and ScrollLock, the position of the bit indicates whether the corresponding mode is enabled or disabled.

The most significant bit of the second byte (0x8000) is set if the key is pressed (and not released) at the current moment.

This feature cannot be used to track pressing of alphanumeric and functional keys. For this purpose, it is necessary to implement the [OnChartEvent](/en/book/applications/events/events_onchartevent) handler and intercept messages with the CHARTEVENT_KEYDOWN code in the program. Please note that events are generated on the chart and are only available for Expert Advisors and indicators. Programs of other types (scripts and services) do not support the event programming model.

The EnvKeys.mq5 script includes a loop through all TERMINAL_KEYSTATE constants.

```
void OnStart()
{
   for(ENUM_TERMINAL_INFO_INTEGER i = TERMINAL_KEYSTATE_TAB;
      i <= TERMINAL_KEYSTATE_SCRLOCK; ++i)
   {
      const string e = EnumToString(i);
      // skip values that are not enum elements
      if(StringFind(e, "ENUM_TERMINAL_INFO_INTEGER") == 0) continue;
      PrintFormat("%s=%4X", e, (ushort)TerminalInfoInteger(i));
   }
}

```

You can experiment with keystrokes and enable/disable keyboard modes to see how the values change in the log.

For example, if capitalization is disabled by default, we will see the following log:

```
TERMINAL_KEYSTATE_SCRLOCK= 0

```

If we press the ScrollLock key and, without releasing it, run the script again, we get the following log:

```
TERMINAL_KEYSTATE_CAPSLOCK=8001

```

That is, the mode is already on and the key is pressed. Let's release the key, and the next time the script will return:

```
TERMINAL_KEYSTATE_SCRLOCK= 1

```

The mode remained on, but the key was released.

TerminalInfoInteger is not suitable for checking the status of keys (TERMINAL_KEYSTATE_XYZ) in dependent indicators created by the [iCustom](/en/book/applications/indicators_use/indicators_icustom) or [IndicatorCreate](/en/book/applications/indicators_use/indicators_indicatorcreate) call. In them, the function always returns 0, even if the indicator was added to the chart using [ChartIndicatorAdd](/en/book/applications/charts/charts_indicators).

Also, the function does not work when the MQL program chart is not active (the user has switched to another one). MQL5 does not provide means for permanent control of the keyboard.
