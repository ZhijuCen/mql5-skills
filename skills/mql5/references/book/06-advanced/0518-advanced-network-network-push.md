# Sending push notifications

As you know, the terminal allows you to send push notifications from MetaQuotes services, the terminal itself, and MQL programs to a mobile device with [iOS](https://www.metatrader5.com/en/mobile-trading/iphone/help/settings_messages) or [Android](https://www.metatrader5.com/en/mobile-trading/android/help/messages) operating systems. This technology uses MetaQuotes ID, a unique identifier of a user (see the note). MetaQuotes ID is allocated when installing the mobile version of the terminal on the user's device, after which the ID must be specified in the terminal settings, on the Notifications tab (several identifiers can be specified separated by commas). After that, the functionality for sending push notifications becomes available for MQL programs.

In fact, MetaQuotes ID does not identify a user, but a specific installation of a mobile terminal; a user can have several installations. The ID is not associated with the registration in the mql5.com community by default, although such a binding can be specified on the site. Do not confuse user registration in the community with MetaQuotes ID. To work with notifications, the terminal user is not required to log into the community.

bool SendNotification(const string text)

The SendNotification function sends push notifications with the specified text to all mobile terminals that have a MetaQuotes ID from the terminal settings. The message length is no more than 255 characters.

If the notification is successfully sent from the terminal, the function returns true, and it returns false if an error occurs. Possible error codes in _LastError include:

- 4515 — ERR_NOTIFICATION_SEND_FAILED — communication problems
- 4516 — ERR_NOTIFICATION_WRONG_PARAMETER — an invalid parameter, for example, an empty string
- 4517 — ERR_NOTIFICATION_WRONG_SETTINGS — MetaQuotes ID is incorrectly configured or missing
- 4518 — ERR_NOTIFICATION_TOO_FREQUENT — too frequent function calls

If there is a connection to the server, the message is sent instantly. If the user's device is online, the message should reach the addressee, but delivery cannot be guaranteed in the general case. There is no return notification to the program about the delivery of the message. The history of push messages on the server for deferred delivery is not saved.

The function has restrictions on the frequency of use: no more than 2 calls per second and no more than 10 per minute.

The SendNotification function is not executed in the strategy tester.

The book includes a simple script NetNotification.mq5 that sends a test notification when the settings are correct.

```
void OnStart()
{
   const string message = MQLInfoString(MQL_PROGRAM_NAME)
      + " runs on " + AccountInfoString(ACCOUNT_SERVER)
      + " " + (string)AccountInfoInteger(ACCOUNT_LOGIN);
   Print("Sending notification: " + message);
   PRTF(SendNotification(NULL));    // INVALID_PARAMETER(4003)
   PRTF(SendNotification(message)); // NOTIFICATION_WRONG_SETTINGS(4517) or 0 (success)
}

```
