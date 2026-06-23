# Compilation Errors

MetaEdtior 5 shows error messages about the program errors detected by the built-in compiler during compilation. The list of these errors is given below in table. To compile a source code into an executable one, press F7. Programs that contain errors cannot be compiled until the errors identified by the compiler are eliminated.

| Code | Description |
| --- | --- |
| 100 | File reading error |
| 101 | Error of opening an *. EX5 for writing |
| 103 | Not enough free memory to complete compilation |
| 104 | Empty syntactic unit unrecognized by compiler |
| 105 | Incorrect file name in #include |
| 106 | Error accessing a file in #include (probably the file does not exist) |
| 108 | Inappropriate name for #define |
| 109 | Unknown command of preprocessor (valid #include, #define, #property, #import) |
| 110 | Symbol unknown to compiler |
| 111 | Function not implemented (description is present, but no body) |
| 112 | Double quote (") omitted |
| 113 | Opening angle bracket (<) or double quote (") omitted |
| 114 | Single quote (') omitted |
| 115 | Closing angle bracket ">" omitted |
| 116 | Type not specified in declaration |
| 117 | No return operator or return is found not in all branches of the implementation |
| 118 | Opening bracket of call parameters was expected |
| 119 | Error writing EX5 |
| 120 | Invalid access to an array |
| 121 | The function is not of void type and the return operator must return a value |
| 122 | Incorrect declaration of the destructor |
| 123 | Colon ":" is missing |
| 124 | Variable is already declared |
| 125 | Variable with such identifier already declared |
| 126 | Variable name is too long (> 250 characters) |
| 127 | Structure with such identifier already defined |
| 128 | Structure is not defined |
| 129 | Structure member with the same name already defined |
| 130 | No such structure member |
| 131 | Breached pairing of brackets |
| 132 | Opening parenthesis "(" expected |
| 133 | Unbalanced braces (no "}") |
| 134 | Difficult to compile (too much branching, internal stack levels are overfilled) |
| 135 | Error of file opening for reading |
| 136 | Not enough memory to download the source file into memory |
| 137 | Variable is expected |
| 138 | Reference cannot be initialized |
| 140 | Assignment expected (appears at declaration) |
| 141 | Opening brace "{" expected |
| 142 | Parameter can be a  dynamic array  only |
| 143 | Use of "void" type is unacceptable |
| 144 | No pair for ")" or "]", i.e. "(or" [ " is absent |
| 145 | No pair for "(or" [ ", i.e. ") "or"] " is absent |
| 146 | Incorrect array size |
| 147 | Too many parameters (> 64) |
| 149 | This token is not expected here |
| 150 | Invalid use of operation (invalid operands) |
| 151 | Expression of void type not allowed |
| 152 | Operator is expected |
| 153 | Misuse of break |
| 154 | Semicolon ";" expected |
| 155 | Comma "," expected |
| 156 | Must be a class type, not struct |
| 157 | Expression is expected |
| 158 | "non HEX character" found in HEX or too long number (number of digits> 511) |
| 159 | String-constant has more than 65534 characters |
| 160 | Function definition is unacceptable here |
| 161 | Unexpected end of program |
| 162 | Forward declaration is prohibited for structures |
| 163 | Function with this name is already defined and has another return type |
| 164 | Function with this name is already defined and has a different set of parameters |
| 165 | Function with this name is already defined and implemented |
| 166 | Function overload for this call was not found |
| 167 | Function with a return value of void type cannot return a value |
| 168 | Function is not defined |
| 170 | Value is expected |
| 171 | In  case  expression only integer constants are valid |
| 172 | The value of  case  in this  switch  is already used |
| 173 | Integer is expected |
| 174 | In #import expression file name is expected |
| 175 | Expressions are not allowed on global level |
| 176 | Omitted parenthesis ")" before ";" |
| 177 | To the left of equality sign a variable is expected |
| 178 | The result of expression is not used |
| 179 | Declaring of variables is not allowed in  case |
| 180 | Implicit conversion from a string to a number |
| 181 | Implicit conversion of a number to a string |
| 182 | Ambiguous call of an overloaded function (several overloads fit) |
| 183 | Illegal  else  without proper  if |
| 184 | Invalid  case  or  default  without a  switch |
| 185 | Inappropriate use of ellipsis |
| 186 | The initializing sequence has more elements than the initialized variable |
| 187 | A constant for  case  expected |
| 188 | A constant expression required |
| 189 | A constant variable cannot be changed |
| 190 | Closing bracket or a comma is expected (declaring array member) |
| 191 | Enumerator identifier already defined |
| 192 | Enumeration cannot have access modifiers (const, extern, static) |
| 193 | Enumeration member already declared with a different value |
| 194 | There is a variable defined with the same name |
| 195 | There is a structure defined with the same name |
| 196 | Name of enumeration member expected |
| 197 | Integer expression expected |
| 198 | Division by zero in constant expression |
| 199 | Wrong number of parameters in the function |
| 200 | Parameter by reference must be a variable |
| 201 | Variable of the same type to pass by reference expected |
| 202 | A constant variable cannot be passed by a non-constant reference |
| 203 | Requires a positive integer constant |
| 204 | Failed to access protected class member |
| 205 | Import already defined in another way |
| 208 | Executable file not created |
| 209 | 'OnCalculate' entry point not found for the indicator |
| 210 | The continue operation can be used only inside a loop |
| 211 | Error accessing private (closed) class member |
| 213 | Method of structure or class is not declared |
| 214 | Error accessing private (closed) class method |
| 216 | Copying of structures with objects is not allowed |
| 218 | Index out of array range |
| 219 | Array initialization in structure or class declaration not allowed |
| 220 | Class constructor cannot have parameters |
| 221 | Class destructor can not have parameters |
| 222 | Class method or structure with the same name and parameters have already been declared |
| 223 | Operand expected |
| 224 | Class method or structure with the same name exists, but with different parameters (declaration!=implementation) |
| 225 | Imported function is not described |
| 226 | ZeroMemory()  is not allowed for objects with protected members or inheritance |
| 227 | Ambiguous call of the overloaded function (exact match of parameters for several overloads) |
| 228 | Variable name expected |
| 229 | A reference cannot be declared in this place |
| 230 | Already used as the enumeration name |
| 232 | Class or structure expected |
| 235 | Cannot call 'delete' operator to delete the array |
| 236 | Operator ' while' expected |
| 237 | Operator 'delete' must have a pointer |
| 238 | There is 'default' for this 'switch' already |
| 239 | Syntax error |
| 240 | Escape-sequence can occur only in strings (starts with '\') |
| 241 | Array required - square bracket '[' does not apply to an array, or non arrays are passed as array parameters |
| 242 | Can not be initialized through the initialization sequence |
| 243 | Import is not defined |
| 244 | Optimizer error on the syntactic tree |
| 245 | Declared too many structures (try to simplify the program) |
| 246 | Conversion of the parameter is not allowed |
| 247 | Incorrect use of the 'delete' operator |
| 248 | It's not allowed to declare a pointer to a reference |
| 249 | It's not allowed to declare a reference to a reference |
| 250 | It's not allowed to declare a pointer to a pointer |
| 251 | Structure declaration in the list of parameter is not allowed |
| 252 | Invalid operation of typecasting |
| 253 | A pointer can be declared only for a class or structure |
| 256 | Undeclared identifier |
| 257 | Executable code optimizer error |
| 258 | Executable code generation error |
| 260 | Invalid expression for the 'switch' operator |
| 261 | Pool of string constants overfilled, simplify program |
| 262 | Cannot convert to enumeration |
| 263 | Do not use 'virtual' for data (members of a class or structure) |
| 264 | Cannot call protected method of class |
| 265 | Overridden virtual functions return a different type |
| 266 | Class cannot be inherited from a structure |
| 267 | Structure cannot be inherited from a class |
| 268 | Constructor cannot be virtual ( virtual  specifier is not allowed) |
| 269 | Method of structure cannot be virtual |
| 270 | Function must have a body |
| 271 | Overloading of system functions (terminal functions) is prohibited |
| 272 | Const  specifier is invalid for functions that are not members of a class or structure |
| 274 | Not allowed to change class members in constant method |
| 276 | Inappropriate initialization sequence |
| 277 | Missed default value for the parameter (specific declaration of default parameters) |
| 278 | Overriding the default parameter (different values in declaration and implementation) |
| 279 | Not allowed to call non-constant method for a constant object |
| 280 | An object is necessary for accessing members (a dot for a non class/structure is specified) |
| 281 | The name of an already declared structure cannot be used in declaration |
| 284 | Unauthorized conversion (at closed inheritance) |
| 285 | Structures and arrays cannot be used as input variables |
| 286 | Const  specifier is not valid for constructor/destructor |
| 287 | Incorrect string expression for a datetime |
| 288 | Unknown property (#property) |
| 289 | Incorrect value of a property |
| 290 | Invalid index for a property in #property |
| 291 | Call parameter omitted - <func (x,)> |
| 293 | Object must be passed by reference |
| 294 | Array must be passed by reference |
| 295 | Function was declared as exportable |
| 296 | Function was not declared as exportable |
| 297 | It is prohibited to export imported function |
| 298 | Imported function cannot have this parameter (prohibited to pass a pointer, class or structure containing a dynamic array, pointer, class, etc.) |
| 299 | Must be a class |
| 300 | #import was not closed |
| 302 | Type mismatch |
| 303 | Extern variable  is already initialized |
| 304 | No  exported  function or  entry point  found |
| 305 | Explicit  constructor  call is not allowed |
| 306 | Method was declared as  constant |
| 307 | Method was not declared as  constant |
| 308 | Incorrect size of the resource file |
| 309 | Incorrect resource name |
| 310 | Resource file opening error |
| 311 | Resource file reading error |
| 312 | Unknown resource type |
| 313 | Incorrect path to the resource file |
| 314 | The specified  resource  name is already used |
| 315 | Argument expected for the function-like macro |
| 316 | Unexpected symbol in macro definition |
| 317 | Error in formal parameters of the macro |
| 318 | Invalid number of parameters for a macro |
| 319 | Too many parameters for a macro |
| 320 | Too complex, simplify the macro |
| 321 | Parameter for  EnumToString()  can be only an enumeration |
| 322 | The  resource  name is too long |
| 323 | Unsupported image format (only BMP with 24 or 32 bit color depth is supported) |
| 324 | An array cannot be declared in operator |
| 325 | The function can be declared only in the  global  scope |
| 326 | The declaration is not allowed for the current  scope |
| 327 | Initialization of static variables with the values of local variables is not allowed |
| 328 | Illegal declaration of an array of objects that do not have  a default constructor |
| 329 | Initialization list  allowed only for  constructors |
| 330 | No function definition after initialization list |
| 331 | Initialization list  is empty |
| 332 | Array initialization in a constructor is not allowed |
| 333 | Initializing members of a parent class in the  initialization list  is not allowed |
| 334 | Expression of the  integer type  expected |
| 335 | Memory required for the  array  exceeds the maximum value |
| 336 | Memory required for the  structure  exceeds the maximum value |
| 337 | Memory required for the variables declared on the  global level  exceeds the maximum value |
| 338 | Memory required for  local variables  exceeds the maximum value |
| 339 | Constructor  not defined |
| 340 | Invalid name of the  icon file |
| 341 | Could not open the  icon file  at the specified path |
| 342 | The  icon file  is incorrect and is not of the  ICO  format |
| 343 | Reinitialization of a member in a class/structure constructor using the  initialization list |
| 344 | Initialization of  static  members in the constructor  initialization list  is not allowed |
| 345 | Initialization of a  non-static  member of a class/structure on a  global level  is not allowed |
| 346 | The name of the class/structure method matches the name of an earlier declared member |
| 347 | The name of the class/structure member matches the name of an earlier declared method |
| 348 | Virtual  function cannot be declared as  static |
| 349 | The  const  modifier is not allowed for  static  functions |
| 350 | Constructor  or  destructor  cannot be static |
| 351 | Non-static member/method of a class or a structure cannot be accessed from a  static  function |
| 352 | An overload operation (+,-,[],++,-- etc.) is expected after the  operator  keyword |
| 353 | Not all operations can be  overloaded  in MQL5 |
| 354 | Definition does not match declaration |
| 355 | An invalid number of parameters is specified for the  operator |
| 356 | Event handling function  not found |
| 357 | Method cannot be  exported |
| 358 | A pointer to the  constant  object cannot be normalized by a non-constant object |
| 359 | Class templates are not supported yet |
| 360 | Function template  overload  is not supported yet |
| 361 | Function template cannot be applied |
| 362 | Ambiguous parameter in function template (several parameter types can be applied) |
| 363 | Unable to determine the parameter type, by which the function template argument should be normalized |
| 364 | Incorrect number of parameters in the function template |
| 365 | Function template cannot be  virtual |
| 366 | Function templates cannot be exported |
| 367 | Function templates cannot be imported |
| 368 | Structures containing the objects are not allowed |
| 369 | String arrays and structures containing the objects are not allowed |
| 370 | A static class/structure member  must be explicitly initialized |
| 371 | Compiler limitation: the string cannot contain more than 65 535 characters |
| 372 | Inconsistent  #ifdef/#endif |
| 373 | Object of class cannot be returned, copy constructor not found |
| 374 | Non-static members and methods cannot be used |
| 375 | OnTesterInit() impossible to use without OnTesterDeinit() |
| 376 | Redefinition of formal parameter '%s' |
| 377 | Macro  __FUNCSIG__  and  __FUNCTION__  cannot appear outside of a function body |
| 378 | Invalid returned type. For example, this error will be produced for functions imported from DLL that return structure or pointer. |
| 379 | Template usage error |
| 380 | Not used |
| 381 | Illegal syntax when declaring pure virtual function, only "=NULL" or "=0" are allowed |
| 382 | Only virtual functions can be declared with the pure-specifier ("=NULL" or "=0") |
| 383 | Abstract class cannot be instantiated |
| 384 | A pointer to a user-defined type should be applied as a target type for dynamic casting using the  dynamic_cast  operator |
| 385 | "Pointer to function" type is expected |
| 386 | Pointers to methods are not supported |
| 387 | Error – cannot define the type of a pointer to function |
| 388 | Type cast is not available due to  private  inheritance |
| 389 | A variable with  const  modifier should be initialized during declaration |
| 393 | Only methods with  public access  can be declared in an  interface |
| 394 | Invalid nesting of an  interface  inside of another interface |
| 395 | An interface can only be derived from another interface |
| 396 | An  interface  is expected |
| 397 | Interfaces only support  public inheritance |
| 398 | An  interface  cannot contain members |
| 399 | Interface  objects cannot be created directly, only use inheritance |
| 400 | A specifier cannot be used in a forward declaration |
| 401 | Inheritance from the class is impossible, since it is declared with the  final  specifier |
| 402 | Cannot  redefine  a method declared with the  final  specifier |
| 403 | The  final  specifier can be applied only to virtual functions |
| 404 | The method marked by the  override  specifier actually does not override any base class function |
| 405 | A specifier is not allowed in defining a function, but only in declaring |
| 406 | Cannot cast the type to the specified one |
| 407 | The type cannot be used for a  resource  variable |
| 408 | Error in the project file |
| 409 | Cannot be used as a  union  member |
| 410 | Ambiguous choice for the name, the usage context should be explicitly defined |
| 411 | The structure cannot be used from DLL |
| 412 | Cannot call a function marked by the  delete  specifier |
| 413 | MQL4 is not supported. To compile this program, use MetaEditor from your MetaTrader 4 installation folder |
