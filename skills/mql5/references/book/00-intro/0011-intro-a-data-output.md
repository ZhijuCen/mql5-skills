# Data output

In the case of our script, data are output by simply recording the greeting into the log using the Print function. Where necessary, MQL5 allows saving the results in files and databases, sending over the Internet, and displaying as graphical series (in indicators) or objects on charts.

The simplest way to communicate some simple momentary information to the user without making him or her looking into the log (which is a service tool for monitoring the operation of programs and may be hidden from the screen) is provided by the MQL5 API function Comment. It can be used exactly as that of Print. However, its execution results in displaying the text not in the log, but on the current chart, in its upper left corner.

For instance, having replaced Print with Comment in the text script, we will obtain such a function Greeting:

```
void OnStart()
{
  Comment(Greeting(GreetingHour), ", ", Symbol());
}

```

Having launched the changed script in the terminal, we will see the following:

![Displaying text information on the chart using the Comment function](pics/comment.png)

Displaying text information on the chart using the Comment function

If we need both display the text for the user and draw their attention to a change in the environment, related to the new information, it is better to use function Alert. It sends a notification into a separate terminal window that pops up over the main window, accompanying it with a sound alert. It is useful, for example, in case of a trade signal or non-routine events requiring the user's intervention.

The syntax of Alert is identical to that of Print and Comment.

The image below shows the result of the Alert function operation.

![Displaying a notification using the Alert function](pics/alert-ru.png)

Displaying a notification using the Alert function

Script versions with functions Comment and Alert are not attached to this book for the reader to independently try and edit GoodTime2.mq5 and reproduce the screenshots provided herein.
