# Services

A service is an MQL program with a single OnStart handler and the #property service directive.

Recall that after the successful compilation of the service, you need to create and configure its instance (one or more) using the Add Service command in the context menu of the Navigator window.

As an example of a service, let's solve a small applied problem that often arises among developers of MQL programs. Many of them practice linking their programs to the user's account number. This is not necessarily about a paid product but may refer to distribution among friends and acquaintances to collect statistics or successful settings. At the same time, the user can register demo accounts in addition to a working real account. The lifetime of such accounts is usually limited, and therefore it is rather inconvenient to update the link for them every couple of weeks. To do this, you need to edit the source code, compile and send the program again.

Instead, we can develop a service that will register in global variables (or files) the numbers of accounts to which a successful connection was implemented from the given terminal.

The binding technology is based on pairwise encryption (or, alternatively, hashing) of account numbers: the old login account and the new login account. The previous account must be a master account (to which the conditional link is "issued") in order for the pair's common signature to extend the rights to use the product to the new account. The key is a secret known only inside the programs (it is assumed that all of them are supplied in a closed, compiled form). The result of the operation will be a string in the Base64 format. The implementation uses MQL5 API functions, some of which are yet to be studied, in particular, obtaining an account number via [AccountInfoInteger](/en/book/automation/account/account_info_overview) and [CryptEncode](/en/book/advanced/crypt/crypt_encode) encryption function. Connection to the server is checked using the TerminalInfoInteger function (see [Checking network connections](/en/book/common/environment/env_connectivity)).

The service is not required to know which accounts are master, and which ones are additional ones. It only needs to sign pairs of any successively logged-in accounts in a special way. But a specific application program should supplement the process of checking its "license": in addition to comparing the current account with the master account, you should repeat the service algorithm: create a pair [master account; current account], calculate the encrypted signature for it, and check whether it is among the global variables.

It will be possible to steal such a license by transferring it to another computer only if you connect to the same account in trading mode (not investor). An unscrupulous user, of course, can create demo accounts for other people. Therefore, it is desirable to improve the protection. In the current implementation, the global variable is simply made temporary, that is, it is deleted along with the end of the terminal session, but this does not prevent its possible copying.

As additional measures, it is possible, for example, to encrypt the time of its creation in the signature and provide for the expiration of rights every day (or with another frequency). Another option is to generate a random number when the service starts and add it to the signed information along with account numbers. This number is known only inside the service, but it can translate it to interested MQL programs on charts using the [EventChartCustom](/en/book/applications/events/events_custom) function. Thus, the signature will continue to be valid in this instance of the terminal until the end of the session. Each session will generate and send a new random number, so it will not work for other terminals. Finally, the simplest and most convenient option would probably be to add to the signature of the system start time: (TimeLocal() - GetTickCount() / 1000) or its derivative.

Of the various types of MQL programs, only some continue to run between account switches and allow this protection scheme to be implemented. Since it is necessary to protect MQL programs of any type in a uniform way, including indicators and Expert Advisors (which are reloaded when the account is changed), it makes sense to entrust this task to a service. Then the service, which is constantly running from the moment the terminal is loaded until it is closed, will control logins and generate authorizing signatures.

The source code of the service is given in the file MQL5/Services/MQL5Book/p5/ServiceAccount.mq5. The input parameters specify the master account and the prefix of global variables in which signatures will be stored. In real programs, lists of master accounts should be hardcoded in the source code, and instead of global variables, it is better to use files in the Common folder to cover the tester as well.

```
#property service
   
input long MasterAccount = 123456789;
input string Prefix = "!A_";

```

The main function of the service performs its work as follows: in an endless loop with pauses of 1 second, we track account changes and save the last number, create a signature for the pair, and write it to a global variable. The signature is created by the Cipher function.

```
void OnStart()
{
   static long account = 0; // previous login
   
   for(; !IsStopped(); )
   {
      // require connection, successful login and full access (not investor)
      const bool c = TerminalInfoInteger(TERMINAL_CONNECTED)
                  && AccountInfoInteger(ACCOUNT_TRADE_ALLOWED);
      const long a = c ? AccountInfoInteger(ACCOUNT_LOGIN) : 0;
   
      if(account != a) // account changed
      {
         if(a != 0) // current account
         {
            if(account != 0) // previous account
            {
               // transfer authorization from one to another
               const string signature = Cipher(account, a);
               PrintFormat("Account %I64d registered by %I64d: %s", 
                  a, account, signature);
               // saving a record about the connection of accounts
               if(StringLen(signature) > 0)
               {
                  GlobalVariableTemp(Prefix + signature);
                  GlobalVariableSet(Prefix + signature, account);
               }
            }
            else // the first account is authorized, now waiting for the second one
            {
               PrintFormat("New account %I64d detected", a);
            }
            // remember the last active account
            account = a;
         }
      }
      Sleep(1000);
   }
}

```

The Cipher function uses a special union ByteOverlay2 to represent a pair of account numbers (of type long) as a byte array, which is passed for encryption in CryptEncode (CRYPT_DES encryption method is chosen here, but it can be replaced with CRYPT_AES128, CRYPT_AES256 or just CRYPT_HASH_SHA256 hashing (with secret as "salt"), if information recovery from "signature" is not required).

```
template<typename T>
union ByteOverlay2
{
   T values[2];
   uchar bytes[sizeof(T) * 2];
   ByteOverlay2(const T v1, const T v2) { values[0] = v1; values[1] = v2; }
};
   
string Cipher(const long data1, const long data2)
{
   // TODO: replace the secret with your passphrase
   // TODO: CRYPT_AES128/CRYPT_AES256 methods require 16/32 byte arrays
   const static uchar secret[] = {'S', 'E', 'C', 'R', 'E', 'T', '0'};
   ByteOverlay2<long> bo(data1, data2);
   uchar result[];
   if(CryptEncode(CRYPT_DES, bo.bytes, secret, result) > 0)
   {
      uchar dummy[], text[];
      if(CryptEncode(CRYPT_BASE64, result, dummy, text) > 0)
      {
         return CharArrayToString(text);
      }
   }
   return NULL;
}

```

Then any program in the terminal can check if there are "licenses" for the current account in the global variables. This is done using the CheckAccounts and IsCurrentAccountAuthorizedByMaster functions. They are shown in the service just for demonstration purposes.

The CheckAccounts functions performs a check on hardcoded all master accounts to find those matching the current one.

```
bool CheckAccounts()
{
   const long accounts[] = {MasterAccount}; // TODO: to fill array with constants
   for(int i = 0; i < ArraySize(accounts); ++i)
   {
      if(IsCurrentAccountAuthorizedByMaster(accounts[i])) return true;
   }
   return false;
}

```

IsCurrentAccountAuthorizedByMaster takes the number of one master account as a parameter, recreates a "signature" for it in a pair with the current account, and analyzes matches.

```
bool IsCurrentAccountAuthorizedByMaster(const long data)
{
   const long a = AccountInfoInteger(ACCOUNT_LOGIN);
   if(a == data) return true; // direct match
   const string s = Cipher(data, a); // recalculating "signature"
   if(a != 0 && GlobalVariableGet(Prefix + s) == a)
   {
      Print("Sub-License is active: ", s);
      return true;
   }
   return false;
}

```

Let's assume that programs are allowed to run on account 123456789 and it is currently active. On start, the service will respond with a log entry:

```
New account 123456789 detected

```

If we then change the account number, for example, to 5555555, we get the following signature:

```
Account 5555555 registered by 123456789: jdVKxUswBiNlZzDAnV3yxw==

```

If we stop and start the service again, we will see the verification of account 5555555 in action (calling the function CheckAccounts embedded for demonstration at the beginning OnStart).

```
Sub-License is active: jdVKxUswBiNlZzDAnV3yxw==
Account 123456789 registered by 5555555: ZWcwwJ1d8seN1UrFSzAGIw==

```

The license worked for the new account. If you switch back, a "pass" will be generated from the current account to the previous one (this is a consequence of the fact that the service does not "know" which accounts are primary and which are temporary, and such a "signature" is most likely not required in programs).

To indirectly authorize a new account, you will need to log into the master account again and only then switch to the new one: this will create another global variable with the encrypted pair [master account; new account].

This version of the service does not check that the master account is real and the dependent account is demo. Each of these restrictions can be added.
