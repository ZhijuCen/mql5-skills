# SendMail

Sends an email at the address specified in the settings window of the "Email" tab.

```
bool  SendMail(
   string  subject,       // header
   string  some_text      // email text
   );

```

Parameters

subject

[in]  Email header.

some_text

[in]  Email body.

Return Value

true – if an email is put into the send queue, otherwise - false.

Note

Sending can be prohibited in settings, email address can be omitted as well. For the error information call [GetLastError()](/en/docs/check/getlasterror).

SendMail() function does not work in the [Strategy Tester](/en/docs/runtime/testing#alert_etc).

Example:

```
//+------------------------------------------------------------------+
//|                                                     SendMail.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com
#property version     "1.00"
 
#define   SUBJECT   "Test SendMail"
#define   TEXT      "Text for SendMail() function"
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart(void)
  {
//--- check permission to send email in the terminal
   if(!TerminalInfoInteger(TERMINAL_EMAIL_ENABLED))
     {
      Print("Error. The client terminal does not have permission to send email messages");
      return;
     }
//--- send mail
   ResetLastError();
   if(!SendMail(SUBJECT, TEXT))
      Print("SendMail() failed. Error ",GetLastError());
  }

```
