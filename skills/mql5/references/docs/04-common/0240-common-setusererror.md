# SetUserError

Sets the predefined variable [_LastError](/en/docs/predefined/_lasterror) into the value equal to [ERR_USER_ERROR_FIRST](/en/docs/constants/errorswarnings/errorcodes#err_user_error_first) + user_error

```
void  SetUserError(
   ushort user_error,   // error number
   );

```

Parameters

user_error

[in]  [Error](/en/docs/constants/errorswarnings/errorcodes) number set by a user.

Return Value

No return value.

Note

After an error has been set using the SetUserError(user_error) function, [GetLastError()](/en/docs/check/getlasterror) returns value equal to [ERR_USER_ERROR_FIRST](/en/docs/constants/errorswarnings/errorcodes#err_user_error_first) + user_error.

Example:

```
void OnStart()
  {
//--- set error number 65537=(ERR_USER_ERROR_FIRST +1)
   SetUserError(1);
//--- get last error code
   Print("GetLastError = ",GetLastError());
/* 
   Result
   GetLastError = 65537
*/ 
  }

```
