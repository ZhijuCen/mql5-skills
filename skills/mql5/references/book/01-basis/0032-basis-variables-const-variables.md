# Constant variables

However paradoxically this appears, most programming languages support the concept of constant variables. In MQL5, they are described by adding modifier const. It is placed in the variable description, preceding its type, and means that the variable value cannot be changed in any way upon its initialization by the initial value. During its entire lifetime, the variable will have the same value, i.e., a constant.

The compiler will just prevent assigning the constant with a value: The error "constant cannot be modified" will appear in the relevant string.

Modifier const is aimed at explicitly showing the programmer's intention not to change the relevant variable, if a commonly known fixed value, such as the EUR index to compute the USD index, the number of weeks in a year, etc. It is recommended to always use modifier const if you are not going to change the variable. This helps avoid potential errors later, if the programmer themselves or somebody from among their colleagues accidentally tries to write something else into the constant.

For example, we can add modifier const for the messages array in the Greeting function. This does not appear plainly useful for such a small program. However, since programs tend to grow out, any string may sooner or later "find itself" in a much more complex software environment, such as added statements, operation modes, etc. Therefore, it makes sense to have a plan B; particularly as it is so simple.

```
string Greeting() 
{
  static int counter = 0;
  static const string messages[3] =
  {
    "Good morning", "Good day", "Good evening"
  };
  // error demo: 'messages' - constant cannot be modified
  // messages[0] = "Good night";
  return messages[counter++ % 3];
}

```

In the commented string, we test recording the "Good night" string into the first element of the array (remember that numbering starts from 0). In this case, the sense of this action is just to make sure that the compiler prevents from doing that.

As is easily seen, modifiers static and const can be combined. The order of recording them is not important.

By the way, in MQL5, variables become constants in both using modifier const and declaring them with the input variables of the program.
