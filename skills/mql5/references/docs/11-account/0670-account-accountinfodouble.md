# AccountInfoDouble

Returns the value of the appropriate account property.

```
double  AccountInfoDouble(
   ENUM_ACCOUNT_INFO_DOUBLE  property_id      // Property identifier
   );

```

Parameters

property_id

[in]  Property identifier. The value can be one of the values of [ENUM_ACCOUNT_INFO_DOUBLE](/en/docs/constants/environment_state/accountinformation#enum_account_info_double).

Return Value

Value of [double](/en/docs/basis/types/double) type.

Example:

```
void OnStart()
  {
//--- Show all the information available from the function AccountInfoDouble()
   printf("ACCOUNT_BALANCE =  %G",AccountInfoDouble(ACCOUNT_BALANCE));
   printf("ACCOUNT_CREDIT =  %G",AccountInfoDouble(ACCOUNT_CREDIT));
   printf("ACCOUNT_PROFIT =  %G",AccountInfoDouble(ACCOUNT_PROFIT));
   printf("ACCOUNT_EQUITY =  %G",AccountInfoDouble(ACCOUNT_EQUITY));
   printf("ACCOUNT_MARGIN =  %G",AccountInfoDouble(ACCOUNT_MARGIN));
   printf("ACCOUNT_MARGIN_FREE =  %G",AccountInfoDouble(ACCOUNT_MARGIN_FREE));
   printf("ACCOUNT_MARGIN_LEVEL =  %G",AccountInfoDouble(ACCOUNT_MARGIN_LEVEL));
   printf("ACCOUNT_MARGIN_SO_CALL = %G",AccountInfoDouble(ACCOUNT_MARGIN_SO_CALL));
   printf("ACCOUNT_MARGIN_SO_SO = %G",AccountInfoDouble(ACCOUNT_MARGIN_SO_SO));
  }

```

See also

[SymbolInfoDouble](/en/docs/marketinformation/symbolinfodouble),  [SymbolInfoString](/en/docs/marketinformation/symbolinfostring), [SymbolInfoInteger](/en/docs/marketinformation/symbolinfointeger), [PrintFormat](/en/docs/common/printformat)
