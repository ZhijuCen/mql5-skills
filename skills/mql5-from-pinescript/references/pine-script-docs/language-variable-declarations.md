<!-- source: https://www.tradingview.com/pine-script-docs/language/variable-declarations/ | fetched 2026-09-23 | why: var / varip = the recursion & sequence state we ported -->

User ManualLanguage# Variable declarations
## Introduction
Variables are named containers that store calculated values or other data for a script to access and use within a given scope. Variables in Pine Script ® can hold data of any available type that is not void , including the direct values of value types , and the IDs (references) of drawings , collections , plots or other instances of reference types .

A variable in Pine Script consists of three main parts:

- An identifier (name), which represents the variable in the source code.
- A qualified type , which determines the kind of data the variable stores and whether the data can change.
- An assigned value or reference.
Programmers write variable declarations to create custom variables for working with data of specific types when the available built-in variables do not suffice. A variable declaration is a statement specifying that, from a particular point onward in a specific scope , an identifier refers to a variable with a given initial value or reference. The script accesses the saved value or reference while evaluating expressions or statements that use the variable’s identifier.

There are two forms of variable declarations in Pine Script:

- Single-variable declarations declare and initialize one variable. Programmers can include optional keywords in the statement to define the variable’s type and its declaration behavior, or to export the variable from a library .
- Tuple declarations declare and initialize multiple variables using a tuple format. Programmers use these statements to declare variables that hold the data from function calls , conditional structures , or loops that return tuples of data.
All of the statements in the following code block are examples of valid variable declarations. Each identifier to the left of an = operator in the code is the name of a new variable , and the expression or structure to the right determines that variable’s initial value or reference:

Regardless of format, several key characteristics and limitations apply to user-defined variables:

- Every variable has one qualified type, even if its declaration does not explicitly specify the type in the code. Variables declared without type keywords or qualifier keywords inherit type information from their assigned data. A variable’s qualified type never changes across script executions.
- Most custom variables are mutable . Scripts can reassign mutable variables by using the reassignment or compound assignment operators. However, they cannot reassign any global variables from inside user-defined functions or methods .
- The scope of a variable depends on the location of its declaration in the code. The scope determines which parts of the script can access that variable. A variable is available to all parts of a script after its declaration in the same scope or a nested scope , but not to any part that is before the declaration or in an outer scope .
- Variables in different scopes can have the same name , but all variables in the same scope require unique names . The only exception is for variables whose identifier is an underscore ( _ ), which makes them unusable in any expressions or statements.
- If a variable in a nested scope has the same name as one in an outer scope, that variable shadows the outer scope’s variable. In other words, the script cannot access the outer scope’s variable in any part of the nested scope following the inner variable’s declaration.
- By default, a script declares and initializes a variable anew during each execution of its scope. However, a single-variable declaration can include the var or varip keyword to set an alternative declaration mode , causing the variable and its data to persist across bars or ticks.
## Single-variable declarations
A single-variable declaration is a statement that creates one new variable, names it, and assigns it an initial value or reference. The statement can include keywords to specify the variable’s qualified type and declaration mode, or to export the variable. The syntax is as follows:

```
[export ][var |varip ][[qualifier ]<type> ]<identifier> = <expression>|<structure>
```
Where:

- The | character represents OR , all parts enclosed in angle brackets ( <> ) represent required syntax, and all parts in square brackets ( [] ) represent optional syntax.
- export is the optional keyword for exporting the variable from a library , enabling its use in other scripts. Exporting is allowed only if the variable is of a fundamental type and the declaration includes the const keyword.
- var and varip are optional keywords that cause the variable and its data to persist across bars or ticks. If the declaration does not include either keyword, the script reinitializes the variable during every execution of the variable’s scope . Refer to the Declaration modes section for more information.
- qualifier and type refer to keywords for specifying the variable’s qualified type . These keywords are usually optional. If the declaration does not include them, the variable’s assigned data determines its type information. See the Declaring qualified types section to learn more.
- identifier is the variable’s name .
- = is the assignment operator . The expression or structure part to the right of the operator determines the initial value or reference that it assigns to the new variable. expression refers to a literal value, the identifier of another variable, an operation, or a function or method call that returns a single value or reference. structure refers to any conditional structure or loop that returns a single value or reference.
The example below demonstrates a single-variable declaration that declares a “float” variable named median to hold the current value returned by a ta.median() function call:

Note that:

- This statement initializes the median variable anew on every execution, because it does not specify a different declaration mode with the var or varip keyword. Each execution thus updates the variable with the function call’s latest result for the current bar.
- The //@variable comment is an optional annotation that documents the declared variable in the code. Users can hover over the median identifier in the Pine Editor to view a pop-up window that displays the specified line of text.
After a script declares a variable, it can then use that variable in any subsequent part of the code in the same scope or a nested scope. The variable’s identifier serves as a placeholder for a specific value or reference in the script’s logic. When the script evaluates an expression that contains the identifier, it retrieves the variable’s saved data and uses that data in the calculation.

For example, the following script calculates the median of hl2 values over a specified number of bars, then plots the median on the chart as a color-coded line. It declares variables to store the median and other values for the calculations, and uses three of the variables as arguments for the plot() call at the end:

Note that:

- The const keyword specifies that the script cannot reassign the variable. For value types such as “string”, it also declares that the variable’s qualifier is “const”, meaning that it accepts only constant values that are available at compile time .
- The script uses the int , float , bool , color , and string keywords to specify the type of each variable. Using type keywords is optional in all the above declarations, because the compiler can automatically determine the appropriate types, but doing so helps promote readability. See the Declaring qualified types section to learn more about type and qualifier keywords.
- The script can assign the result of the if structure to a variable because both of the structure’s local blocks return the same type (“color”). See the Matching local block type requirement section of the Conditional structures page to learn more.
It’s important to note that a script cannot use a custom variable in any expressions or statements that precede the variable’s declaration, because the variable is not available at that point in the code. Attempting to use a variable in any code before its declaration causes a compilation error.

For example, moving the median declaration in the previous script to the end of the source code causes an error, because the script can no longer access the variable for the isUptrend calculation or the plot() call:

Note The for loop structure uses a single-variable declaration in its header to declare a local counter variable. Likewise, the for…in structure can declare a single local variable in its header to store items from a collection . These types of declarations use a different syntax than that of the declarations described above. See the Loops page to learn more.

## Tuple declarations
Some conditional structures , loops , and function or method calls return tuples containing multiple values or references. To use the data returned from such expressions and structures, programmers must write tuple declarations , which are single statements that declare multiple variables using a tuple format.

The syntax for a tuple declaration is as follows:

```
<tuple_of_identifiers> = <function_call>|<structure>
```
Where:

- The | character represents OR , and all parts enclosed in angle brackets ( <> ) represent required syntax.
- tuple_of_identifiers represents a comma-separated list of variable names enclosed in square brackets (e.g., [x, y, z] ). The tuple must contain one new identifier for each returned value or reference.
- = is the assignment operator . The function_call or structure part to the right of the operator determines the initial data that it assigns to each new variable. function_call refers to a call to a built-in function or user-defined function , or method, that returns a tuple. Likewise, structure refers to a loop or conditional structure that returns a tuple.
Some built-in functions in the ta namespace return a tuple instead of a single value. Therefore, scripts must use tuple declarations to create variables that store the data from calls to those functions. For example, the ta.bb() function returns a tuple containing all three values of the Bollinger Bands indicator in the following order: the basis moving average, the upper band, and the lower band. Therefore, a script must use a tuple declaration, such as the following, to declare one new variable for each returned value:

Tip Function signatures displayed by the Pine Editor’s autosuggest feature or the Reference Manual list return types in square brackets if the function returns a tuple. For instance, the signature for ta.bb() shows the return type [series float, series float, series float] , indicating that a call to the function returns a tuple of three “series float” values.

Programmers often use tuples in user-defined functions and methods to return multiple values for use later in a script’s calculations. A user-defined function returns a tuple only if the final code in its body is a tuple of expressions.

For example, the code block below defines a calcWidthAndColor() function that returns a two-item tuple. The tuple contains a “float” value representing the width between two bands, and a “color” value based on the width value. The code then calls that function using variables from the previous example declaration as arguments, and uses a tuple declaration to declare two new variables to store the returned values:

Note that:

- The upper , lower , length , upperColor , and lowerColor identifiers in the function definition represent parameters , which determine the types of arguments that a call to the function requires.
- The function definition uses single-variable declarations in its body to create variables that store the necessary data for the function’s calculations. Those variables are available only inside the function definition; a script cannot access them in any other scope .
Programmers often use tuple declarations to declare multiple variables that store results returned by conditional structures . Similar to a function, a conditional structure returns a tuple if the final code in each local block is a tuple of expressions.

For example, the following code block declares two variables, lowColor and highColor , to hold “color” values returned by a switch structure based on the value of a string input :

The following script combines all three examples above to calculate a set of Bollinger Bands, their width, and a gradient color, then plots all the values on the chart:

Note The for…in loop structure can also use a tuple declaration in its header to declare two local variables for tracking items from a collection and their indices. However, the syntax differs from other tuple declarations described above. See the for...in loops section of the Loops page to learn more.

## Using an underscore as an identifier
Scripts can declare variables using a single underscore ( _ ) as the identifier to mark those variables as unused . A script cannot access data from any variables named _ or use those variables in other expressions or statements after their declaration. Programmers can write any number of _ variable declarations anywhere in a script, including multiple times in the same scope .

This behavior is useful in cases where a function call returns a tuple of multiple values, but the script requires only some of those values in its calculations. Rather than specifying unique names for all the unused variables from a tuple declaration , programmers can discard those variables by using _ as the name for each one.

For example, the following script calculates the highest and lowest prices across the chart’s visible bars. It imports the VisibleChart library from PineCoders and calls the library’s ohlcv() function to perform the calculation. The call returns a tuple of five values: the visible chart range’s open, high, low, close, and cumulative volume. However, our script requires only the high and low. Instead of specifying unique names for all the unused variables, we use _ as each unused variable’s identifier:

Programmers also occasionally use _ when writing a loop whose calculations do not require the variables declared in the loop’s header. For example, the script below calculates the sum of 20 pseudorandom values from math.random() calls using a for loop. The calculation does not require the loop’s counter variable, so we used _ as the variable’s name to mark it as unused:

Note that:

- The += and /= operators in this script reassign the value of the sample variable after initialization. See the Variable reassignment section to learn more.
## Declaring qualified types
Every variable has an assigned type and a type qualifier , which together define the variable’s qualified type . A variable’s type determines what kind of data the variable represents in the script’s calculations, as well as the types of data that the script can pass to the variable. A variable’s qualifier indicates when the assigned data is available and whether it can change across executions.

Tip Programmers can inspect a variable’s qualified type by hovering over its identifier in the Pine Editor. The editor displays a pop-up window that shows the variable’s type information below its defined description.

By default, the Pine Script compiler automatically determines the qualified type of a variable based on its assigned data. However, in single-variable declarations , programmers can override this behavior and specify qualified types directly by prefixing the declared identifiers with type keywords and qualifier keywords .

The following sections explain how these keywords affect declared variables. For detailed information about Pine’s types and qualifiers, and how they work, refer to the Type system page.

Note Tuple declarations do not support extra keywords for specifying qualified types. As such, each variable from a tuple declaration automatically inherits the same type as its assigned value or reference, and all the variables inherit the strongest type qualifier used by the function call or structure. See the Tuples section of the Type system page to learn more.

### Type keywords
A variable declaration that prefixes the variable’s identifier with a type keyword specifies the type of data that the variable represents in the script’s calculations.

Programmers can use any of the following as the type keyword in a single-variable declaration to set the variable’s type:

- Built-in type keywords: int , float , bool , color , string , line , linefill , box , polyline , label , table , chart.point , footprint , and volume_row .
- Collection type identifiers, which contain the array , matrix , or map keyword followed by a type template (e.g., array<int> , matrix<float> , map<string, color> ).
- The names of enum types or user-defined types .
Note Not all built-in types have corresponding keywords. For example, there are no keywords for the “plot” and “hline” types, or for the unique value types such as “plot_style”.

Including a type keyword in a variable declaration is usually optional , because the Pine Script compiler can automatically determine a variable’s type based on its assigned value or reference. However, a variable declaration requires a type keyword if any of the following conditions apply:

- The declaration includes a qualifier keyword .
- The variable is a constant exported by a library .
- The variable’s initial value is na (undefined), and the statement does not cast it to a valid type using the available type-casting functions (e.g., int() ). See the na value section of the Type system page for more information.
Tip Even when type keywords are not required, we recommend using them in variable declarations when possible. Type keywords help promote readability, and they help the Pine Editor provide type-specific code suggestions.

If a variable declaration does not include a type keyword, the variable automatically inherits the same type as the data that the script uses to initialize it.

For example, the script below declares a variable named myVar without using a type keyword. It initializes the variable using the result of the expression last_bar_index - bar_index , which returns an “int” value. Therefore, the variable automatically inherits the “int” type:

Note that:

- The variable’s qualified type is “series int”, because the built-in variables in the expression store “series” values that change from bar to bar. See the Qualifiers section of the Type system page and the Qualifier keywords section below to learn more.
After a variable inherits a type, the script can assign only data of the inherited type or data that Pine Script can cast to that type, because a variable’s assigned type cannot change after initialization.

For example, the following script attempts to reassign the myVar variable using an expression that returns a “float” value after initializing the variable with an “int” value. This script causes a compilation error , because it cannot automatically cast a “float” value to the “int” type that the myVar variable requires:

If a variable declaration does include a type keyword, the compiler assigns the specified type directly to the variable instead of using the type of the initial value or reference. The script can then assign the variable only data of the specified type, or data that Pine can cast to that type.

For example, if we add the float type keyword to the myVar declaration in the previous example, no compilation error occurs. The keyword directly sets that variable’s type to “float”. Variables of the “float” type can accept “float” or “int” values without errors, because Pine automatically casts “int” values to the “float” type when necessary:

### Qualifier keywords
A single-variable declaration that includes a qualifier keyword ( const , simple , or series ) before the type keyword specifies the variable’s type qualifier . A variable’s type qualifier indicates when the assigned value must be accessible, and whether the value can change during or across script executions. Qualifier keywords are almost always optional . The only exception is for a library’s exported variables, which require the const keyword in their declarations.

Below, we list how each qualifier keyword affects declared variables of value types :

const

The variable has the “const” qualifier . It accepts only a “const” value, which is a compile-time constant that never changes at runtime. Additionally, the keyword prevents the script from reassigning the variable. Other code that requires any value of the type specified by the type keyword can use the variable, because the “const” qualifier is the weakest in Pine’s qualifier hierarchy .

simple

The variable has the “simple” qualifier . It accepts a “simple” value, which becomes available at runtime , during script executions on the first bar of the dataset, and remains consistent across all subsequent bars. It can also accept a value with a weaker qualifier (“input” or “const”). The script can use the variable in any code that allows “simple” values of the given type, but not in any code that requires values with the “input” or “const” qualifiers.

series

The variable has the “series” qualifier . It can accept values with any type qualifier, because “series” is the strongest qualifier in Pine’s qualifier hierarchy. The variable’s value is available at runtime and can change on any bar. The script can use the variable in code that allows “series” values of the given type, but not in any code that requires a value with a weaker qualifier.

Note It is possible to use a qualifier keyword when declaring variables of most reference types . However, in such declarations, the keyword does not directly define the variable’s type qualifier. Instances of these types always have the “series” qualifier. Therefore, the variables that store their IDs automatically inherit the “series” qualifier, regardless of any qualifier keyword. See the Type system page to learn more.

If the declaration of a value-type variable does not include a qualifier keyword, the compiler automatically assigns the variable the strongest type qualifier used by the expressions and structures that determine its value, including those that the script uses to reassign the variable after declaring it.

Note Pine Script does not include a keyword for the “input” qualifier . A variable inherits the “input” qualifier only if its declaration does not use a qualifier keyword and the script uses “input” expressions to determine its value.

For example, the following script calculates and plots the RMA of the close series with a specified length when it runs on a standard chart. It declares multiple variables of value types without using qualifier keywords. Therefore, each variable automatically inherits a qualifier based on its assigned data:

Note that:

- If a reassignment or compound assignment operation modifies any variable declared without a qualifier keyword, and the operation depends on a value with a stronger type qualifier than that of the variable’s initial value, the variable automatically inherits that stronger qualifier. For instance, the plotColor variable has the “series” qualifier, even though the script initializes it using a “const color” value, because the if structure where the script reassigns the value depends on a “series bool” expression ( ta.change(rma) > 0 ).
If a value-type variable declaration does include a qualifier keyword, the compiler assigns the specified qualifier directly to the variable. The variable can accept a value of the specified type with the given qualifier or a weaker one, but it cannot accept a value with a stronger qualifier.

Below, we modified the previous example from this section to demonstrate how qualifier keywords restrict assigned values. Each declaration after the first includes a qualifier keyword that represents a weaker qualifier than that of the variable’s assigned value, causing a compilation error :

In addition to restricting when a variable’s value must be available and whether it can change, a qualifier keyword restricts how the script can use the variable. Scripts can pass a variable only to code that accepts the variable’s qualified type, or to code that allows a value of the same type with a stronger qualifier. If a script attempts to use the variable in code that requires a value with a weaker qualifier, a compilation error occurs.

For example, the script version below uses the simple keyword for the INPUT_TITLE declaration. This change causes an error in the input.int() call. The simple keyword sets the INPUT_TITLE variable’s type to “simple string”, but the title parameter of the input.int() function requires an argument of the type “const string”. The parameter cannot accept “string” arguments with any other type qualifier:

## Variable reassignment
In Pine Script, most variables declared by a script are mutable , meaning that the script can change (reassign) their assigned values or references (IDs) after their declarations. The only exception is for variables that a script declares using the const keyword, because that keyword explicitly prevents the script from reassigning those variables.

Scripts can reassign custom variables of most available types by using the reassignment operator (:=) . The operator directly replaces the variable’s assigned value or reference with the one returned by the specified expression or structure.

For example, the following script declares a variable named myVar with an initial value of 0. Then, it uses the := operator to reassign the variable a value of 10 and plots the result. The script plots a consistent value of 10, not 0, because the := operation overwrites the variable’s initial value:

Note that scripts cannot reassign variables before declaring those variables. Similarly, they cannot reassign local variables while executing code in an outer scope or a separate local scope. See the Scopes section below for more information.

For example, a compilation error occurs if we move the := operation above the myVar declaration in the previous script, because the variable is not available at that point in the global scope:

Scripts can also reassign variables of specific value types by using the compound assignment operators. These operators perform an arithmetic operation using the value of a variable and another specified value, and then reassign the result directly to the original variable:

- Addition/concatenation assignment ( += )
- Subtraction assignment ( -= )
- Multiplication assignment ( *= )
- Division assignment ( /= )
- Modulo (remainder) assignment ( %= )
Note Most compound assignment operators are compatible with variables or fields of only the “int” and “float” types. However, the += operator is also compatible with variables of the “string” type. Additionally, scripts can use the += and -= operators to modify variables that store “plot_display” values from expressions that use the built-in display.* constants.

The following example calculates an EMA of the close series with a user-specified length using reassignment and compound assignment operations. It declares a variable named ema and initializes it with a value of 0, and then reassigns the variable to store the value of nz(ema[1], close) . Afterward, the script uses the *= operator to multiply the variable’s value by the value of (1.0 - alpha) , and then calculates the final value by using the += operator to add the result of alpha * close :

Note that:

- This script uses compound assignment operators for demonstration purposes. An equivalent way to calculate the ema value with fewer lines of code is to use a single := operation to reassign the variable the result of (1.0 - alpha) * nz(ema[1], close) + alpha * close .
- Reassigning a variable can affect its type qualifier . For example, although the script initializes the ema variable using a “const” value, it also reassigns the variable using “series” expressions. Therefore, the variable inherits the “series” qualifier, because that qualifier is stronger than “const”.
Variables declared in tuple declarations are also compatible with reassignment or compound assignment operators. For example, the script below uses a tuple declaration to declare three variables that hold the result of a ta.macd() call, and then uses the := operator on the declared macd variable to assign it a new value. It plots the value of the variable before and after the operation for comparison:

Note that:

- A reassignment or compound assignment operation does not apply to a variable in any code before that operation in the script. The two plot() calls demonstrate this behavior. Although both calls use the macd variable, they show different results because the first call uses the variable’s initial value, and the second uses the variable’s value after executing the := operation.
## Scopes
The scope of a variable refers to the region of a script in which the script can use the declared identifier to access that variable and its data. Every script has one global scope and zero or more local scopes.

The location of a variable declaration in a source code determines the resulting variable’s scope:

- A variable declared inside the code block of a conditional structure , a loop , or a user-defined function or method definition belongs to a unique local scope.
- All variables declared outside these structures, as signified by non-indented lines of code, belong to the script’s global scope.
The global scope is the outermost scope; it encloses all parts of the script defined in the source code. Every local scope is an inner scope, nested into an outer scope, that encloses only the parts of the script defined within a specific structure . In general, declared variables that belong to a given outer scope are accessible to the inner scopes defined within that scope, but only if the structures that create those scopes are below the variable declarations in the code. However, variables that belong to an inner scope are not accessible to any outer scope.

For example, the following script declares a variable named counter and increments its assigned value inside the scope of an if structure, then attempts to use that local variable’s identifier for the series argument of a plot() call in the global scope. This script causes a compilation error, because only the if structure can use the counter identifier to access the variable declared within it. In the global scope, the identifier does not refer to a valid variable:

By contrast, if we move the counter variable declaration above the if structure in the previous code, the variable then belongs to the global scope . With this change, the plot() call can now use the variable. Additionally, the script can still use the identifier in the if structure’s += operation to reassign the variable without causing an error, because a global variable is accessible to the local scopes of the structures defined after its declaration:

Note that:

- The script uses the var keyword to enable the counter variable and its value to persist across bars. To learn more about this keyword, see the Declaration modes section below.
Each variable in a script is a unique container that stores a specific value or reference (ID). As such, every variable that belongs to the same scope must have a unique identifier, because using two variables with identical names in the same scope causes ambiguity. The only exception is for variables that have a single underscore ( _ ) as their identifier, because the identifier makes those variables unusable .

However, variables that belong to different scopes can have the same identifier, even if they differ in their qualified types or declaration modes , because the identifier refers to only one specific variable while the script executes the scope where each variable declaration occurs.

For example, the script below calculates the percentage difference between the total number of rising and falling bars. It declares three variables named counter for its calculations. The script declares the first two inside the separate if structures, and the last one below those structures in the global scope. Although multiple variables share the counter identifier, each exists in a different scope, and the identifier refers to only one of those variables at a time. Therefore, the script compiles successfully:

Note that:

- The script declares the global risingCount and fallingCount variables to store the values returned by the if structures, because the local counter variables are not accessible to the expressions outside their local scopes. When either structure executes its scope, it returns the result of its counter += 1 statement. Otherwise, it returns na .
- If we move the variable declaration on line 20 in this script above the two if statements, a compiler warning occurs because the local variables named counter shadow the global variable. See the Shadowing section below to learn more.
### Shadowing
Variable shadowing refers to the behavior in which a variable in a specific scope prevents access to a variable with the same name in an outer scope. If a script declares a variable within an inner scope and assigns it the same identifier as a variable declared before it in an outer scope, the script cannot use the identifier to access the outer variable while executing the rest of the inner scope. In other words, the inner variable shadows the outer variable.

In most cases, variable shadowing is unintentional . It typically occurs in parts of a script where the programmer intends to reassign a variable instead of creating a new one. Therefore, the compiler displays a warning in the Pine Editor to inform the programmer when it detects a local variable that shadows an outer-scope variable.

Consider the following script, which checks for engulfing candlestick patterns on the chart. It declares a global variable named isEngulf with an initial conditional value of true or false . Then, the script uses the isEngulf identifier in an if structure to filter the condition using criteria based on inputs , and draws a diamond label if the filtered condition remains true. Lastly, the script uses the identifier in a barcolor() call to highlight bars in yellow or orange if the global variable’s value is true .

A newcomer to Pine might expect the script to color the same bars for which it also draws a label, and not others. However, the script colors every bar where the expression on line 16 returns true , and the inputs intended to filter the condition do not affect that output:

This behavior occurs because the script uses the = operator with the isEngulf identifier inside the if structure, then uses the identifier further in the local block to specify the condition that controls the label drawings. That = operation declares a new, local variable named isEngulf , and the new variable shadows the global variable declared on line 16. Consequently, the logic of the structure does not affect the value of the global isEngulf variable. The compiler also displays a warning on line 25 in the code, where the local isEngulf declaration occurs.

We can align the script’s visuals and resolve the compiler warning by replacing the = operator with the reassignment operator (:=) in the if structure. This simple change causes the script to reassign the global isEngulf variable using the switch statement’s result rather than creating a new local variable. Because the script directly changes the value of the global variable in the if structure and uses that variable to control both the label and the bar color, both outputs now occur on the same recent bars:

It is also possible for custom variables in a script to shadow some built-in variables . If a script declares a variable with the same identifier as a built-in variable, the identifier refers exclusively to that variable for the remainder of the scope. As with custom variables, shadowing a built-in variable causes a compiler warning.

For example, the script below declares a variable named close and assigns it the value of the built-in open variable, then plots the values associated with the two identifiers. Both plots show the same values, because the variable declaration makes the built-in close variable inaccessible to the script:

However, shadowing a built-in variable is possible only if the script does not use the identifier to represent the built-in anywhere in the code. If a script already uses the built-in variable, creating a custom variable that shadows it causes a compilation error . For example:

Some variables can also have the same names as namespaces . This naming does not typically result in shadowing. For example, a script can name a variable barstate and still access variables from the barstate namespace. However, if a variable is of a user-defined type (UDT), a compilation error occurs if its name matches a namespace. Such an identifier is not allowed for the type because it can cause obscuring , where the namespace becomes inaccessible or the use of the name becomes ambiguous. For example:

Tip Regardless of errors or warnings, we recommend declaring variables with names that do not conflict with identifiers for built-ins of any kind or custom variables from outer scopes. In addition to preventing shadowing and obscuring, using unique identifiers often helps promote readability and makes code simpler to maintain.

## Declaration modes
A variable’s declaration mode defines whether and how the variable and its data persist across script executions. By default, declared variables do not persist beyond a single execution; the script declares and initializes them anew during every execution of their scopes .

Programmers can override this behavior and specify an alternative mode in a single-variable declaration by including the var or varip keyword in the statement:

- If the declaration includes the var keyword, the resulting variable persists across bars after the first execution of its scope on a bar’s closing tick. After initialization on a closing tick, the variable remains initialized and preserves any data changes that occur on the close of each subsequent bar. However, it does not preserve any changes that occur on a bar before the bar’s closing tick.
- If the declaration includes the varip keyword, the resulting variable persists across every execution . The variable remains initialized after the first execution of its scope, even if that execution occurs before the bar’s closing tick. After initialization, the variable preserves all changes that occur on any execution, including on those for the incoming ticks of open realtime bars .
Tip The sections below provide detailed explanations of the default , var , and varip declaration modes. Understanding this information requires some prior knowledge of Pine’s Execution model and Type system . Therefore, we recommend reviewing the basics of the execution model, reading about the available types , and then coming back to this part to learn more about each declaration mode.

### Default
If a script declares a variable without using the var or varip keyword, it declares and initializes that variable anew during every execution of the variable’s scope . In other words, the variable resets and holds a new value or reference on each new execution, without preserving the data stored during the scope executions on previous bars or ticks.

Note Tuple declarations do not support extra keywords. Therefore, all variables created by a tuple declaration always use the default declaration mode.

The following example demonstrates the default declaration behavior. The script declares a variable named count with an initial value of 0, then uses the += operator to increase its value by one and plots the result. Because the variable declaration does not include the var or varip keyword, the script reinitializes the variable with a value of 0 on every execution. Therefore, the += operation reassigns a constant value of 1 to the variable across the entire dataset:

Although a variable that uses the default declaration mode does not persist across executions, Pine’s runtime system commits (saves) a script’s calculated data from each execution on a bar’s closing tick , including the data for all the script’s variables, to internal time series structures. Scripts can access a variable’s previous saved values or references (IDs) by using the history-referencing operator or the built-in functions that retrieve history internally.

For example, the script version below retrieves the last saved value of the count variable from one bar back using the expression nz(count[1]) , then increments that value by one and reassigns the result to the count variable on the current bar using the := operator. The plot now shows a value that increases by one on each bar rather than remaining at a constant value, because the final value of the count variable on each bar is one greater than the retrieved value for the previous bar:

Note that:

- The expression count[1] returns na on the first bar of the dataset, because there is no previous bar for the script to access at that point. Therefore, we use the nz() function to replace na with 0 in the calculation. See the na value section of the Type system page to learn more.
- A simpler way to achieve the same plotted result is to add var to the counter variable declaration in the previous example script. See the var section to learn more.
Note Although the [] operator can retrieve reference-type IDs for previous bars, scripts cannot modify all types of historical objects. For example, a script cannot modify a collection that it accesses using an ID retrieved for a previous bar. To maintain and update collections across bars, the simplest approach is to declare persistent variables to store their IDs. The var section below includes a basic example.

### ​ var ​
A variable declaration that includes the var keyword creates a variable that persists across bars . The variable remains initialized after the first execution of its scope on a bar’s closing tick . From that bar onward, the variable automatically preserves its assigned value or reference until the script explicitly reassigns it.

In the following example, we modified the first example from the Default section above by adding the var keyword to the count variable declaration. With this change, the script no longer reinitializes the variable on every bar. Instead, the variable becomes permanently initialized as of the closing tick of the dataset’s first bar . On each subsequent bar, the += operation increases the variable’s value by one, and that new value persists into the next execution. The script now plots a value that changes to 1 on the first bar, then to 2 on the second, and so on:

Scripts can use the var keyword to declare persistent variables of most available types , including reference types . If a variable declared with var stores the reference (ID) of an object , such as a collection , changes to that object’s saved data also persist across bars.

For example, the script below declares a variable named myArray using var and initializes it with the ID of an empty array created from a call to array.new<float>() . Then, it uses the variable in a call to array.push() to add a new element to the array once every five bars, and plots the array’s size on the chart. The plotted size increases by one on every fifth bar without resetting to zero, because assigning an array’s ID to a var variable causes that array to persist while the variable continues to reference it:

Note The data associated with a variable declared using var can change during executions that occur before a bar’s closing tick, including those on the ticks of an open realtime bar . However, such changes are temporary . Pine’s rollback process reverts the variable and its data to their last confirmed states, as of the previous bar’s close, before executing on the current bar again. Only the final changes to the variable’s data on the bar’s closing tick persist across subsequent bars. See the Realtime bars section of the Execution model page to learn more. To create a variable that preserves changes across every tick, not just every closing tick, use the varip keyword instead of var in the declaration. See the varip section below for more information.

The var keyword is often helpful when working with instances of drawing types , such as lines . Drawing objects automatically persist across bars until deleted by the runtime system or calls to the built-in *.delete() functions, even if a script does not assign their IDs to variables. However, using var variables to directly store drawing IDs, or the data that the drawings require, often makes them simpler to manage across bars. Additionally, it helps promote runtime efficiency.

For example, the script below draws a line from the open to the close of each daily period on the chart. It uses ta.valuewhen() calls to calculate the opening time and price values for the current period, and assigns those values to variables. On historical bars, the script creates a new line using line.new() and initializes a currLine variable with the returned ID when a new period starts. On realtime bars where the current period is open, the script retrieves the last line ID saved by the variable ( currLine[1] ), deletes the referenced line with a call to line.delete() , and then creates a new line to follow the latest price.

This code is not the most efficient way to achieve the intended result, because it uses ta.valuewhen() to calculate values that the script does not require on every bar, and it deletes and redraws lines on the last bar rather than using line.set*() functions to modify the latest line:

The following script version demonstrates a simpler and more efficient way to achieve the same result. It uses the var keyword in the currLine variable declaration to initialize the variable on only the first bar. On historical bars where a new period starts, the script calls line.set_xy2() to update the end coordinates of the current line referenced by the currLine variable, and then creates a new line for the current bar and reassigns the variable to store that line’s ID. On the latest bar where the current period is open, the script passes the variable to a line.set_xy2() call to update the current line instead of deleting that line and creating a new one:

Note that:

- Programmers can observe the performance difference between these scripts by analyzing them with the Pine Profiler on the historical and realtime bars of an intraday chart.
- It is possible to search the built-in line.all array to access the last drawn line instead of using a persistent variable. However, that approach requires checking the array’s size with the array.size() function and using the array.get() or array.last() function to retrieve the latest line ID. These extra steps require more resources than maintaining a persistent ID with a var variable and updating the referenced line’s data across specific bars.
Scripts can use the var keyword to declare variables in global or local scopes . If a var variable declaration is in a local scope, such as within a conditional structure , that variable persists across each execution of the scope and preserves changes that occur on a bar’s closing tick. The variable does not reset to its initial state on bars where the scope does not execute.

For example, the script below declares a persistent local variable named localVar with an initial value of -1 inside the scope of an if structure. The structure’s local code executes once every 10 bars. After initializing the persistent variable, the structure uses the *= operator to multiply the variable’s current value by -1 and reassign it. The script assigns the local variable’s value to a variable in the global scope named globalVar and plots the result on the chart. Because the localVar variable persists without resetting to its initial value, the plotted results on each 10th bar alternate between -1 and 1:

Note that:

- The if structure returns na on each bar where the local scope does not execute. Therefore, the globalVar variable stores a value other than na only on each 10th bar.
- If we remove var from the localVar variable declaration, causing it to use the default declaration mode, the script plots a consistent value of 1 on each 10th bar, and na on other bars. The result changes because each execution of the scope reinitializes the value to -1, and multiplying that value by -1 results in a value of 1.
It’s important to note that local variables declared using var inside loops behave very differently from those declared using the default declaration mode. If a local variable in a loop uses the default mode, the script reinitializes it on every iteration . By contrast, if the local declaration uses var , the variable remains initialized after the first loop iteration on a bar’s closing tick. From that point onward, it persists and preserves changes to its data from each iteration on the closing ticks of subsequent bars.

For example, the following script declares two local variables inside the body of a for loop that performs five iterations. The local1 variable declaration uses the default declaration mode, and the local2 declaration uses the var keyword. The loop reassigns a value of 0 to the local2 variable on the first iteration, then increments the values of both variables by one on every iteration. The loop returns a tuple containing both values when it ends, and the script uses a tuple declaration to create global variables that store the returned values for its plots:

As shown below, the final value of the local1 variable on each bar is 1, whereas the value of the local2 variable is 5. This difference occurs because the script reinitializes the local1 variable to hold 0 on every loop iteration, so the += operation on that variable consistently sets the value to 1. In contrast, the local2 variable remains initialized after the first loop iteration. Therefore, the += operation on that variable consistently increases the assigned value. The variable stores a value of 1 on the first iteration, 2 on the second iteration, and so on until it reaches the final value of 5 on the last iteration:

Note that:

- As demonstrated by the previous example, even local variables declared with var persist across bars. Therefore, if we remove the if statement that reassigns 0 to the local2 variable, that variable’s value consistently increases by five on each bar.
### ​ varip ​
A variable declaration that includes the varip keyword creates a variable that persists across every tick . The variable becomes permanently initialized after the first execution of its scope , even if that execution occurs before a bar’s closing tick. From that point onward, all changes to the variable’s data persist, even those that occur during script executions on an open bar. The “ip” in the keyword stands for “intrabar persist” , as the value or reference stored by the variable persists across every update within each bar until the script explicitly reassigns the variable.

The varip keyword is compatible with variables that store only specific types of data, including the following:

- Values of any fundamental type (“int”, “float”, “bool”, “color”, or “string”).
- Members of enum types .
- IDs of the chart.point , footprint , or volume_row type.
- The IDs for objects of user-defined types (UDTs) .
The keyword is also compatible with variables that store the IDs of collections , but only if those collections store the following types of data:

- Values of a fundamental type.
- IDs of the chart.point , footprint , or volume_row type.
- IDs for objects of a user-defined type with fields for storing data of only the above types or the IDs of other collections that contain elements of only these types.
A variable declared with varip typically behaves the same as a variable declared with var on historical bars (where the value of the barstate.ishistory variable is true ), because by default, all scripts execute once per bar on that part of the dataset. However, on realtime bars , which form over time as new ticks become available from the data feed, indicator and library scripts execute once per tick instead of once per bar. Variables declared with var and varip typically behave differently on these bars.

As noted in the previous section, if a script modifies a var variable while executing on an open bar, those modifications do not persist. Pine’s rollback process reverts the variable to its last confirmed state as of the previous bar’s close before the script executes on the bar again. This process ensures that the variable stores only confirmed data at the start of each execution, and not any temporary data from ticks that arrive before the bar closes.

By contrast, a variable declared with varip is not affected by rollback. If a script modifies a variable declared with varip while executing on an open bar, the variable preserves its new value or reference without reverting to a previous state after the execution ends. The variable’s new data persists across every subsequent execution on that bar and the bars that follow until the script explicitly changes it again.

Tip For advanced details about the rollback process, refer to the Executions on realtime bars section of the Execution model page.

The following indicator script demonstrates how varip variables behave differently from var variables on realtime bars. The script declares two global variables named counter1 and counter2 . The first declaration uses the var keyword, and the second uses varip . On each execution, the script uses the += operator to increment the values of both variables by one, and then plots the resulting values on the chart. The script also colors the background when the value of barstate.isrealtime is true to emphasize realtime bars:

While running on historical bars, the script executes once on each bar’s closing tick. Therefore, the values of both variables consistently increase by one on each bar in that part of the dataset, and the plots for the two variables show the same results. Then, when the script reaches realtime bars, the two plots begin to diverge.

The script executes multiple times on each realtime bar – once for each new tick – to calculate the bar’s results using the latest available data. The += operations on each execution increase the values of both variables by one. However, while the current bar is open, the change to the counter1 variable resets before each new execution. The variable preserves only the change that occurs on the bar’s closing tick . Therefore, the variable’s final value increases by only one on each realtime bar, just like it does on historical bars.

By contrast, the counter2 variable, declared using varip , does not revert to a previous state on any execution. With each new tick in an open realtime bar, the += operation increases the variable’s value by one, and the new value for the variable persists into the execution on the next tick. Therefore, the variable’s final value for each realtime bar increases by the number of ticks that are available for that bar:

When using the varip keyword to declare variables that access objects of built-in reference types , including chart points or collections of value types, changes to the values stored by those objects also persist across each tick without resetting to a previous state.

For example, the script below uses varip to declare a variable named testPoint that stores a persistent reference to a chart.point object. Then, it uses the += operator to increase the value of the object’s price field by one on each execution and plots the field’s final value for each bar. The plot increments by one across all historical bars, where the script executes only once per bar. On realtime bars, the plot increments by the number of ticks available for each bar, because the chart point’s price field does not reset to a previous state after each += operation while a bar is open:

Note that:

- The same persistent behavior applies to built-in objects whose IDs are stored in collections referenced by varip variables. For example, if a script declares a varip variable that references an array of chart.point IDs, changes to the chart points referenced by the array, and their fields, persist across ticks.
Note In contrast to objects of built-in reference types, objects of user-defined types do not automatically apply varip behaviors to their fields when referenced by variables declared using the varip keyword. To enable these behaviors for the fields of a UDT, prefix the identifier of each field with the varip keyword in the UDT declaration. See the Objects page for an example.

It’s crucial to note that strategies execute differently from indicators. By default, a strategy executes strictly once per bar , even on realtime bars . Therefore, varip variables in a strategy behave the same as var variables by default. However, users can change a strategy’s calculation behavior to enable additional executions on each realtime tick , each historical tick , or after order fills . These settings can cause a strategy’s varip variables to behave differently on both realtime and historical bars.

For example, the simple strategy below alternates between creating a long and short market order on each execution. It also declares two persistent variables named counter1 and counter2 and increments their values by one with the += operator. The first declaration uses var , and the second uses varip . The script also colors the background of all realtime bars for visual reference:

If we run the script with the default calculation behavior, the strategy executes only once on every closed bar. On realtime bars, it waits for each bar to close before performing a new execution. As such, the values of both variables consistently increment by the same amount across all bars and do not diverge:

If we select the “On realtime bar tick” checkbox in the strategy’s Script execution settings, the script executes on each new tick in a realtime bar, similar to an indicator. With this change, the plot for the counter2 variable diverges from that of the counter1 variable on realtime bars:

If we select the “On order fill” checkbox, the script executes again on any bar where the broker emulator fills an order. By default, the emulator assumes that the open, high, low, and close of historical bars are all valid ticks for filling orders, and our script creates a new order on every available tick. With this change, in addition to incrementing by the number of ticks on each realtime bar, the value of the counter2 variable increments by four instead of one on each historical bar after the first:

For more detailed information about this historical behavior, see the Executions on historical bars section of the Execution model page.

Notice Saving data to varip variables is often helpful for various types of calculations that require information from realtime intrabar updates, such as tracking the temporary states of a metric, analyzing value fluctuations within a bar, counting script executions, and more. However, we recommend exercising caution and inspecting your scripts carefully when using the varip keyword in variable declarations, because it can easily cause repainting . After a script reloads across a dataset, all elapsed realtime bars from the former script run become historical bars , which do not contain any of the temporary data from past realtime ticks. Therefore, a script that uses a variable declared using varip might yield different results after reloading, especially if the variable’s associated data changes while a realtime bar is open. Depending on how the script uses the variable, this behavior can impact the script’s alerts , strategy reports , visuals , or overall logic. To see this behavior in action, reload any of the above scripts in this section after running them on realtime bars. For advanced details about this behavior, as well as the events that cause a script to reload, refer to the Events that trigger script executions section of the Execution model page. For general information about the different types of repainting behaviors in Pine and their causes, refer to the Repainting page.

PreviousDeclaration statementsNextOperators## On this page
IntroductionSingle-variable declarationsTuple declarationsUsing an underscore as an identifierDeclaring qualified typesType keywordsQualifier keywordsVariable reassignmentScopesShadowingDeclaration modesDefaultvarvarip
