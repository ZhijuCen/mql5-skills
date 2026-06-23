# Binding a program to runtime properties

As an example of working with the properties described in the previous sections, let's consider the popular task of binding an MQL program to a hardware environment to protect it from copying. When the program is distributed through the MQL5 Market, the binding is provided by the service itself. However, if the program is developed on a custom basis, it can be linked either to the account number, or to the name of the client, or to the available properties of the terminal (computer). The first is not always convenient, because many traders have several live accounts (probably with different brokers), not to mention demo accounts with a limited validity period. The second may be fictional or too commonplace. Therefore, we will implement a prototype algorithm for binding a program to a selected set of environment properties. More serious security schemes could probably use a DLL and directly read device hardware labels from Windows, but not every client will agree to run potentially unsafe libraries.

Our protection option is presented in the script EnvSignature.mq5. The script calculates hashes from the given properties of the environment and creates a unique signature (imprint) based on them.

Hashing is a special processing of arbitrary information, as a result of which a new block of data is created that has the following characteristics (they are guaranteed by the algorithm used):

- Matching hash values for two original data sets means, with almost 100% probability, that the data are identical (the probability of a random match is negligible).
- If the original data changes, their hash value will also change.
- It is impossible to mathematically restore the original data from the hash value (they remain secret) unless a complete enumeration of possible initial values is performed (if their initial size increases and there is no information about their structure, the problem is unsolvable in the foreseeable future).
- The hash size is fixed (does not depend on the amount of initial data).

Suppose one of the environment properties is described by the string: "TERMINAL_LANGUAGE=German". It can be obtained with a simple statement like the following (simplified):

```
string language = EnumToString(TERMINAL_LANGUAGE) +
            "=" + TerminalInfoString(TERMINAL_LANGUAGE);

```

The actual language will match the settings. Having a hypothetical Hash function, we can compute the signature.

```
string signature = Hash(language);

```

When there are more properties, we simply repeat the procedure for all of them, or request a hash from the combined strings (so far this is pseudo-code, not part of the real program).

```
string properties[];
// fill in the property lines as you wish
// ...
string signature;
for(int i = 0; i < ArraySize(properties); ++i)
{
   signature += properties[i];
}
return Hash(signature);

```

The received signature can be reported by the user to the program developer, who will "sign" it in a special way, upon receiving a validation string suitable only for this signature. The signature is also based on hashing and requires knowledge of some secret (password phrase), known only to the developer and hard-coded into the program (for the verification phase).

The developer will pass the validation string to the user who then will be able to run the program by specifying this string in the parameters.

When launched without a validation string, the program should generate a new signature for the current environment, print it to the log, and exit (this information should be passed to the developer). With an invalid validation string, the program should display an error message and exit.

Several launch modes can be provided for the developer himself: with a signature, but without a validation string (to generate the last one), or with a signature and a validation string (here the program will re-sign the signature and compare it with the specified validation string just for checking).

Let's estimate how selective such protection will be. After all, the binding here is not performed to a unique identifier of anything.

The following table provides statistics on two characteristics: screen size and RAM. Obviously, the values will change over time, but the approximate distribution will remain the same: a few characteristic values will be the most popular, while some "new" advanced and "old" ones that are going out of circulation will make up decreasing "tails".

| Screen | 1920x1080 | 1536x864 | 1440x900 | 1366x768 | 800x600 |
| RAM | 21% | 7% | 5% | 10% | 4% |
| --- | --- | --- | --- | --- | --- |
| 4Gb    20% | 4.20 | 1.40 | 1.00 | 2.0 | 0.8 |
| 8Gb    20% | 4.20 | 1.40 | 1.00 | 2.0 | 0.8 |
| 16Gb  15% | 3.15 | 1.05 | 0.75 | 1.5 | 0.6 |
| 32Gb  10% | 2.10 | 0.70 | 0.50 | 1.0 | 0.4 |
| 64Gb    5% | 1.05 | 0.35 | 0.25 | 0.5 | 0.2 |

Pay attention to the cells with the largest values, because they mean the same signatures (unless we introduce an element of randomness into them, which will be discussed below). In this case, two combinations of characteristics in the upper left corner are most likely, with each at 4.2%. But these are only two features. If you add the interface language, time zone, number of cores, and working data path (preferably shared, since it contains the Windows username) to the evaluated environment, then the number of potential matches will noticeably decrease.

For hashing, we use the built-in CryptEncode function (it will be described in the [Cryptography](/en/book/advanced/crypt/crypt_encode) section) that supports the SHA256 hashing method. As its name suggests, it produces a hash that is 256 bits long, i.e., 32 bytes. If we needed to show it to the user, then we would translate it into text in hexadecimal representation and get a 64-character long string.

To make the signature shorter, we will convert it using Base64 encoding (it is also supported by the CryptEncode function and its counterpart CryptDecode), which will give a 44-character long string. Unlike a one-way hash operation, Base64 encoding is reversible, i.e. the original data can be recovered from it.

The main operations are implemented by the EnvSignature class. It defines the data string which should accumulate certain fragments describing the environment. The public interface consists of several overloaded versions of the append function to add strings with environment properties. Essentially, they join the name of the requested property and its value using some abstract element returned by the virtual 'pepper' method as a link. The derived class will define it as a specific string (but it can be empty).

```
class EnvSignature
{
private:
   string data;
protected:
   virtual string pepper() = 0;
public:
   bool append(const ENUM_TERMINAL_INFO_STRING e)
   {
      return append(EnumToString(e) + pepper() + TerminalInfoString(e));
   }
   bool append(const ENUM_MQL_INFO_STRING e)
   {
      return append(EnumToString(e) + pepper() + MQLInfoString(e));
   }
   bool append(const ENUM_TERMINAL_INFO_INTEGER e)
   {
      return append(EnumToString(e) + pepper()
        + StringFormat("%d", TerminalInfoInteger(e)));
   }
   bool append(const ENUM_MQL_INFO_INTEGER e)
   {
      return append(EnumToString(e) + pepper()
        + StringFormat("%d", MQLInfoInteger(e)));
   }

```

To add an arbitrary string to an object, there is a generic method append, which is called in the above methods.

```
   bool append(const string s)
   {
      data += s;
      return true;
   }

```

Optionally, the developer can add a so-called "salt" to the hashed data. This is an array with randomly generated data which further complicates hash reversal. Each generation of the signature will be different from the previous one, even though the environment remains constant. The implementation of this feature as well as of other more specific protection aspects (such as the use of symmetric encryption and dynamic calculation of the secret) are left for independent study.

Since the environment consists of well-known properties (their list is limited by MQL5 API constants), and not all of them are sufficiently unique, our defense, as we calculated, can generate the same signatures for different users if we do not use the salt. The signature match will not allow identifying the source of the license leak if it happened.

Therefore, you can increase the effectiveness of protection by changing the method of presenting properties before hashing for each customer. Of course, the method itself should not be disclosed. In the considered example, this implies changing the contents of the pepper method and recompiling the product. This can be expensive, but it allows you to avoid using random salt.

With the property string filled in, we can generate a signature. This is done using the emit method.

```
   string emit() const
   {
      uchar pack[];
      if(StringToCharArray(data + secret(), pack, 0, 
         StringLen(data) + StringLen(secret()), CP_UTF8) <= 0) return NULL;
   
      uchar key[], result[];
      if(CryptEncode(CRYPT_HASH_SHA256, pack, key, result) <= 0) return NULL;
      Print("Hash bytes:");
      ArrayPrint(result);
   
      uchar text[];
      CryptEncode(CRYPT_BASE64, result, key, text);
      return CharArrayToString(text);
   }

```

The method adds a certain secret (a sequence of bytes known only to the developer and located inside the program) to the data and calculates the hash for the shared string. The secret is obtained from the virtual secret method, which will also define the derived class.

The resulting byte array with the hash is encoded into a string using Base64.

Now comes the most important class function: check. It is this function that implements the signature from the developer and checks it from the user.

```
   bool check(const string sig, string &validation)
   {
      uchar bytes[];
      const int n = StringToCharArray(sig + secret(), bytes, 0, 
         StringLen(sig) + StringLen(secret()), CP_UTF8);
      if(n <= 0) return false;
      
      uchar key[], result1[], result2[];
      if(CryptEncode(CRYPT_HASH_SHA256, bytes, key, result1) <= 0) return false;
      
      /*
        WARNING
        The following code should only be present in the developer utility.
        The program supplied to the user must compile without this if.
      */
      #ifdef I_AM_DEVELOPER
      if(StringLen(validation) == 0)
      {
         if(CryptEncode(CRYPT_BASE64, result1, key, result2) <= 0) return false;
         validation = CharArrayToString(result2);
         return true;
      }
      #endif
      uchar values[];
      // the exact length is needed to not append terminating '0'
      if(StringToCharArray(validation, values, 0, 
         StringLen(validation)) <= 0) return false;
      if(CryptDecode(CRYPT_BASE64, values, key, result2) <= 0) return false;
      
      return ArrayCompare(result1, result2) == 0;
   }

```

During normal operation (for the user), the method calculates the hash from the received signature, supplemented by the secret, and compares it with the value from the validation string (it must first be decoded from Base64 into the raw binary representation of the hash). If the two hashes match, the validation is successful: the validation string matches the property set. Obviously, an empty validation string (or a string entered at random) will not pass the test.

On the developer's machine, the I_AM_DEVELOPER macro must be defined in the source code for the signature utility, which results in an empty validation string being handled differently. In this case, the resulting hash is Base64 encoded, and this string is passed out through the validation parameter. Thus, the utility will be able to display a ready-made validation string for the given signature to the developer.

To create an object, you need a certain derived class that defines strings with the secret and pepper.

```
// WARNING: change the macro to your own set of random bytes
#define PROGRAM_SPECIFIC_SECRET "<PROGRAM-SPECIFIC-SECRET>"
// WARNING: choose your characters to link in pairs name'='value 
#define INSTANCE_SPECIFIC_PEPPER "=" // obvious single sign is selected for demo
// WARNING: the following macro needs to be disabled in the real product,
//          it should only be in the signature utility
#define I_AM_DEVELOPER
#ifdef I_AM_DEVELOPER
#define INPUT input
#else
#define INPUT const
#endif
 
INPUT string Signature = "";
INPUT string Secret = PROGRAM_SPECIFIC_SECRET;
INPUT string Pepper = INSTANCE_SPECIFIC_PEPPER;
 
class MyEnvSignature : public EnvSignature
{
protected:
   virtual string secret() override
   {
      return Secret;
   }
   virtual string pepper() override
   {
      return Pepper;
   }
};

```

Let's quickly pick a few properties to fill in the signature.

```
void FillEnvironment(EnvSignature &env)
{
   // the order is not important, you can mix
   env.append(TERMINAL_LANGUAGE);
   env.append(TERMINAL_COMMONDATA_PATH);
   env.append(TERMINAL_CPU_CORES);
   env.append(TERMINAL_MEMORY_PHYSICAL);
   env.append(TERMINAL_SCREEN_DPI);
   env.append(TERMINAL_SCREEN_WIDTH);
   env.append(TERMINAL_SCREEN_HEIGHT);
   env.append(TERMINAL_VPS);
   env.append(MQL_PROGRAM_TYPE);
}

```

Now everything is ready to test our protection scheme in the OnStart function. But first, let's look at the input variables. Since the same program will be compiled in two versions, for the end user and for the developer, there are two sets of input variables: for entering registration data by the user and for generating this data based on the developer's signature. The input variables intended for the developer have been described above using the INPUT macro. Only the validation string is available to the user.

```
input string Validation = "";

```

When the string is empty, the program will collect the environment data, generate a new signature, and print it to the log. This completes the work of the script since access to the useful code has not yet been confirmed.

```
void OnStart()
{
   MyEnvSignature env;
    string signature;
   if(StringLen(Signature) > 0)
   {
     // ... here will be the code to be signed by the author
   }
   else
   {
      FillEnvironment(env);
      signature = env.emit();
   }
   
   if(StringLen(Validation) == 0)
   {
      Print("Validation string from developer is required to run this script");
      Print("Environment Signature is generated for current state...");
      Print("Signature:", signature);
      return;
   }
   else
   {
     // ... check the validation string here
   }
   Print("The script is validated and running normally");
   // ... actual working code is here
}

```

If the variable Validation is filled, we check its compliance with the signature and terminate the work in case of failure.

```
   if(StringLen(Validation) == 0)
   {
      ...
   }
   else
   {
      validation = Validation; // need a non-const argument
      const bool accessGranted = env.check(Signature, validation);
      if(!accessGranted)
      {
         Print("Wrong validation string, terminating");
         return;
      }
      // success
   }
   Print("The script is validated and running normally");
   // ... actual working code is here
}

```

If there are no discrepancies, the algorithm proceeds to the working code of the program.

On the developer's side (in the version of the program that was built with the I_AM_DEVELOPER macro), a signature can be introduced. We restore the state of the MyEnvSignature object using the signature and calculate the validation string.

```
void OnStart()
{
   ...
   if(StringLen(Signature) > 0)
   {
      #ifdef I_AM_DEVELOPER
      if(StringLen(Validation) == 0)
      {
         string validation;
         if(env.check(Signature, validation))
           Print("Validation:", validation);
         return;
      }
      signature = Signature; 
      #endif
   }
   ...

```

The developer can not only specify the signature but also validate it: in this case, the code execution will continue in the user mode (for debugging purposes).

If you wish, you can simulate a change in the environment, for example, as follows:

```
      FillEnvironment(env);
      // artificially make a change in the environment (add a time zone)
      // env.append("Dummy" + (string)(TimeGMTOffset() - TimeDaylightSavings()));
      const string update = env.emit();
      if(update != signature)
      {
         Print("Signature and environment mismatch");
         return;
      }

```

Let's look at a few test logs.

When you first run the EnvSignature.mq5 script, the "user" will see something like the following log (values will vary due to environment differences):

```
Hash bytes:
  4 249 194 161 242  28  43  60 180 195  54 254  97 223 144 247 216 103 238 245 244 224   7  68 101 253 248 134  27 102 202 153
Validation string from developer is required to run this script
Environment Signature is generated for current state...
Signature:BPnCofIcKzy0wzb+Yd+Q99hn7vX04AdEZf34hhtmypk=

```

It sends the generated signature to the "developer" (there are no actual users during the test, so all the roles of "user" and "developer" are quoted), who enters it into the signing utility (compiled with the I_AM_DEVELOPER macro), in the Signature parameter. As a result, the program will generate a validation string:

```
Validation:YBpYpQ0tLIpUhBslIw+AsPhtPG48b0qut9igJ+Tk1fQ=

```

The "developer" sends it back to the "user", and the "user", by entering it into the Validation parameter, will get the activated script:

```
Hash bytes:
  4 249 194 161 242  28  43  60 180 195  54 254  97 223 144 247 216 103 238 245 244 224   7  68 101 253 248 134  27 102 202 153
The script is validated and running normally

```

To demonstrate the effectiveness of protection, let's duplicate the script as a service: to do this, let's copy the file to the folder MQL5/Services/MQL5Book/p4/ and replace the following line in the source code:

```
#property script_show_inputs

```

with the following line:

```
#property service

```

Let's compile the service, create and run its instance, and specify the previously received validation string in the input parameters. As a result, the service will abort (before reaching the statements with the required code) with the following message:

```
Hash bytes:
147 131  69  39  29 254  83 141  90 102 216 180 229 111   2 246 245  19  35 205 223 145 194 245  67 129  32 108 178 187 232 113
Wrong validation string, terminating

```

The point is that among the properties of the environment we have used the string MQL_PROGRAM_TYPE. Therefore, an issued license for one type of program will not work for another type of program, even if it is running on the same user's computer.
