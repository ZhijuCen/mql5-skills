# Permissions

MetaTrader 5 provides features for restricting the execution of certain actions by MQL programs for security reasons. Some of these restrictions are two-level, i.e., they are set separately for the terminal as a whole and for a specific program. Terminal settings have a priority or act as default values for the settings of any MQL program. For example, a trader can disable all automated trading by checking the corresponding box in the MetaTrader 5 settings dialog. In this case, private trading permissions set earlier to specific robots in their dialogs become invalid.

In the MQL5 API, such restrictions (or vice versa, permissions) are available for reading via the functions TerminalInfoInteger and MQLInfoInteger. Since they have the same effect on an MQL program, the program must check general and specific prohibitions equally carefully (to avoid generating an error when trying to perform an illegal action). Therefore, this section provides a list of all options of different levels.

All permissions are boolean flags, i.e., they store the values of true or false.

| Identifier | Description |
| --- | --- |
| TERMINAL_DLLS_ALLOWED | Permission to use the DLL |
| TERMINAL_TRADE_ALLOWED | Permission to trade automatically online |
| TERMINAL_EMAIL_ENABLED | Permission to send emails (SMTP server and login must be specified in the terminal settings) |
| TERMINAL_FTP_ENABLED | Permission to send files via FTP to the specified server (including reports for the trading account specified in the terminal settings) |
| TERMINAL_NOTIFICATIONS_ENABLED | Permission to send push notifications to a smartphone |
| MQL_DLLS_ALLOWED | Permission to use the DLL for this program |
| MQL_TRADE_ALLOWED | Permission for a program to trade automatically |
| MQL_SIGNALS_ALLOWED | Permission for a program to work with signals |

Permission to use a DLL at the terminal level means that when running an MQL program that contains a link to some dynamic library, the 'Enable DLL Import' flag on the Dependencies tab will be enabled by default in its properties dialog. If the flag is cleared in the terminal settings, then the option in the properties of the MQL program will be disabled by default. In any case, the user must allow imports for the individual program (there is one exception for scripts, which is discussed below). Otherwise, the program will not run.

In other words, the TERMINAL_DLLS_ALLOWED and MQL_DLLS_ALLOWED flags can be checked either by a program without binding to a DLL, or by a program with binding, but for this program, MQL_DLLS_ALLOWED must be unambiguously equal to true (due to the fact that it has already started). Thus, as part of software systems that require a DLL, it probably makes sense to provide an independent utility that would monitor the state of the flag and display diagnostics for the user if it is suddenly turned off. For example, an Expert Advisor may require an indicator that uses a DLL. Then, before trying to load the indicator and get its handle, the EA can check the TERMINAL_DLLS_ALLOWED flag and generate a warning if the flag is reset.

For scripts, the behavior is slightly different because the script settings dialog only opens if the #property script_show_inputs directive is present in the source code. If it is not present, then the dialog appears when the TERMINAL_DLLS_ALLOWED flag is reset in the terminal settings (and the user must enable the flag in order for the script to work). When the general flag TERMINAL_DLLS_ALLOWED is enabled, the script is run without user confirmation, i.e., the MQL_DLLS_ALLOWED value is assumed to be true (according to TERMINAL_DLLS_ALLOWED).

When working in the tester, the TERMINAL_TRADE_ALLOWED and MQL_TRADE_ALLOWED flags are always equal to true. However, in [indicators](/en/book/applications/indicators_make), access to all trading functions is prohibited regardless of these flags. The tester does not allow the testing of MQL programs with DLL dependencies.

The TERMINAL_EMAIL_ENABLED, TERMINAL_FTP_ENABLED, and TERMINAL_NOTIFICATIONS_ENABLED flags are critical for the send mail, SendFTP, and send notification functions, which are described in the [Network functions](/en/book/advanced/network) section. The MQL_SIGNALS_ALLOWED flag affects the availability of a group of functions that manage the mql5.com trading signal subscription  (not discussed in this book). Its state corresponds to the option 'Allow changing signal settings' in the Common tab of MQL program properties.

Since checking some properties requires additional effort, it makes sense to wrap the flags in a class that hides multiple calls to various system functions in its methods. This is all the more necessary because some permissions are not limited to the above options. For example, permission to trade can be set (or removed) not only at the terminal or MQL program level but also for an individual financial instrument — according to its specification from your broker and the exchange sessions. Therefore, at this step, we will present a draft of the Permissions class which will only contain familiar elements, and then we will improve for particular application APIs.

Thanks to the class which acts as a program layer, the programmer does not have to remember which permissions are defined for TerminalInfo functions and which of them are defined for MqlInfo functions.

The source code is in the EnvPermissions.mq5 file.

```
class Permissions
{
public:
   static bool isTradeEnabled(const string symbol = NULL, const datetime session = 0)
   {
      // TODO: will be supplemented by applied checks of the symbol and sessions
      return PRTF(TerminalInfoInteger(TERMINAL_TRADE_ALLOWED))
          && PRTF(MQLInfoInteger(MQL_TRADE_ALLOWED));
   }
   static bool isDllsEnabledByDefault()
   {
      return (bool)PRTF(TerminalInfoInteger(TERMINAL_DLLS_ALLOWED));
   }
   static bool isDllsEnabled()
   {
      return (bool)PRTF(MQLInfoInteger(MQL_DLLS_ALLOWED));
   }
   
   static bool isEmailEnabled()
   {
      return (bool)PRTF(TerminalInfoInteger(TERMINAL_EMAIL_ENABLED));
   }
   
   static bool isFtpEnabled()
   {
      return (bool)PRTF(TerminalInfoInteger(TERMINAL_FTP_ENABLED));
   }
   
   static bool isPushEnabled()
   {
      return (bool)PRTF(TerminalInfoInteger(TERMINAL_NOTIFICATIONS_ENABLED));
   }
   
   static bool isSignalsEnabled()
   {
      return (bool)PRTF(MQLInfoInteger(MQL_SIGNALS_ALLOWED));
   }
};

```

All class methods are static and are called in OnStart.

```
void OnStart()
{
   Permissions::isTradeEnabled();
   Permissions::isDllsEnabledByDefault();
   Permissions::isDllsEnabled();
   Permissions::isEmailEnabled();
   Permissions::isPushEnabled();
   Permissions::isSignalsEnabled();
}

```

An example of generated logs is shown below.

```
TerminalInfoInteger(TERMINAL_TRADE_ALLOWED)=1 / ok
MQLInfoInteger(MQL_TRADE_ALLOWED)=1 / ok
TerminalInfoInteger(TERMINAL_DLLS_ALLOWED)=0 / ok
MQLInfoInteger(MQL_DLLS_ALLOWED)=0 / ok
TerminalInfoInteger(TERMINAL_EMAIL_ENABLED)=0 / ok
TerminalInfoInteger(TERMINAL_NOTIFICATIONS_ENABLED)=0 / ok
MQLInfoInteger(MQL_SIGNALS_ALLOWED)=0 / ok

```

For self-study, the script has a built-in (but commented out) ability to connect system DLLs to read the contents of the Windows clipboard. We will consider the creation and use of libraries, in particular the #import directive, in the seventh part of the book, in the section [Libraries](/en/book/advanced/libraries).

Let's assume that the global DLL import option is disabled in the terminal disabled (this is the recommended setting for security reasons). Then, if DLLs are connected to the script, it will be possible to run the script only by allowing import in its individual settings dialog, as a result of which MQLInfoInteger(MQL_DLLS_ALLOWED) will be returning 1 (true). If the global permission for the DLL is given, then we get TerminalInfoInteger(TERMINAL_DLLS_ALLOWED)=1, and MQL_DLLS_ALLOWED will inherit this value.
