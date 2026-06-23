# Editing, compiling, and running programs

All MetaTrader 5 programs are compilable. That is, a source code written in MQL5 must be compiled to obtain the binary representation that will be exactly the one executed in the terminal.

Programs are edited and compiled using MetaEditor.

![Editing an MQL program in MetaEditor](pics/me_edit_en.png)

Editing an MQL program in MetaEditor

Source code is a text written according to the MQL5 rules and saved as a file having the extension of mq5. The file containing a compiled program will have the same name, while its extension will be ex5.

In the simplest case, one executable file corresponds with one file containing the source code; however, as we will see later, coding complex programs frequently requires splitting the source code into multiple files: The main one and some supporting ones that are enabled from the main file in a special manner. In this case, the main file must still have the extension of mq5, while those enabled from it must have the extension of mqh. Then statements from all source files will get into the executable file being generated. Thus, multiple files containing the source code may be the starting point for creating one executable file/program. All this mentioned here to complete the picture is going to be presented in the second part of the book.

We will use the term MQL5 syntax to denote the set of all rules that allow constructing programs in MQL5. Only the strict adherence to the syntax allows coding programs compatible with the compiler. In fact, teaching to code consists of sequentially introducing all the rules of a particular language that is MQL5, in our case. And this is the main purpose of this book.

To compile a source code, we can use the command MetaEditor File -> Compile or just press F7. However, there are some other, special methods to compile – we will discuss them later. Compiling is accompanied by displaying the changing status in the editor log (where an MQL5 program consists of multiple files containing the source code, and enabling each file is marked in a single log line).

![Compiling an MQL5 program in MetaEditor](pics/me_compile_en.png)

Compiling an MQL5 program in MetaEditor

An indication of a successful compilation is zero errors ("0 errors"). Warnings do not affect the compilation results, they just inform on potential issues. Therefore, it is recommended to fix them on the same basis as errors (we will tell you later how to do that). Ideally, there should not be any warnings ("0 warnings").

Upon the successful compilation of an mq5 file, we get a same-name file with the extension of ex5. MetaTrader 5 Navigator displays as a tree all executable ex5 files located in folder MQL5 and its subfolders, including the one just compiled.

![MetaTrader 5 Navigator with a compiled MQL5 program](pics/mt_navex_en.png)

MetaTrader 5 Navigator with a compiled MQL5 program

Ready programs are launched in the terminal using any methods familiar to the user. For instance, any program, other than a service, can be dragged with the mouse from Navigator to the chart. We will talk about the features of services separately.

Besides, developers often need the program to be executed in the debugging mode to find what causes the errors. There are multiple special commands for this purpose, and we will refer to them in [Bug fixing and debugging](/en/book/intro/errors_debug).
