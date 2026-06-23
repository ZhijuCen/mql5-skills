# Sending email notifications

The terminal allows you to send emails to the email address specified on the Email tab of the settings dialog. For this, MQL5 provides the SendMail function.

bool SendMail(const string subject, const string text)

The function parameters set the title and text (the body of the message).

The function returns true if the message is queued for sending on the mail server; otherwise, it returns false. Errors are possible if the work with mail is disabled in the settings or the mail data (SMTP server, port, login, password) contains an error or is not specified.

The function SendMail is not executed in the strategy tester.

MQL5 does not support checking incoming email and reading it (ie POP, IMAP protocols).

The book includes the script NetMail.mq5 that attempts to send a test message.

```
void OnStart()
{
   const string message = "Hello from "
      + AccountInfoString(ACCOUNT_SERVER)
      + " " + (string)AccountInfoInteger(ACCOUNT_LOGIN);
   Print("Sending email: " + message);
   PRTF(SendMail(MQLInfoString(MQL_PROGRAM_NAME),
      message)); // MAIL_SEND_FAILED(4510) or 0 (success)
}

```
