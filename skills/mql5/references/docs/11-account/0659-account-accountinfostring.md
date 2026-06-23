# AccountInfoString

Returns the value of the appropriate account property.

```
string  AccountInfoString(
   ENUM_ACCOUNT_INFO_STRING  property_id      // Property identifier
   );

```

Parameters

property_id

[in]  Property identifier. The value can be one of the values of [ENUM_ACCOUNT_INFO_STRING](/en/docs/constants/environment_state/accountinformation#enum_account_info_string).

Return Value

Value of [string](/en/docs/basis/types/stringconst) type.

Example:

```
void OnStart()
  {
//--- Show all the information available from the function AccountInfoString()
   Print("The name of the broker = ",AccountInfoString(ACCOUNT_COMPANY));
   Print("Deposit currency = ",AccountInfoString(ACCOUNT_CURRENCY));
   Print("Client name = ",AccountInfoString(ACCOUNT_NAME));
   Print("The name of the trade server = ",AccountInfoString(ACCOUNT_SERVER));
  }

```

See also

[Account Information](/en/docs/constants/environment_state/accountinformation)
