# Data input

The basic way of data transfer into an MQL program is to use input parameters. They are similar to those of functions and just variables, from many aspects, particularly, in terms of description syntax and principles of their further use in the code.

Moreover, an input parameter description has some essential differences:

- It is placed in the text outside of all blocks (we have learned just the blocks constituting the body of functions yet, but we will learn about the other ones later) or, in other words, beyond any pairs of braces;
- It starts with the keyword input; and
- It is initialized with a default value.

It is usually recommended to place input parameters at the start of the source code.

For instance, to define an input parameter for entering the hour number in our script, the next string should be added immediately upon the triple of directives #property:

```
input int GreetingHour = 0;

```

This record means several things.

- First, there is the GreetingHour variable in the script now, which is available from any place of the source code, including from inside of any function. This definition is called a global-level definition, which is due to the execution of item 1 from the list above.
- Second, using the input keyword makes such a variable visible inside the program and in the user interface, in the MQL5 program properties dialog, which opens when it starts. Thus, when starting the program, a user sets the necessary value of parameters (in our case, one parameter GreetingHour), and they become the values of the corresponding variables during the execution of the program.

Let's note again that the default value that we have specified in the code will be shown to the user in the dialog. However, the user will be able to change it. In this case, it is that new, manually entered value that will be included in the program (not the initialization value).

The initial value of input parameters is affected by both the initialization in the code and the user's interactive choice in launching them, and the MQL5 program type, and the way it is launched. The matter is that different types of MQL5 programs have different life cycles after being launched on charts. Thus, upon a one-time placement in the chart, indicators and Expert Advisors are 'registered' in it forever, until the user removes them explicitly. Therefore, the terminal remembers the latest settings selected and uses them automatically, for example, upon the terminal restart. However, scripts are not saved in charts between the terminal sessions. Therefore, only the default value may be shown to us when we launch the script.

Unfortunately, for some reason, the description of an input parameter does not guarantee calling the dialog of settings at the script start (for scripts as an independent MQL5 program type). For this to happen, it is necessary to add one more, script-specific directive #property into the code:

```
#property script_show_inputs

```

As we will see further, this directive is not required for other types of MQL5 programs.

We needed GreetingHour to transfer its value into the Greeting function. To do so, it is sufficient to insert it into the Greeting function call, instead of 0:

```
void OnStart()
{
  Print(Greeting(GreetingHour), ", ", Symbol());
}

```

Considering the changes we have made to describe the input parameter, let's save the new script version in file GoodTime1.mq5. If we compile and start it, we will see the data entry dialog:

![Dialog to enter the parameters of script GoodTime1.mq5](pics/goodtime1_en.png)

Dialog to enter the parameters of script GoodTime1.mq5

For instance, if we edit the value GreetingHour to 10, then the script will display the following greeting:

```
GoodTime1 (EURUSD,H1)        Good afternoon, EURUSD

```

This is a correct and expected result.

Just for the fun of it, let's run the script again and enter 100. Instead of any meaningful response, we will get:

```
GoodTime1 (EURUSD,H1)        array out of range in 'GoodTime1.mq5' (19,18)

```

We have just encountered a new phenomenon, i.e., runtime error. In this case, the terminal notifies that in position 18 of string 19, our script has tried to read the value of an array element having a non-existing index (beyond the array size).

Since errors are a permanent and necessary companion of a programmer and we have to learn how to fix them, let's talk in some more details about them.
