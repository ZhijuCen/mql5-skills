# Creating and deleting custom symbols

The first two functions you need in order to work with custom symbols are CustomSymbolCreate and CustomSymbolDelete.

bool CustomSymbolCreate(const string name, const string path = "", const string origin = NULL)

The function creates a custom symbol with the specified name (name) in the specified group (path) and, if necessary, with the properties of an exemplary symbol — its name can be specified in the parameter origin.

The name parameter should be a simple identifier, without hierarchy. If necessary, one or more required levels of groups (subfolders) should be specified in the parameter path, with the delimiter character being a backslash '\' (the forward slash is not supported here, unlike the file system). The backslash must be doubled in literal strings ("\\").

By default, if the path string is empty ("" or NULL), the symbol is created directly in the Custom folder, which is allocated in the general hierarchy of symbols for user symbols. If the path is filled, it is created inside the Custom folder to the full depth (if there are no corresponding folders yet).

The name of a symbol, as well as the name of a group of any level, can contain Latin letters and numbers, without punctuation marks, spaces, and special characters. Additionally, only '.', '_', '&', and '#' are allowed.

The name must be unique in the entire symbol hierarchy, regardless of which group the symbol is supposed to be created in. If a symbol with the same name already exists, the function will return false and will set the error code 5300 (ERR_NOT_CUSTOM_SYMBOL) or 5304 (ERR_CUSTOM_SYMBOL_EXIST) in _LastError.

Note that if the last (or even the only) element of the hierarchy in the path string exactly matches the name (case sensitive), then it is treated as a symbol name that is part of the path and not as a folder. For example, if the name and path contain the strings "Example" and "MQL5Book\\Example", respectively, then the symbol "Example" will be created in the "Custom\\MQL5Book\\" folder. At the same time, if we change the name to "example", we will get the "example" symbol in the "Custom\\MQL5Book\\Example" folder.

This feature has another consequence. The SYMBOL_PATH property returns the path along with the symbol name at the end. Therefore, if we transfer its value without changes from some exemplary symbol to a newly created one, we will get the following effect: a folder with the name of the old symbol will be created, inside which a new symbol will appear. Thus, if you want to create a custom symbol in the same group as the original symbol, you must strip the name of the original symbol from the string obtained from the SYMBOL_PATH property.

We will demonstrate the side effect of copying the SYMBOL_PATH property in an example in the next section. However, this effect can also be used as a positive one. In particular, by creating several of its symbols based on one original symbol, copying SYMBOL_PATH will ensure that all new symbols are placed in the folder with the name of the original, i.e., it will group the symbols according to their prototype symbol.

The SYMBOL_PATH property for custom symbols always starts with the "Custom\\" folder (this prefix is added automatically).

Name length is limited to 31 characters. When the limit is exceeded, CustomSymbolCreate will return false and set error code 5302 (ERR_CUSTOM_SYMBOL_NAME_LONG).

The maximum length of the parameter path is 127 characters, including "Custom\\", group separators "\\", and the symbol name, if it is specified at the end.

The origin parameter allows you to optionally specify the name of the symbol from which the properties of the created custom symbol will be copied. After creating a custom symbol, you can change any of its properties to the desired value using the appropriate functions (see [CustomSymbolSet](/en/book/advanced/custom_symbols/custom_symbols_properties) functions).

If a non-existent symbol is given as the origin parameter, then the custom symbol will be created "empty", as if the parameter origin was not specified. This will raise error 4301 (ERR_MARKET_UNKNOWN_SYMBOL).

In a new symbol created "blank", all properties are set to their default values. For example, the contract size is 100000, the number of digits in the price is 4, the margin calculation is carried out according to Forex rules, and charting is based on the Bid prices.

When you specify origin, only settings are transferred from this symbol to the new symbol but not quotes or ticks as they should be generated separately. This will be discussed in the following sections.

Creating a symbol does not automatically add it to Market Watch. So, this must be done explicitly (manually or programmatically). Without quotes, the chart window will be empty.

bool CustomSymbolDelete(const string name)

The function deletes a custom symbol with the specified name. Not only settings are deleted, but also all data on the symbol (quotes and ticks). It is worth noting, that the history is not deleted immediately, but only after some delay, which can be a source of problems if you intend to recreate a symbol with the same name (we will touch on this point in the example of the section [Adding, replacing, and deleting quotes](/en/book/advanced/custom_symbols/custom_symbols_rates)).

Only a custom symbol can be deleted. Also, you cannot delete a symbol selected in Market Watch or a symbol having an open chart. Please note that a symbol can also be selected [implicitly](/en/book/automation/symbols/symbols_state), without displaying in the visible list (in such cases, the SYMBOL_VISIBLE property is false, and the SYMBOL_SELECT property is true). Such a symbol first must be "hidden" by calling SymbolSelect("name", false) before attempting to delete: otherwise, we get a CUSTOM_SYMBOL_SELECTED (5306) error.

If deleting a symbol leaves an empty folder (or folder hierarchy), it is also deleted.

For example, let's create a simple script CustomSymbolCreateDelete.mq5. In the input parameters, you can specify a name, a path, and an exemplary symbol.

```
input string CustomSymbol = "Dummy";         // Custom Symbol Name
input string CustomPath = "MQL5Book\\Part7"; // Custom Symbol Folder
input string Origin;

```

In the OnStart handler, let's check if there is already a symbol with the given name. If not, then after the confirmation from the user, we will create such a symbol. If the symbol is already there and it's a custom symbol, let's delete it with the user's permission (this will make it easier to clean up after the experiment is over).

```
void OnStart()
{
   bool custom = false;
   if(!PRTF(SymbolExist(CustomSymbol, custom)))
   {
      if(IDYES == MessageBox("Create new custom symbol?", "Please, confirm", MB_YESNO))
      {
         PRTF(CustomSymbolCreate(CustomSymbol, CustomPath, Origin));
      }
   }
   else
   {
      if(custom)
      {
         if(IDYES == MessageBox("Delete existing custom symbol?", "Please, confirm", MB_YESNO))
         {
            PRTF(CustomSymbolDelete(CustomSymbol));
         }
      }
      else
      {
         Print("Can't delete non-custom symbol");
      }
   }
}

```

Two consecutive runs with default options should result in the following log entries.

```
SymbolExist(CustomSymbol,custom)=false / ok
Create new custom symbol?
CustomSymbolCreate(CustomSymbol,CustomPath,Origin)=true / ok
   
SymbolExist(CustomSymbol,custom)=true / ok
Delete existing custom symbol?
CustomSymbolDelete(CustomSymbol)=true / ok

```

Between runs, you can open the symbol dialog in the terminal and check that the corresponding custom symbol has appeared in the symbol hierarchy.
